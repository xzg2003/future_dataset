# 建立数据库
import os
import pandas as pd
from config import *
import numpy as np
import matplotlib.pyplot as plt
# 自适应分位数切割函数
# 该函数根据数据密度自适应调整分位数边界
def adaptive_quantile_cutoff(data, density_threshold=0.2, max_iter=10000):
    if len(data) == 0:
        return 0,0
    
    initial_length = len(data)
    lower, upper = np.percentile(data, [0.1, 99.9])  # 初始分位数
    for _ in range(max_iter):
        mask = (data >= lower) & (data <= upper)
        data = data[mask]
        
        # 如果子集长度小于初始长度的80%，则停止迭代
        if len(data)/initial_length < 0.8:
            break

        # 计算区间内数据密度
        hist, edges = np.histogram(data, bins=100)
        density = hist / hist.max()
        
        # 检查是否有低密度区域
        if np.min(density) > density_threshold:
            break
            
        # 调整分位数边界
        if len(data) > 0:
            upper = np.percentile(data, 99.9)
            lower = np.percentile(data, 0.1)

    return lower, upper

class factor_judge():
    def __init__(self, factor, k_line):
        self.name = factor
        self.k_line = k_line
        self.df = {}
        
        if not os.path.exists(f'./result/{k_line}/{self.name}'):
            os.makedirs(f'./result/{k_line}/{self.name}')

        # 提前读取每种期货的因子值并存储
        for i in instruments:
            if os.path.exists(f'{DATA_DIR}/{k_line}/{i}/{self.name}.csv'):
                df = pd.read_csv(f'{DATA_DIR}/{k_line}/{i}/{i}.csv',encoding='utf-8')
                df1 = pd.read_csv(f'{DATA_DIR}/{k_line}/{i}/{self.name}.csv',encoding='utf-8')
                df1 = df1.replace([np.inf, -np.inf], np.nan)
                df[self.name] = df1[self.name]
                if k_line == '5m':
                    df['yield'] = (df['open'].shift(-24)-df['open'])/df['open']
                elif k_line == '1d':
                    df['yield'] = (df['open'].shift(-1)-df['open'])/df['open']
                lower, upper = adaptive_quantile_cutoff((df[self.name].dropna()).values)
                df = df[(df[self.name] >= lower) & (df[self.name] <= upper)]
                self.df[i] = df

if __name__ == "__main__":
    # 测试因子判断类
    factor = 'FCT_Ac_Tr_1'
    k_line = '1d'
    judge = factor_judge(factor, k_line)
    df_combined = []
    for i in instruments:
        if i in judge.df.keys():
            df = judge.df[i].copy()
        else:
            continue
        df_combined.append(df)

    df_combined = pd.concat(df_combined, axis=0, ignore_index=True)
    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.rcParams['axes.unicode_minus'] = False
    plt.figure(figsize=(10, 6))
    plt.xlabel('因子值')
    plt.ylabel('频数')
    plt.title(f'{factor}')
    plt.hist(df_combined[factor], bins=100, color='skyblue', edgecolor='black')
    #plt.show()
    plt.close() 