from factor_cal.factor_cal import factor_calculator
import os
import csv

# 设置工作区相对路径
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# 最小变化单位文件路径
mindiff_file_path = './data/mindiff/mindiff.csv'

def main():
    """
    各个参数的设置，
    instruments:    期货品种
    k_line_type:    k线类型
    lengths:        滑动平均长度
    mindiff:        最小变化单位
    """

    instruments = ['A','AG','AL','AP','AU','BU','C','CF','CJ','CS',
                   'CU','EB','EG','FG','FU','HC','I','IC','IF','IH',
                   'J','JD','JM','L','LU','LH','M','MA','NI','OI','P',
                   'PB','PF','PG','PK','PP','RB','RM','RU','SA','SF',
                   'SM','SN','SP','SR','SC','SS','TA','T','TF','UR','V','Y','ZN']
    # instruments = ['A']
    k_line_type = '5m'
    lengths = [10, 20, 40, 80, 120, 180]

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