import logging
import os       # 与路径操作相关的包，用于管理文件
import pandas
import importlib
import multiprocessing
import csv

from lxml.doctestcompare import strip

from config import default_data
from config import k_line_types
from config import instruments

# 最小变化单位文件路径
mindiff_file_path = '../data/mindiff/mindiff.csv'

factor_names_data = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    'factor_name.csv'
)

def get_factor_calculator(factor_name):
    """
    动态调用各个因子计算器
    :param factor_name:需要导入的因子名称
    :return:返回因子的类名称，供后续导入
    """
    # 这里假设每个因子模块名和类名都与 factor_name 一致
    try:
        module = importlib.import_module(f'{factor_name}')
        factor_class = getattr(module, factor_name)
        return factor_class
    except Exception as e:
        logger.error(f"Importing {factor_name} failed: {e}")
        return None

def split_factor_name(factor_name):
    """
    对一个因子名称进行分割，考虑两种情况，并返回因子部分和长度部分
    :param factor_name:需要处理的因子名称
    :return:返回两个值，一个是因子基础名称的部分，一个是长度部分
    """
    if '@' in factor_name:
        # 对存在长度的因子名称进行分割
        parts = factor_name.split('@')
        if len(parts) == 2:
            factor = parts[0]
            factor_length = int(parts[1])   # 这里对长度进行强制转换
            return factor, factor_length
    # 对没有长度的因子，直接返回结果即可
    return factor_name, None

def read_single_column(file_path, skip_header=True):
    """
    读取单列 CSV 文件，返回一个包含所有行数据的列表
    :param file_path: CSV 文件路径
    :param skip_header: 是否跳过第一行（标题行），默认为 True
    :return: 返回一个列表，包含 CSV 文件中所有数据行的第一列内容
    """
    data = []
    with open(file_path, mode='r', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        if skip_header:
            next(reader)    # 跳过标题行
        for row in reader:
            if row:
                data.append(row[0].strip()) # 取出首尾空白字符
    return data

def run_one_instrument(instrument, k_line_type, instruments_mindiff):
    # 子进程专用 logger 配置
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - [%(module)s] %(message)s',
        handlers=[
            logging.FileHandler('app.log'),
            logging.StreamHandler()
        ]
    )
    # 定义 logger
    local_logger = logging.getLogger(__name__)

    try:
        calculator = factor_calculator([instrument], k_line_type, instruments_mindiff)
        calculator.factors_cal(local_logger)  # 传入 logger
    except Exception as e:
        logging.exception(f"Error processing {instrument}, {k_line_type} : {e}")

class factor_calculator:
    def __init__(self, instruments, k_line_type, instruments_mindiff):
        """
        初始化因子计算器
        :param instruments: 期货品种列表
        :param k_line_typ: K线类型
        """
        self.instruments = instruments
        self.k_line_type = k_line_type
        self.instruments_mindiff = instruments_mindiff

    def factors_cal(self, logger):
        """
        调用各个因子计算器，并返回计算结果
        :return: 以 dataframe 的格式返回因子计算的结果，
        """
        for instrument in self.instruments:
            # 构建数据路径
            data_path = os.path.join(
                os.path.dirname(os.path.abspath(__file__)),
                f'../data/{self.k_line_type}/{instrument}/{instrument}.csv'
            )
            logger.info(f"Trying to read: {data_path}")
            if not os.path.exists(data_path):
                logger.warning(f"File not exists: {data_path}")
                continue

            try:
                # 读取数据
                df = pandas.read_csv(data_path)
            except Exception as e:
                logger.error(f"Failed to read file: {data_path}, error at: {e}")
                continue

            # 获取因子名称列表
            factor_names = read_single_column(factor_names_data, skip_header=True)

            # 遍历因子字典，逐个计算因子
            # 第一层循环是关于k线类型的循环

            # 第二层循环是关于因子名称的循环
            for factor_name in factor_names:
                # 这里将分割后的结果进行解包
                factor, length = split_factor_name(factor_name)

                # 构建param字典，包含df和length
                param = {
                    'df':           df,
                    'instrument':   instrument,
                    'length':       length,
                    'k_line_type':  self.k_line_type,
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
                    logger.warning(f"{instrument} no set mindiff")
                    continue

                # 设置因子保存路径
                save_path = os.path.join(
                    os.path.dirname(os.path.abspath(__file__)),
                    f'../data/{self.k_line_type}/{instrument}/{factor_name}.csv'
                )

                # 动态导入需要的因子计算器的包
                calculator_class = get_factor_calculator(factor)
                if calculator_class is None:
                    logger.warning(f"Import failed: {factor}")
                    continue

                # 创建因子计算器实例
                calculator_instance = calculator_class()

                try:
                    # 检查文件是否存在，以跳出当前因子计算的循环
                    if os.path.exists(save_path):
                        # print(f"{save_path}已存在，跳过该因子该长度的计算")
                        continue

                    # 因子计算信息回报
                    logger.info(f"Calculating: {instrument} {factor_name} {self.k_line_type} {length}")

                    # 计算每一个因子，调用 calculator.formula 并传入参数进行计算
                    result = calculator_instance.formula(param)

                    # 利用 os.makedirs 设置一个路径，并利用to_csv保存结果
                    os.makedirs(os.path.dirname(save_path), exist_ok=True)
                    result.to_csv(save_path, index=False)

                    # 保存成功信息回报
                    logger.info(f"Calculate success: {save_path}")

                except Exception as e:
                    # 当因子计算出错时报错
                    logger.exception(f"Calculate failed: {save_path}, error at: {e}")

# 主程序入口
if __name__ == "__main__":
    # 配置 root logger
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - [%(module)s] %(message)s',
        handlers=[
            logging.FileHandler('app.log', encoding='utf-8'),  # 设置编码为 utf-8
            logging.StreamHandler()
        ]
    )

    # 定义 logger
    logger = logging.getLogger(__name__)

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
                logger.warning(f"Skip invalid data: {row}")

    logger.info(f"Loaded instruments_mindiff: {instruments_mindiff}")

    '''
    # 单进程处理每个因子
    for k_line_type in k_line_types:
        logging.info(f"Processing: {k_line_type}")

        for instrument in instruments:
            for length in lengths:
                run_one_instrument(instrument, k_line_type, instruments_mindiff)

        logging.info(f"Finished: {k_line_type}")
    '''

    # 利用进程池计算每个因子
    for k_line_type in k_line_types:
        logger.info(f"Processing: {k_line_type}")
        pool = multiprocessing.Pool(processes=multiprocessing.cpu_count())

        for instrument in instruments:
            pool.apply_async(run_one_instrument, args=(instrument, k_line_type, instruments_mindiff))
        pool.close()
        pool.join()
        logger.info(f"Finished: {k_line_type}")