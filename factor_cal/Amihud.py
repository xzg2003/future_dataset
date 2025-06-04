#Amihud 流动性因子计算 （每日收盘价百分比变化绝对值/成交量）的滚动平均值

import pandas as pd
import numpy as np

class Amihud:
    def __init__(self):
        pass

    def formula(self, param):
        # 从字典中提取 DataFrame
        df = param.get('df', None)
        length = param.get('length', 5)
        factor_name = f'Amihud@{length}'

        if df is None:
            raise ValueError("参数 'param' 中缺少 'df' 键或其值为空")

        # 确保 df 是 pandas.DataFrame 类型
        if not isinstance(df, pd.DataFrame):
            raise TypeError("'df' 必须是 pandas.DataFrame 类型")

        # 计算每日收益率
        df['return'] = df['close'].pct_change()

        # 计算 Amihud 流动性因子
        df[factor_name] = (np.abs(df['return']) / df['volume']).rolling(window=length).mean()

        # 返回结果
        if 'datetime' in df.columns:
            df = df.rename(columns={'datetime': 'date'})
        result = df[['date', factor_name]].copy()
        return result
