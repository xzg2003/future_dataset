# 乖离率除以TR去量纲

import pandas
import numpy

class FCT_Bias_1:
    def __init__(self):
        self.fact_name = 'FCT_Bias_1'

    def formula(self, param):
        # 从字典中提取 DataFrame
        df = param.get('df', None)
        if df is None:
            raise ValueError("no 'df' in param")

        # 确保 df 是 pandas.DataFrame 类型
        if not isinstance(df, pandas.DataFrame):
            raise TypeError("df must be DataFrame")

        """
        从字典中读取 length
        获取 instrument 名称，用于提取mindiff中的数据
        """
        length = param.get('length', None)
        if length is None:
            raise ValueError("param missing 'length'")
        print(f"Using length: {length}")

        # 获取instrument
        instrument = param.get('instrument', None)
        if instrument is None:
            raise ValueError("param miss instrument")

        # 获取mindiff
        mindiff = param.get('mindiff', None)
        if mindiff is None:
            raise ValueError(f"param miss mindiff for instrument: {param.get('instrument', 'unknown')}")
        print(f"Using mindiff: {mindiff}")

        # 计算震荡指标（这里直接照搬了前面Tr的计算代码）
        # 前一k线的收盘价
        df['close_pre'] = df['close'].shift(1)

        # 逐行取三种差值的最大值作为 TR
        df['Tr'] = df[['close_pre', 'high', 'low']].apply(
            lambda row: max(row['high'] - row['close_pre'], row['high'] - row['low'], row['close_pre'] - row['low']),
            axis=1
        )

        """
        # 计算因子，缺失mindiff，故这个函数是没有比较的
        df[f'FCT_Bias_1@{length}'] = (df['close'] - df['close'].rolling(window=length).mean()) / df['Tr'].rolling(window=length).mean()
        """

        # 计算 Tr 的滚动均值并处理NaN
        rolling_mean_Tr = df['Tr'].rolling(window=length).mean().fillna(0)

        # 计算收盘价的滚动均值
        rolling_mean_close = df['close'].rolling(window=length).mean().fillna(0)

        # 正确的计算函数
        df[f'FCT_Bias_1@{length}'] = numpy.where(
            rolling_mean_Tr < mindiff,
            0,
            (df['close'] - rolling_mean_close) / rolling_mean_Tr
        )

        # 返回结果
        result = df[['datetime', f'FCT_Bias_1@{length}']].copy()
        return result

