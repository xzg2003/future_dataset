import matplotlib.pyplot as plt
import pandas as pd
import os

from setuptools.sandbox import save_path

# 设置相对路径
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# 设置期货类型列表
instruments = ['A', 'AG', 'AL', 'AP', 'AU', 'BU', 'C', 'CF', 'CJ', 'CS',
               'CU', 'EB', 'EG', 'FG', 'FU', 'HC', 'I', 'IC', 'IF', 'IH',
               'J', 'JD', 'JM', 'L', 'LU', 'LH', 'M', 'MA', 'NI', 'OI', 'P',
               'PB', 'PF', 'PG', 'PK', 'PP', 'RB', 'RM', 'RU', 'SA', 'SF',
               'SM', 'SN', 'SP', 'SR', 'SC', 'SS', 'TA', 'T', 'TF', 'UR', 'V', 'Y', 'ZN']

# 设置因子类型的列表
factors = ['FCT_Ac_Tr_1']

# 设置滑动长度的列表
lengths = [10]

# 设置k线类型的列表
k_line_type = '5m'

# 用于存储全部数据的列表、
all_data = []

for instrument in instruments:
    for factor in factors:
        for length in lengths:
            # 设置文件读取路径，并读取其中的数据
            data_path = f'../data/5m/{instrument}/{factor}@{length}.csv'
            df = pd.read_csv(data_path)
            try:
                if os.path.exists(data_path):
                    df = pd.read_csv(data_path)
                    df = df.dropna()    # 删除空数据点
                    all_data.append(df[f'{factor}'])
            except Exception as e:
                print(f"Error：{e}")

if all_data:
    # 合并所有数据
    merged_df = pd.concat(all_data, ignore_index=True)

    # 修改列的名称
    if isinstance(merged_df, pd.DataFrame):
        column_mapping = {'FCT_Ac_Tr_1': 'FCT_Ac_Tr_1@10'}
        merged_df = merged_df.rename(columns='FCT_Ac_Tr_1@10')
    else:
        merged_df = merged_df.rename('FCT_Ac_Tr_1@10')

    # 设置存储路径
    save_path = f'../data/merge/{k_line_type}/{factor}@{length}.csv'

    # 利用os.makedirs设置一个路径
    os.makedirs(os.path.dirname(save_path), exist_ok=True)

    # 保存合并后的数据
    merged_df.to_csv(save_path, index=False)
    print(f"success to {save_path}")
else:
    print("no valid data")



