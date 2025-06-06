import os       # 与路径操作相关的包，用于管理文件
import pandas
import importlib
import csv
import multiprocessing
import sys

# 包所在的根目录
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config import factor_categories
from config import default_data
from config import k_line_types
from config import instruments
from config import lengths

# 最小变化单位文件路径
mindiff_file_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'data', 'mindiff', 'mindiff.csv')
factor_name_file_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'factor_name.csv')


# 进程池中，因子计算器的调用函数
def run_one_instrument(instrument, k_line_type, length, instruments_mindiff, factor_names):
    calculator = factor_calculator([instrument], [k_line_type], length, instruments_mindiff, factor_names)
    calculator.factors_cal()

# 因子名称的拆分
def split_factor_name(factor_name):
    """
    拆分因子名，返回基础名和参数部分
    例如：FCT_Ac_Tr_1@180 -> ('FCT_Ac_Tr_1', '@180')
    """
    if '@' in factor_name:
        # 这是因为，有因子并不依赖于任何参数的限制，因此还需要对 @ 这个中间符号进行判断
        idx = factor_name.index('@')
        return factor_name[:idx], factor_name[idx:]
    else:
        return factor_name, ''

# 动态调用各个因子计算器
def get_factor_name(factor_name):
    """
    这里假设每个因子模块名和类名都与 factor_name 一致

    直接调用 split_factor_name，对因子名称进行分割
    """
    base_name, _ = split_factor_name(factor_name)
    try:
        module = importlib.import_module(f'factor_cal.{base_name}')
        factor_class = getattr(module, base_name)
        return factor_class
    except Exception as e:
        print(f"Import {factor_name} failed: {e}")
        return None

class factor_calculator:
    def __init__(self, instruments, k_line_types, lengths, instruments_mindiff, factor_names):
        """
        初始化因子计算器
        :param instruments: 期货品种列表
        :param k_line_type: K线类型
        :param lengths:     滑动平均长度列表
        """
        self.instruments = instruments
        self.k_line_types = k_line_types
        self.lengths = lengths
        self.instruments_mindiff = instruments_mindiff

        """
        初始化所有因子计算器
        以字典的形式，将每个计算器与其名称进行对应，便于在程序中调用
        
        这里优先计算 Tr 因子，因为后续很多因子计算都需要调用 Tr 的数据
        先计算 Tr，在计算其他因子时可以调用 Tr.csv 文件中的数据，简化计算
        
        经过程序结构的优化，这里改为自动化导入
        在对字典导入的同时，导入每个因子计算器的类

        用全名做 key， 基础类做 value
        """
        self.factors_dict = {}
        self.factors_base_map = {} # 记录全名到基础名的映射
        for name in factor_names:
            base_name, param_part = split_factor_name(name)
            factor_class = get_factor_name(name)
            if factor_class is not None:
                self.factors_dict[name] = factor_class()
                self.factors_base_map[name] = base_name

    def factors_cal(self):
        """
        调用所有计算器，计算相应因子并保存到文件夹中
        """
        for instrument in self.instruments:
            # 构建数据路径
            data_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), f'../data/5m/{instrument}/{instrument}.csv')
            print(f"Trying to read the file:{data_path}")
            if not os.path.exists(data_path):
                print(f"Not exist:{data_path}")
                continue

            try:
                # 读取数据
                df = pandas.read_csv(data_path)
            except Exception as e:
                print(f'Read failed:{data_path}, error info:{e}')
                continue

            # 遍历因子字典，逐个计算因子
            for factor_name, calculator in self.factors_dict.items():
                for length in self.lengths:
                    # 构建param字典
                    param = {
                        'df':           df,
                        'instrument':   instrument,
                        'length':       length,
                        'mindiff':      self.instruments_mindiff.get(instrument, None),
                        'short':        default_data["short"],
                        'long':         default_data["long"],
                        'atr_length':   default_data["atr_length"],
                        'vol_length':   default_data["vol_length"],
                        'thr':          default_data["thr"],
                        'n_std':        default_data["n_std"],
                        'fast':         default_data["fast"],
                        'slow':         default_data["slow"],
                        'signal':       default_data["signal"],
                    }

                    # 检查 mindiff 是否存在
                    if param['mindiff'] is None:
                        print(f"No mindiff for {instrument}, skip")
                        continue

                    try:
                        # 用全名作为文件名
                        save_path = os.path.join(
                            os.path.dirname(os.path.abspath(__file__)),
                            f'../data/{k_line_type}/{instrument}/{factor_name}.csv'
                        )

                        # 检查文件是否存在，以跳出当前因子计算的循环
                        if os.path.exists(save_path):
                            print(f"{save_path} exists, skip")
                            continue

                        # 因子计算信息回报
                        print(f"instrument:{instrument} factor:{save_path} calculating.")

                        # 计算每一个因子，调用 calculator.formula 并传入参数进行计算
                        result = calculator.formula(param)

                        # 利用 os.makedirs 设置一个路径，并利用to_csv保存结果
                        os.makedirs(os.path.dirname(save_path), exist_ok=True)
                        result.to_csv(save_path, index=False)

                        # 保存成功信息回报
                        print(f"instrument:{instrument} factor:{save_path} success.")
                    except Exception as e:
                        # 当因子计算出错时报错
                        print(f"error at{save_path}, {e}")



# 主程序入口
if __name__ == "__main__":
    # 初始化 mindiff 字典
    instruments_mindiff = {}

    # 读取 CSV 文件
    with open(mindiff_file_path, mode='r', encoding='utf-8') as mindiff_file:
        reader = csv.DictReader(mindiff_file)
        for row in reader:
            instrument = row['instrument'].strip()
            mindiff = row['mindiff']
            try:
                # 确保 instrument 和 mindiff 不为空
                if instrument and mindiff:
                    instruments_mindiff[instrument] = float(mindiff)
            except ValueError:
                print(f"Skip invalid data:{row}")

    print(f"Loaded instruments_mindiff:{instruments_mindiff}")

        # 读取因子名称列表
    factor_names = pandas.read_csv(factor_name_file_path, skiprows=[0], comment="#").iloc[:, 0].tolist()

# 单进程计算
for k_line_type in k_line_types:
    for instrument in instruments:
        # 创建因子计算器实例，以调用内部的函数
        calculator = factor_calculator([instrument], [k_line_type], lengths, instruments_mindiff, factor_names)

        # 计算所有的因子
        calculator.factors_cal()


"""
    # 利用进程池计算每个因子
    for k_line_type in k_line_types:
        print(f"Processing: {k_line_type}")
        pool = multiprocessing.Pool(processes=multiprocessing.cpu_count())

        for instrument in instruments:
            pool.apply_async(run_one_instrument, args=(instrument, k_line_type,instruments_mindiff, factor_names))

        pool.close()
        pool.join()
        print(f"Finished: {k_line_type}")
"""
