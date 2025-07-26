
import os
import csv
import json
import pandas as pd
import concurrent.futures
import logging
import importlib
import multiprocessing
from config import *
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
                    "factor_name": config["factor_name"],
                    "factor_kind": base_factor_name,  # 使用基础因子名称
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

def load_instruments_mindiff():
    """
    从CSV文件加载品种的最小变动单位
    """
    instrument_mindiff = {}
    try:
        df = pd.read_csv('mindiff.csv')

        if 'instrument' not in df.columns or 'mindiff' not in df.columns:
            raise ValueError("CSV文件必须包含 'instrument' 和 'mindiff' 列")

        for _, row in df.iterrows():
            instrument_mindiff[row['instrument']] = float(row['mindiff'])
        
        return instrument_mindiff
    
    except Exception as e:
        logger.error(f"加载mindiff数据失败: {str(e)}")
        return {}

def get_factor_data(k_line_type,instrument,factor_name):
    """获取已有因子数据"""
    data_path = f'{DATA_DIR}/{k_line_type}/{instrument}/{factor_name}.csv'
    logger.info(f"读取数据: {data_path}")
    if not os.path.exists(data_path):
        logger.warning(f"文件不存在: {data_path}")
        return None

    try:
        df = pd.read_csv(data_path)
    except Exception as e:
        logger.error(f"读取文件失败: {data_path}, 错误: {e}")
        return None
    
    return df

def run_one_instrument(args):
    """
    运行单个品种的因子计算
    :param instrument: 品种名称
    :param k_line_types: K线类型列表
    :param instruments_mindff: 品种最小变动单位字典
    :param factor_params: 因子参数JSON文件内容
    """
    """计算单个K线类型下的所有因子"""
    instrument, k_line_type, factor_params, instruments_mindiff = args
    logger.info(f"开始处理 {instrument} 的 {k_line_type} K线")
    factor_name = factor_params["factor_name"]
    base_factor_name = factor_params["factor_kind"]

    # 动态导入因子计算器
    factor_calculator = get_factor_calculator(base_factor_name)
    if factor_calculator is None:
        logger.warning(f"未找到因子计算器: {base_factor_name}")
        return 0, 0

    # 设置因子保存路径
    save_path = f'{DATA_DIR}/{k_line_type}/{instrument}/{factor_name}.csv'

    # 获取mindiff
    mindiff = instruments_mindiff[instrument]
    if mindiff is None:
        logger.warning(f"{instrument} 未设置最小变动单位")
        return 0, 0

    # 收集所有因子参数
    total_factors = len(factor_params)
    completed = 0
    failed = 0

    # 创建参数字典
    param = {
        'df': get_factor_data(k_line_type, instrument, instrument),
        'instrument': instrument,
        'k_line_type': k_line_type,
        'mindiff': mindiff,
        **{k: v for k, v in factor_params.items() if v is not None}
    }

    # 将需要使用的已有因子计算结果添加到param中
    for key, value in param.items():
        if type(value) is str and value == 'Need':
            param[key] = get_factor_data(k_line_type, instrument, key)

    # 创建因子计算器实例
    calculator_instance = factor_calculator()

    try:
        logger.info(f"计算中: {instrument} {factor_name} {k_line_type}")

        # 计算因子
        result = calculator_instance.formula(param)

        # 保存结果
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        result.to_csv(save_path, index=False)

        logger.info(f"计算成功: {save_path}")
        completed += 1
    except Exception as e:
        logger.exception(f"计算失败: {save_path}, 错误: {e}")
        failed += 1

    return completed, failed
    
if __name__ == "__main__":
    # 加载最小变动单位
    instrument_mindiff = load_instruments_mindiff()
    if not instrument_mindiff:
        logger.error("无法加载最小变动单位数据，程序退出")
        exit(1)

    # 检查品种设置
    missing_instruments = [inst for inst in instruments if inst not in instrument_mindiff]
    if missing_instruments:
        logger.warning(f"以下品种未设置最小变动单位: {', '.join(missing_instruments)}")

    # 因子参数JSON文件路径
    factor_json_path = './factor_cal/factor_name.json'

    # 遍历所有因子
    factor_params_list = list(iterate_factor_parameters(factor_json_path))
    for factor_params in factor_params_list:
        # 准备进程池任务，固定因子参数，对品种进行多线程计算
        tasks = [
            (instrument, k_line_type, factor_params, instrument_mindiff)
            for instrument in instruments
        ]

        total_tasks = len(tasks)
        logger.info(f"开始处理 {total_tasks} 个品种的因子计算")
        
        # 单进程调试
        #for task in tasks:
        #    run_one_instrument(task)
        # 使用spawn方法创建进程，避免fork导致的问题
        ctx = multiprocessing.get_context('spawn')

        # 根据CPU核心数设置进程数，保留1个核心
        n_cores = max(1, os.cpu_count() - 1 or 1)

        with ctx.Pool(processes=n_cores) as pool:
            # 提交所有任务
            for task in tasks:
                pool.apply_async(run_one_instrument, (task,))

            pool.close()
            pool.join()
        