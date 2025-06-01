# 建立数据库
import os
import pandas as pd
from config import *
import numpy as np


class factor_judge():
    def __init__(self, factor, k_line):
        self.name = factor
        self.k_line = k_line
        self.df = {}

        if not os.path.exists(f'./result/{k_line}/{self.name}'):
            os.makedirs(f'./result/{k_line}/{self.name}')

        # 提前读取每种期货的因子值并存储
        for i in instruments:
            if os.path.exists(f'./data/{k_line}/{i}/{self.name}.csv'):
                df = pd.read_csv(f'./data/{k_line}/{i}/{self.name}.csv', encoding='utf-8')
                df = df.replace([np.inf, -np.inf], np.nan)
                df1 = pd.read_csv(f'./data/{k_line}/{i}/{i}.csv', encoding='utf-8')
                # 支持更多K线类型
                if k_line == '5m':
                    shift_n = 24
                elif k_line == '1d':
                    shift_n = 1
                else:
                    # 可根据实际情况补充其它周期
                    shift_n = 1
                df['yield'] = (df1['open'].shift(-shift_n) - df1['open']) / df1['open']
                self.df[i] = df