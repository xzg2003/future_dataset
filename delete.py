# 删除期货因子的代码，万一大家算出来的因子有问题可以删了重新算
import os
import csv

from config import instruments
from config import k_line_types

FACTOR_NAME_FILE = './factor_name.csv'

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

def get_factor_file_names(factor_name):
    """
    根据因子名称生成对应的文件名模式。
    某些因子可能有多个衍生文件
    :param factor_name:需要处理的因子名称
    :return:返回一个处理好的名称
    """
    base_name = factor_name.split('@')[0]
    return [
        f"{base_name}@{i}" if '@' in factor_name else base_name
        for i in range(1)   # 这里可以调节，如果有多个版本可以进行处理
    ]

def match_factors(input_name, all_factors):
    """
    模糊匹配因子名称，支持前缀匹配
    :param input_name: 需要模糊匹配的因子名称
    :param all_factors: 全体因子名称
    :return: 返回一个匹配好的因子名
    """
    matched = [f for f in all_factors if f.startwith(input_name)]
    if not matched:
        print(f"未找到以'{input_name}'开头的因子")
    return matched

def delete_factor(k_line, factor_files):
    for name in factor_files:
        # 对文件名称加 .csv 后缀
        name_csv = name if name.endswith('.csv') else name + '.csv'
        deleted = False
        for instrument in instruments:
            file_path = f'./data/{k_line}/{instrument}/{name_csv}'
            if os.path.exists(file_path):
                os.remove(file_path)
                print(f'已删除：{file_path}')
                deleted = True

        if not deleted:
            print(f'{name} 在 {k_line} 下未找到对应文件')

if __name__ == '__main__':
    # 读取所有因子名称
    factor_names = read_single_column(FACTOR_NAME_FILE)

    print("支持的因子名称：", ', '.join(factor_names[:5]) + "...（共{}个）".format(len(factor_names)))

    k_lines = k_line_types

    """
    主循环，允许用户删除多个因子计算结果，用户输入0以结束程序
    """
    while True:
        factor_input = input("请输入需要删除的因子名称，输入0以结束程序，输入all删除所有因子：")
        if factor_input == '0':
            print("程序结束。")
            break
        elif factor_input == 'all':
            confirm = input("确定要删除所有因子吗？此操作不可恢复，输入yes确认：")
            if confirm.lower() == 'yes':
                    matched_factors = factor_names
            else:
                print("已取消全部删除操作。")
                continue
        else:
            # 模糊因子匹配名称
            matched_factors = match_factors(factor_input, factor_names)
            if not matched_factors:
                continue

        print(f"将删除以下因子：{', '.join(matched_factors)}")

        for factor in matched_factors:
            factor_files = [factor]
            for k_line in k_lines:
                delete_factor(k_line, factor_files)

        print("删除完成。")
