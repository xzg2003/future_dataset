
import os
import csv
import json
import pandas as pd
import concurrent.futures
import logging
import importlib
from multiprocessing import get_context
from config import default_data, k_line_types, instruments

# 最小变化单位文件路径
mindiff_file_path = '../mindiff.csv'
factor_names_data = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    'factor_name.csv'
)

# 配置根日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("factor_calculation.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

def configure_process_logger():
    """配置进程专用日志"""
    logger = logging.getLogger(f"process_{os.getpid()}")
    if not logger.handlers:
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - [PID:%(process)d] %(message)s')

        # 文件处理器
        file_handler = logging.FileHandler(f"process_{os.getpid()}.log")
        file_handler.setFormatter(formatter)

        # 控制台处理器
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)

        logger.addHandler(file_handler)
        logger.addHandler(console_handler)
        logger.setLevel(logging.INFO)

    return logger


def iterate_factor_parameters(json_file_path):
    """
    从新格式的JSON文件中读取因子配置并逐个输出参数
    新格式: {
        "Acceleration": [
            {"factor_name": "Acceleration@10", "length": 10},
            {"factor_name": "Acceleration@120", "length": 120}
        ],
        ...
    }
    """
    try:
        # 加载JSON文件
        with open(json_file_path, 'r', encoding='utf-8') as f:
            factors = json.load(f)

        # 遍历所有因子组
        for base_factor_name, factor_configs in factors.items():
            # 遍历该基础因子的所有配置
            for config in factor_configs:
                # 创建参数字典
                factor_params = {
                    "full_name": config["factor_name"],
                    "factor_name": base_factor_name,  # 使用基础因子名称
                }

                # 添加所有配置参数
                for key, value in config.items():
                    if key != "factor_name":  # 跳过已处理的字段
                        factor_params[key] = value

                # 确保包含必要的键（即使值为None）
                for param in ["length", "atr_length", "vol_length", "thr",
                              "n_std", "short", "long", "fast", "slow", "signal"]:
                    if param not in factor_params:
                        factor_params[param] = None

                # 返回当前因子的参数
                yield factor_params

        logger.info(f"成功处理 {len(factors)} 个基础因子组的参数")

    except FileNotFoundError:
        logger.error(f"错误: JSON文件 {json_file_path} 不存在")
        yield {}
    except json.JSONDecodeError:
        logger.error(f"错误: JSON文件 {json_file_path} 格式不正确")
        yield {}
    except Exception as e:
        logger.error(f"处理因子参数时出错: {str(e)}")
        yield {}

def get_factor_calculator(factor_name):
    """
    动态调用各个因子计算器
    """
    try:
        module = importlib.import_module(f'{factor_name}')
        factor_class = getattr(module, factor_name)
        return factor_class
    except Exception as e:
        logger.error(f"导入因子 {factor_name} 失败: {e}")
        return None

def load_instruments_mindiff(csv_path):
    """
    从CSV文件加载品种的最小变动单位
    """
    mindiff_dict = {}
    try:
        df = pd.read_csv(csv_path)

        if 'instrument' not in df.columns or 'mindiff' not in df.columns:
            raise ValueError("CSV文件必须包含 'instrument' 和 'mindiff' 列")

        for _, row in df.iterrows():
            mindiff_dict[row['instrument']] = float(row['mindiff'])

        return mindiff_dict
    except Exception as e:
        logger.error(f"加载mindiff数据失败: {str(e)}")
        return {}

class InstrumentProcessor:
    def __init__(self, instrument, k_line_types, instruments_mindiff, factor_json_path):
        """
        处理单个品种的因子计算
        :param instrument: 品种名称
        :param k_line_types: K线类型列表
        :param instruments_mindiff: 品种最小变动单位字典
        :param factor_json_path: 因子参数JSON文件路径
        """
        self.instrument = instrument
        self.k_line_types = k_line_types
        self.instruments_mindiff = instruments_mindiff
        self.factor_json_path = factor_json_path
        self.logger = configure_process_logger()
        self.data_cache = {}  # 按K线类型缓存数据

    def get_instrument_data(self, k_line_type):
        """获取品种数据，带缓存"""
        if k_line_type in self.data_cache:
            return self.data_cache[k_line_type]

        # 构建数据路径
        data_path = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            f'../data/{k_line_type}/{self.instrument}/{self.instrument}.csv'
        )

        self.logger.info(f"读取数据: {data_path}")
        if not os.path.exists(data_path):
            self.logger.warning(f"文件不存在: {data_path}")
            return None

        try:
            df = pd.read_csv(data_path)
            self.data_cache[k_line_type] = df
            return df
        except Exception as e:
            self.logger.error(f"读取文件失败: {data_path}, 错误: {e}")
            return None

    def calculate_factor_for_kline(self, k_line_type):
        """计算单个K线类型下的所有因子"""
        self.logger.info(f"开始处理 {self.instrument} 的 {k_line_type} K线")

        # 获取品种数据
        df = self.get_instrument_data(k_line_type)
        if df is None:
            return 0, 0  # 成功数, 失败数

        # 获取mindiff
        mindiff = self.instruments_mindiff.get(self.instrument)
        if mindiff is None:
            self.logger.warning(f"{self.instrument} 未设置最小变动单位")
            return 0, 0

        # 收集所有因子参数
        factor_params_list = list(iterate_factor_parameters(self.factor_json_path))
        total_factors = len(factor_params_list)
        completed = 0
        failed = 0

        self.logger.info(f"将在 {self.instrument}/{k_line_type} 上计算 {total_factors} 个因子")

        # 遍历所有因子
        for factor_params in factor_params_list:
            full_name = factor_params["full_name"]
            base_factor_name = factor_params["factor_name"]

            # 设置因子保存路径
            save_path = os.path.join(
                os.path.dirname(os.path.abspath(__file__)),
                f'../data/{k_line_type}/{self.instrument}/{full_name}.csv'
            )

            # 检查文件是否已存在
            if os.path.exists(save_path):
                completed += 1
                continue

            # 动态导入因子计算器
            calculator_class = get_factor_calculator(base_factor_name)
            if calculator_class is None:
                self.logger.warning(f"未找到因子计算器: {base_factor_name}")
                failed += 1
                continue

            # 创建参数字典
            param = {
                'df': df,
                'instrument': self.instrument,
                'k_line_type': k_line_type,
                'mindiff': mindiff,
                **{k: v for k, v in factor_params.items() if v is not None and k != "full_name"}
            }

            # 创建因子计算器实例
            calculator_instance = calculator_class()

            try:
                self.logger.info(f"计算中: {self.instrument} {full_name} {k_line_type}")

                # 计算因子
                result = calculator_instance.formula(param)

                # 保存结果
                os.makedirs(os.path.dirname(save_path), exist_ok=True)
                result.to_csv(save_path, index=False)

                self.logger.info(f"计算成功: {save_path}")
                completed += 1
            except Exception as e:
                self.logger.exception(f"计算失败: {save_path}, 错误: {e}")
                failed += 1

            # 定期报告进度
            if (completed + failed) % 10 == 0 or (completed + failed) == total_factors:
                progress = completed + failed
                self.logger.info(f"进度: {progress}/{total_factors} "
                                 f"({progress / total_factors:.1%}), "
                                 f"成功: {completed}, 失败: {failed}")

        self.logger.info(f"{self.instrument}/{k_line_type} 完成: "
                         f"总计 {total_factors}, 成功 {completed}, 失败 {failed}")
        return completed, failed

    def process_instrument(self):
        """处理单个品种的所有K线类型"""
        self.logger.info(f"开始处理品种: {self.instrument}")
        total_success = 0
        total_failed = 0

        for k_line_type in self.k_line_types:
            success, failed = self.calculate_factor_for_kline(k_line_type)
            total_success += success
            total_failed += failed

        self.logger.info(f"品种 {self.instrument} 处理完成: "
                         f"总计因子 {total_success + total_failed}, "
                         f"成功 {total_success}, 失败 {total_failed}")
        return total_success, total_failed

def run_instrument_processor(args):
    """包装函数用于进程池"""
    instrument, k_line_types, instruments_mindiff, factor_json_path = args
    processor = InstrumentProcessor(instrument, k_line_types, instruments_mindiff, factor_json_path)
    return processor.process_instrument()

if __name__ == "__main__":
    # 1. 配置参数
    script_dir = os.path.dirname(os.path.abspath(__file__))

    # 2. 加载最小变动单位数据
    mindiff_csv_path = os.path.join(script_dir, '../mindiff.csv')
    instruments_mindiff_dict = load_instruments_mindiff(mindiff_csv_path)

    if not instruments_mindiff_dict:
        logger.error("无法加载最小变动单位数据，程序退出")
        exit(1)

    # 3. 检查品种设置
    missing_instruments = [inst for inst in instruments if inst not in instruments_mindiff_dict]
    if missing_instruments:
        logger.warning(f"以下品种未设置最小变动单位: {', '.join(missing_instruments)}")

    # 4. 因子参数JSON文件路径
    factor_json_path = os.path.join(script_dir, 'factor_name.json')

    # 5. 准备进程池任务
    tasks = [
        (instrument, k_line_types, instruments_mindiff_dict, factor_json_path)
        for instrument in instruments
    ]

    total_tasks = len(tasks)
    logger.info(f"开始处理 {total_tasks} 个品种的因子计算")

    # 6. 使用多进程池
    # 使用spawn方法创建进程，避免fork导致的问题
    ctx = get_context('spawn')

    # 根据CPU核心数设置进程数，保留1个核心
    n_cores = max(1, os.cpu_count() - 1 or 1)

    with ctx.Pool(processes=n_cores) as pool:
        results = []
        future_to_instrument = {}

        # 提交所有任务
        for task in tasks:
            instrument = task[0]
            future = pool.apply_async(run_instrument_processor, (task,))
            future_to_instrument[future] = instrument

        # 处理结果
        total_success = 0
        total_failed = 0
        completed = 0

        for future in future_to_instrument:
            try:
                success, failed = future.get()
                instrument = future_to_instrument[future]
                total_success += success
                total_failed += failed
                completed += 1

                logger.info(f"品种 {instrument} 完成: 成功 {success}, 失败 {failed}")
                logger.info(f"总体进度: {completed}/{total_tasks} ({completed /total_tasks:.1%}), "
                            f"累计成功: {total_success}, 累计失败: {total_failed}")
            except Exception as e:
                logger.error(f"处理品种 {future_to_instrument[future]} 时出错: {str(e)}")
                completed += 1

    logger.info(f"所有品种处理完成: 总计因子 {total_success + total_failed}, "
                f"成功 {total_success}, 失败 {total_failed}")