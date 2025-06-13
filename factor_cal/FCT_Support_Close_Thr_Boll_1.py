# FCT_Support_Close_Thr_Boll_1：收盘价接近布林带下轨的次数因子，衡量收盘价在窗口内低于下轨的次数

import pandas
import numpy
import os

# 设置工作目录为当前脚本所在的目录
os.chdir(os.path.dirname(os.path.abspath(__file__)))

class FCT_Support_Close_Thr_Boll_1:
    def __init__(self):
        self.factor_name = 'FCT_Support_Close_Thr_Boll_1'

    def formula(self, param):
        # 从字典中提取 DataFrame
        df = param.get('df', None)
        if df is None:
            raise ValueError("no 'df' in param")
        if not isinstance(df, pandas.DataFrame):
            raise TypeError("df must be DataFrame")

        # 从字典中读取 length 和 n_std（布林带标准差倍数，默认为2）
        length = param.get('length', None)
        n_std  = param.get('n_std', 2)
        if length is None:
            raise ValueError("param missing 'length'")
        print(f"Using length: {length}, n_std: {n_std}")

        """
        # 计算布林带下轨
        ma = df['close'].rolling(window=length).mean()
        std = df['close'].rolling(window=length).std()
        lower_band = ma - n_std * std

        # 统计每个窗口内收盘价低于下轨的次数
        def count_below_lower(x, lower):
            return numpy.sum(x <= lower)

        counts = []
        closes = df['close'].values
        lowers = lower_band.values
        for i in range(len(df)):
            if i < length - 1:
                counts.append(numpy.nan)
            else:
                window_close = closes[i - length + 1 : i + 1]
                window_lower = lowers[i - length + 1 : i + 1]
                counts.append(numpy.sum(window_close <= window_lower))
        df[f'FCT_Support_Close_Thr_Boll_1@{length}'] = counts
        """

        # 初始化 new_columns 用于集中管理新增列
        new_columns = pandas.DataFrame(index=df.index)

        # 计算布林带下轨
        ma = df['close'].rolling(window=length).mean()
        std = df['close'].rolling(window=length).std()
        lower_band = ma - n_std * std

        # 预分配数组存储计数结果
        count_array = numpy.empty(len(df), dtype=float)
        count_array[:] = numpy.nan  # 初始化为 NaN

        closes = df['close'].values
        lowers = lower_band.values

        # 向量化填充计数结果
        for i in range(length - 1, len(df)):
            window_close = closes[i - length + 1:i + 1]
            window_lower = lowers[i - length + 1:i + 1]
            count_array[i] = numpy.sum(window_close <= window_lower)

        # 写入 new_columns
        new_columns[f'FCT_Support_Close_Thr_Boll_1@{length}'] = count_array

        # 一次性合并到原始 df
        df = pandas.concat([df, new_columns], axis=1)

        # 返回结果
        if 'datetime' in df.columns:
            df = df.rename(columns={'datetime': 'date'})
        result = df[['date', f'FCT_Support_Close_Thr_Boll_1@{length}']].copy()
        return result