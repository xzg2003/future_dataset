# 计算因子之间的相关系数
import os
import sys
sys.path.append('.')
from config import *
import pandas as pd
class mutal_IC():
    def __init__(self, k_line):
        self.df = {}
        self.k_line = k_line

        # 提前读取每种期货的因子值并存储
        for factor in factors:
            df_combined = []
            if not os.path.exists(f'./result/{self.k_line}'):
                os.makedirs(f'./result/{self.k_line}')

            for i in instruments:
                if os.path.exists(f'{DATA_DIR}/{k_line}/{i}/{factor}.csv'):
                    df = pd.read_csv(f'{DATA_DIR}/{k_line}/{i}/{factor}.csv',encoding='utf-8')
                    df_combined.append(df)

            df_combined = pd.concat(df_combined,axis=0,ignore_index=True)
            self.df[factor] = df_combined 

    def cal_mutal_IC(self):
        # 存储划分后的 DataFrame
        # 列表每一行存储相同层数下所有期货品种的表格
        df = pd.DataFrame()
        for i,value in self.df.items():
            df[i] = value[i]
        df.corr(method='pearson').to_csv(f'./result/{self.k_line}/mutal_IC.csv',index=True,encoding='utf-8')
