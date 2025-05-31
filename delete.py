# 删除期货因子的代码，万一大家算出来的因子有问题可以删了重新算
import os

from multipart import file_path
from sympy.matrices.expressions.matmul import factor_in_front

from config import instruments
from config import factor_names
from config import lengths
from config import factor_categories
from config import default_data
from config import k_line_type

def get_factor_file_names(factor_name):
    file_names = []

    for length in lengths:
        if factor_name in factor_categories.get("no_length", []):
            file_names.append(f"{factor_name}")
            break  # 只生成一次
        elif factor_name in factor_categories.get("short_long", []):
            file_names.append(f"{factor_name}@{default_data['short']}_{default_data['long']}")
            break
        elif factor_name in factor_categories.get("length_thr", []):
            file_names.append(f"{factor_name}@{length}_{default_data['thr']}")
        elif factor_name in factor_categories.get("length_atr", []):
            file_names.append(f"{factor_name}@{length}_{default_data['atr_length']}")
        elif factor_name in factor_categories.get("length_n_std", []):
            file_names.append(f"{factor_name}@{length}_{default_data['n_std']}")
        elif factor_name in factor_categories.get("short_long_atr", []):
            file_names.append(f"{factor_name}@{default_data['short']}_{default_data['long']}_{default_data['atr_length']}")
            break
        elif factor_name in factor_categories.get("short_long_vol", []):
            file_names.append(f"{factor_name}@{default_data['short']}_{default_data['long']}_{default_data['vol_length']}")
            break
        else:
            file_names.append(f"{factor_name}@{length}")

    return file_names

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
    k_lines = k_line_type

    """
    主循环，允许用户删除多个因子计算结果，用户输入0以结束程序
    """
    while True:
        factor_input = input("请输入需要删除的因子名称，输入0以结束程序：")
        if factor_input =='0':
            print("程序结束。")
            break
        if factor_input not in factor_names:
            print("因子名称不存在，请重新输入。")
            continue

        factor_files = get_factor_file_names(factor_input)

        for k_line in k_lines:
            delete_factor(k_line, factor_files)