# FCT_Support_Close_Thr_Boll_1：收盘价接近布林带下轨的次数因子，衡量收盘价在窗口内低于下轨的次数

import os

import numpy
import pandas

# 设置工作目录为当前脚本所在的目录
os.chdir(os.path.dirname(os.path.abspath(__file__)))


class FCT_Support_Close_Thr_Boll_1:
    def __init__(self):
        self.factor_name = 'FCT_Support_Close_Thr_Boll_1'

    def formula(self, param):
        # 从参数字典中读取 DataFrame
        df = param.get('df', None)
        if df is None:
            raise ValueError("no 'df' in param")

        # 从参数字典中读取 length
        length = param.get('length', None)
        if length is None:
            raise ValueError("param missing 'length'")

        # 从参数字典中读取 n_std（布林带标准差倍数）
        n_std = param.get('n_std', None)
        if n_std is None:
            raise ValueError("param missing 'n_std'")

        # 从参数字典中读取 factor_name
        factor_name = param.get('factor_name', None)
        if factor_name is None:
            raise ValueError("param missing 'factor_name'")

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
        new_columns[f'{factor_name}'] = count_array

        # 一次性合并到原始 df
        df = pandas.concat([df, new_columns], axis=1)

        # 返回结果（无日期）
        result = df[[f'{factor_name}']].copy()
        return result
