# 乖离率除以TR去量纲

import pandas
import numpy
import os

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

        # 判断 Tr.csv 文件是否存在，用于调用
        tr_data_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), f'../data/5m/{instrument}/Tr.csv')
        if not os.path.exists(tr_data_path):
            raise FileNotFoundError(F"Tr file not found:{tr_data_path}")

        tr_df = pandas.read_csv(tr_data_path)
        # Tr.csv 有 datetime 和 Tr 两列，且与主 df 按 datetime 对齐
        if 'datetime' in df.columns and 'datetime' in tr_df.columns:
            df = df.merge(tr_df[['datetime', 'Tr']], on='datetime', how='left')
        else:
            # 如果没有 datetime 列，直接用index对齐
            df['Tr'] = tr_df['Tr']

        """
        # 计算因子，缺失mindiff，故这个函数是没有比较的
        df[f'FCT_Bias_1@{length}'] = (df['close'] - df['close'].rolling(window=length).mean()) / df['Tr'].rolling(window=length).mean()
        """

        # 计算 Tr 的滚动均值并处理NaN
        rolling_mean_tr = df['Tr'].rolling(window=length).mean().fillna(0)

        # 计算收盘价的滚动均值
        rolling_mean_close = df['close'].rolling(window=length).mean().fillna(0)

        # 正确的计算函数
        df[f'FCT_Bias_1@{length}'] = numpy.where(
            rolling_mean_tr < mindiff,
            0,
            (df['close'] - rolling_mean_close) / rolling_mean_tr
        )

        # 返回结果
        if 'datetime' in df.columns:
            df = df.rename(columns={'datetime': 'date'})
        result = df[['date', f'FCT_Bias_1@{length}']].copy()
        return result

