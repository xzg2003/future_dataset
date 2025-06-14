from factor_cal.factor_cal import factor_calculator
import os
import csv
import multiprocessing

# 从 config 中导入默认参数
from config import instruments
from config import k_line_types

# 设置工作区相对路径
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# 最小变化单位文件路径
mindiff_file_path = './data/mindiff/mindiff.csv'

def run_one_instrument(instrument, k_line_type, instruments_mindiff):
    try:
        calculator = factor_calculator([instrument], [k_line_type], instruments_mindiff)
        calculator.factors_cal()
    except Exception as e:
        print(f"Error processing {instrument}, {k_line_type} : {e}")

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

    '''
    # 单进程处理每个因子
    for k_line_type in k_line_types:
        print(f"Processing: {k_line_type}")

        for instrument in instruments:
            for length in lengths:
                run_one_instrument(instrument, k_line_type, instruments_mindiff)

        print(f"Finished: {k_line_type}")
    '''

    # 利用进程池计算每个因子
    for k_line_type in k_line_types:
        print(f"Processing: {k_line_type}")
        pool = multiprocessing.Pool(processes=multiprocessing.cpu_count())

        for instrument in instruments:
            pool.apply_async(run_one_instrument, args=(instrument, k_line_type, instruments_mindiff))
        pool.close()
        pool.join()
        print(f"Finished: {k_line_type}")

if __name__ == '__main__':
    main()