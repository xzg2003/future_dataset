# Ac_Tr_1：技术指标AC除以MA（TR）去量纲

import pandas
import numpy

class FCT_Ac_Tr_1:
    def __init__(self):
        self.factor_name = 'FCT_Ac_Tr_1'

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

        # 计算价格均值，这里取价格的最高价与最低价的平均
        df['MP'] = (df['high'] + df['low']) / 2

        # 计算震荡指标
        df['AO'] = df['MP'].rolling(window=length).mean() - df['MP'].rolling(window=(4*length)).mean()

        # 计算 AC
        df['AC'] = df['AO'] - df['AO'].rolling(window=length).mean()

        # 计算震荡指标（这里直接照搬了前面Tr的计算代码）
        # 前一k线的收盘价
        df['close_pre'] = df['close'].shift(1)

        # 取三种差值的绝对值的最大值作为 TR
        df['Tr'] = df[['close_pre', 'high', 'low']].apply(
            lambda row: max(row['high'] - row['close_pre'], row['high'] - row['low'], row['close_pre'] - row['low']),
            axis=1
        )

        """
        # 计算输出结果，这里没有最小变动单位，没有办法进行分类处理
        df[f'FCT_Ac_Tr_1@{length}'] = df['AC'] / df['Tr'].rolling(window=length).mean()
        """

        rolling_mean_tr = df['Tr'].rolling(window=length).mean().fillna(0)

        # 以下是正确的处理函数
        df[f'FCT_Ac_Tr_1@{length}'] = numpy.where(
            rolling_mean_tr < mindiff,
            0,
            df['AC'] / rolling_mean_tr
        )

        # 返回结果
        result = df[['datetime', f'FCT_Ac_Tr_1@{length}']].copy()
        return result