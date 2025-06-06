from factor_cal.factor_cal import factor_calculator
import os
import csv
import multiprocessing
import pandas

# 从 config 中导入默认参数
from config import instruments
from config import k_line_types
from config import lengths

# 设置工作区绝对路径
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
mindiff_file_path = os.path.join(BASE_DIR, 'data', 'mindiff', 'mindiff.csv')
factor_name_file_path = os.path.join(BASE_DIR, 'factor_name.csv')

def run_one_instrument(instrument, k_line_type, length, instruments_mindiff, factor_name_file_path):
    print(f"Start: {instrument}, {k_line_type}, {length}")
    factor_names = pandas.read_csv(factor_name_file_path, skiprows=[0], comment='#')
    calculator = factor_calculator([instrument], [k_line_type], [length], instruments_mindiff, factor_names)
    calculator.factors_cal()
    print(f"Done: {instrument}, {k_line_type}, {length}")

def main():
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

    # 不再在主进程读取 factor_names

    # 利用进程池计算每个因子
    for k_line_type in k_line_types:
        print(f"Processing: {k_line_type}")
        pool = multiprocessing.Pool(processes=multiprocessing.cpu_count())
        results = []
        for instrument in instruments:
            for length in lengths:
                result = pool.apply_async(
                    run_one_instrument,
                    args=(instrument, k_line_type, length, instruments_mindiff, factor_name_file_path),
                )
                results.append(result)
        pool.close()
        pool.join()
        # 检查是否有异常
        for r in results:
            try:
                r.get(timeout=1)
            except Exception as e:
                print(f"Error in task: {e}")
        print(f"Finished: {k_line_type}")

if __name__ == '__main__':
    main()