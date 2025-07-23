# TrendStrength: 趋势系数因子，衡量价格序列的趋势强度（如线性回归斜率/标准差）

import pandas
import numpy
import os
from scipy.stats import linregress

# 设置工作目录为当前脚本所在的目录
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# 设置工作目录为当前脚本所在的目录
os.chdir(os.path.dirname(os.path.abspath(__file__)))

class TrendStrength:
    def __init__(self):
        self.factor_name = 'TrendStrength'

    def formula(self, param):
        # 从字典中提取 DataFrame
        df = param.get('df', None)
        if df is None:
            raise ValueError("no 'df' in param")
        if not isinstance(df, pandas.DataFrame):
            raise TypeError("df must be DataFrame")

        # 从字典中读取 length
        length = param.get('length', None)
        if length is None:
            raise ValueError("param missing 'length'")
        print(f"Using length: {length}")

        # 提取 close 数据为 NumPy 数组
        close_array = df['close'].values

        # 预分配趋势强度数组
        trend_strength_array = numpy.full(len(close_array), numpy.nan, dtype=numpy.float32)

        # 构造 x 轴（窗口内的索引）
        x = numpy.arange(length, dtype=numpy.float32)
        x_mean = x.mean()

        # 滑动窗口计算趋势强度
        for i in range(length - 1, len(close_array)):
            y = close_array[i - length + 1:i + 1]
            y_mean = y.mean()

            # 手动计算协方差和方差（可选替代 linregress）
            covariance = numpy.sum((x - x_mean) * (y - y_mean))
            variance = numpy.sum((x - x_mean) ** 2)
            slope = covariance / (variance + 1e-10)

            std = numpy.std(y)
            trend_strength_array[i] = slope / (std + 1e-10)

        # 构造新列 Series
        col_name = f'{self.factor_name}@{length}'
        new_column = pandas.Series(trend_strength_array, index=df.index, name=col_name)

        # 使用 assign 添加新列，避免 concat，减少内存碎片
        df = df.assign(**{col_name: new_column})

        # 返回结果
        if 'datetime' in df.columns:
            df = df.rename(columns={'datetime': 'date'})
        result = df[['date', f'TrendStrength@{length}']].copy()
        return result