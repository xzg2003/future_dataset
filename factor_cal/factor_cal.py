import os       # 与路径操作相关的包，用于管理文件
import pandas
import importlib

from config import factor_names
from config import factor_categories
from config import default_data

# 设置工作目录为当前脚本所在的目录
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# 动态调用各个因子计算器
def get_factor_name(factor_name):
    # 这里假设每个因子模块名和类名都与 factor_name 一致
    try:
        module = importlib.import_module(f'.{factor_name}', __package__)
        factor_class = getattr(module, factor_name)
        return factor_class
    except Exception as e:
        print(f"导入{factor_name}失败：{e}")
        return None

class factor_calculator:
    def __init__(self, instruments, k_line_type, lengths, instruments_mindiff):
        """
        初始化因子计算器
        :param instruments: 期货品种列表
        :param k_line_type: K线类型
        :param lengths:     滑动平均长度列表
        """
        self.instruments = instruments
        self.k_line_type = k_line_type
        self.lengths = lengths
        self.instruments_mindiff = instruments_mindiff

        """
        初始化所有因子计算器
        以字典的形式，将每个计算器与其名称进行对应，便于在程序中调用
        
        这里优先计算 Tr 因子，因为后续很多因子计算都需要调用 Tr 的数据
        先计算 Tr，在计算其他因子时可以调用 Tr.csv 文件中的数据，简化计算
        
        经过程序结构的优化，这里改为自动化导入
        在对字典导入的同时，导入每个因子计算器的类
        """
        self.factors_dict = {}
        for name in factor_names:
            factor_class = get_factor_name(name)
            if factor_class is not None:
                self.factors_dict[name] = factor_class()

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
                    # 构建param字典，包含df和length
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
                        # 设置保存路径，根据命名规则分开讨论
                        if factor_name in factor_categories["no_length"]:
                            save_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), f'../data/{self.k_line_type}/{instrument}/{factor_name}.csv')
                        elif factor_name in factor_categories["short_long"]:
                            save_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), f'../data/{self.k_line_type}/{instrument}/{factor_name}@{param["short"]}_{param["long"]}.csv')
                        elif factor_name in factor_categories["length_thr"]:
                            save_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), f'../data/{self.k_line_type}/{instrument}/{factor_name}@{length}_{param["thr"]}.csv')
                        elif factor_name in factor_categories["length_atr"]:
                            save_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), f'../data/{self.k_line_type}/{instrument}/{factor_name}@{length}_{param["atr_length"]}.csv')
                        elif factor_name in factor_categories["length_n_std"]:
                            save_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), f'../data/{self.k_line_type}/{instrument}/{factor_name}@{length}_{param["n_std"]}.csv')
                        elif factor_name in factor_categories["short_long_atr"]:
                            save_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), f'../data/{self.k_line_type}/{instrument}/{factor_name}@{param["short"]}_{param["long"]}_{param["atr_length"]}.csv')
                        elif factor_name in factor_categories["short_long_vol"]:
                            save_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), f'../data/{self.k_line_type}/{instrument}/{factor_name}@{param["short"]}_{param["long"]}_{param["vol_length"]}.csv')
                        else:
                            save_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), f'../data/{self.k_line_type}/{instrument}/{factor_name}@{length}.csv')

                        # 检查文件是否存在，以跳出当前因子计算的循环
                        if os.path.exists(save_path):
                            print(f"{save_path}已存在，跳过该因子该长度的计算")
                            continue

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


"""
# 主程序入口
if __name__ == "__main__":
    '''
    数据的初始化，在main.py里面也有相同的部分，便于使用者调整数据处理的范围
    instruments:    期货品种
    k_line_type:    k线类型
    lengths:        滑动平均长度
    '''
    instruments = ['A']
    k_line_type = '5m'
    lengths = [10, 20, 40, 80, 120, 180]

    # 创建因子计算器实例，以调用内部的函数
    calculator = factor_calculator(instruments, k_line_type, lengths, mindiff)

    # 计算所有因子
    calculator.factors_cal()
"""