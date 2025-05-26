from factor_judge.factor_judge import factor_judge
import scipy.stats as st
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import os
import csv
import numpy as np
import pandas as pd
from config import *
import warnings

warnings.filterwarnings("ignore")


def get_avg(data):
    # 排序列表
    data_sorted = np.sort(data)

    # 计算前 10% 和后 10% 元素的数量
    n = len(data_sorted)
    first_10_percent = n // 10
    last_10_percent = n - first_10_percent

    # 提取前 10% 和后 10% 的数据
    first_10_values = data_sorted[:first_10_percent]
    last_10_values = data_sorted[last_10_percent:]

    # 计算平均值
    first_10_avg = np.mean(first_10_values) if len(first_10_values) > 0 else 0
    last_10_avg = np.mean(last_10_values) if len(last_10_values) > 0 else 0

    return last_10_avg, first_10_avg


class statistic(factor_judge):
    def __init__(self, factor, method, k_line):
        # 调用父类 factor_judge 的构造函数
        super().__init__(factor, k_line)
        self.method = method  # 分割方法

        # 初始化 statistic 类的特有属性
        self.results = {
            '因子名称': [self.name],
            '分割方法': [self.method],
            '因子方向': [],
            '25分位数': [],
            '50分位数': [],
            '75分位数': [],
            '因子值平均数': [],
            '偏度': [],
            '峰度': [],
            '标准差': [],
        }

    # 信号方向计算
    def diverse(self):
        # 将不同品种合并
        df_combined = []
        for i in instruments:
            if i in self.df.keys():
                df = self.df[i].copy()
            else:
                continue
            df_combined.append(df)
        if not df_combined:
            # 没有数据可以拼接，返回空的 DataFrame 或raise异常或直接return
            return pd.DataFrame()
        df_combined = pd.concat(df_combined, axis=0, ignore_index=True)

        # 计算皮尔逊系数
        corr = df_combined.loc[:, [self.name, 'yield']].corr(method='pearson').loc[self.name, 'yield']

        # 定义信号方向
        if corr > 0:
            self.div = 1
        else:
            self.div = -1

        factor = df_combined[self.name].dropna()
        p25 = round(np.quantile(factor, 0.25), 4)  # 上四分位数
        p50 = round(np.quantile(factor, 0.5), 4)  # 中四分位数
        p75 = round(np.quantile(factor, 0.75), 4)  # 下四分位数
        mean = round(np.mean(factor), 4)  # 计算平均数
        skew = round(st.skew(factor), 4)  # 计算偏度
        kurtosis = round(st.kurtosis(factor), 4)  # 计算峰度
        std = round(np.std(factor), 4)  # 计算标准差

        self.results['因子方向'].append(self.div)
        self.results['25分位数'].append(p25)
        self.results['50分位数'].append(p50)
        self.results['75分位数'].append(p75)
        self.results['因子值平均数'].append(mean)
        self.results['偏度'].append(skew)
        self.results['峰度'].append(kurtosis)
        self.results['标准差'].append(std)

        if not os.path.exists(f'./result/{self.k_line}{self.name}/{self.name}.png'):
            plt.rcParams['font.sans-serif'] = ['SimHei']
            plt.rcParams['axes.unicode_minus'] = False
            plt.figure(figsize=(10, 6))
            plt.xlabel('因子值')
            plt.ylabel('频数')
            plt.title(f'{self.name}')
            lower = factor.quantile(0.001)
            upper = factor.quantile(0.999)
            # mask = ~((factor < lower) | (df > upper))
            # factor = factor[mask]
            factor = factor.apply(lambda x: np.nan if x <= lower or x >= upper else x)
            # factor = factor.dropna()
            plt.hist(factor, bins=100, color='skyblue', edgecolor='black')
            plt.savefig(f'./result/{self.k_line}/{self.name}/{self.name}.png')
            plt.close()

    def month(self):
        self.IC = {}  # 存放每个月所有品种的IC
        self.ratio = {}  # 存放每个月所有品种的盈亏比

        for i in instruments:
            # 按月份分割
            if i in self.df.keys():
                df = self.df[i].copy()
            else:
                continue
            if 'datetime' in df.columns:
                df.rename(columns={'datetime': 'date'}, inplace=True)
            df['date'] = pd.to_datetime(df['date'])
            df.set_index('date', inplace=True)
            monthly_groups = df.resample(f'{self.method}E')

            # 遍历每个月份的数据
            for month, group in monthly_groups:
                # 计算皮尔逊系数，并按月份保存
                if len(group) > 1:
                    corr = group.loc[:, [self.name, 'yield']].corr(method='pearson').loc[self.name, 'yield']
                    if np.isnan(corr):
                        continue
                    if str(month) in self.IC:
                        self.IC[str(month)].append(corr)
                    else:
                        self.IC[str(month)] = [corr]

                    # 计算盈亏比，并按月份保存
                    # scaler = StandardScaler()
                    group.loc[:, 'signal'] = (group[self.name] - group[self.name].mean()) / group[
                        self.name].std()  # 规范化
                    # group.loc[:,'signal']=np.select([group['signal']>0,group['signal']<0],[1,-1]) # 生成交易信号
                    # 计算收益率的时候第一天存放的实际上是第三天相对于第二天的收益率
                    # 第一天生成的交易信号要到第三天才能做出交易
                    # 故直接相乘即可
                    group.loc[:, 'daily_yield'] = (group['yield'] * group['signal']).fillna(0)
                    profit = sum([x for x in group['daily_yield'] if x > 0])  # 累计收益
                    loss = abs(sum([x for x in group['daily_yield'] if x < 0]))  # 累计亏损
                    ratio = 10
                    if self.div == 1 and loss > 0:
                        ratio = profit / loss
                    elif self.div == -1 and profit > 0:
                        ratio = loss / profit

                    if str(month) in self.ratio:
                        self.ratio[str(month)].append(ratio)
                    else:
                        self.ratio[str(month)] = [ratio]

        # 将每个月的数据取平均

    def save_month_result(self):
        # 打开 CSV 文件，模式为写入 ('w')
        with open(f'./result/{self.k_line}/{self.name}/{self.name}.csv', 'w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=self.results.keys())

            # 写入列名
            writer.writeheader()

            # 将数据按行写入
            max_len = max(len(v) for v in self.results.values())
            for i in range(max_len):  # 假设所有列表长度相同
                row = {key: self.results[key][i] if i < len(self.results[key]) else None for key in self.results}
                writer.writerow(row)

    def get_result(self):
        self.diverse()
        self.month()
        self.month_IC = {}  # 存放每个月平均的IC
        self.ICIR = {}  # 存放每个月的ICIR
        self.hit_ratio = {}  # 存放每个月的命中率
        self.month_ratio = {}  # 存放每个月平均的盈亏比
        result = {}  # 存放结果

        for key, value in self.IC.items():
            self.month_IC[key] = np.mean(value)
            self.ICIR[key] = self.month_IC[key] / np.var(value, ddof=0) if np.var(value, ddof=0) > 0 else 0
            self.hit_ratio[key] = np.mean(np.array(value) > 0)
        # print(self.ICIR)
        for key, value in self.ratio.items():
            self.month_ratio[key] = np.mean(value)

        result['平均IC'] = np.mean(list(self.month_IC.values()))
        result['平均IC前10%的均值'], result['平均IC后10%的均值'] = get_avg(list(self.month_IC.values()))
        result['平均ICIR'] = np.mean(list(self.ICIR.values()))
        result['平均命中率'] = np.mean(list(self.hit_ratio.values()))
        result['平均盈亏比'] = np.mean(list(self.month_ratio.values()))
        result['平均盈亏比前10%的均值'], result['平均盈亏比后10%的均值'] = \
            get_avg(list(self.month_ratio.values()))
        return result