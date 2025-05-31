from factor_cal.factor_cal import factor_calculator
import os
import csv

# 从 config 中导入默认参数
from config import instruments
from config import k_line_type
from config import lengths

# 设置工作区相对路径
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# 最小变化单位文件路径
mindiff_file_path = './data/mindiff/mindiff.csv'

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

    # 创建因子计算器实例，以调用内部的函数
    calculator = factor_calculator(instruments, k_line_type, lengths, instruments_mindiff)

    # 调用计算函数
    calculator.factors_cal()

if __name__ == '__main__':
    main()