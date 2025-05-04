# 人气意愿指标high, ref(close,1), low差值累加对比

import pandas
import numpy

class FCT_Br_1:
    def __init__(self):
        self.factor_name = 'FCT_Br_1'

    def formula(self, param):
        # 从字典中提取DataFrame
        df = param.get('df', None)
        if df is None:
            raise ValueError("no 'df' in param")

        # 确保df是pandas.DataFrame类型
        if not isinstance(df, pandas.DataFrame):
            raise TypeError("df must be DataFrame")

        """
        从字典中读取 length
        获取 instrument 名称，用于提取mindiff中的数据
        """
        length = param.get('length', None)
        if length is None:
            raise ValueError("param missing 'length'")
        print(f"Using length:{length}")

        # 得到前一个收盘价
        df['close_pre'] = df['close'].shift(1)

        # 计算up和down两个值
        df['up'] = numpy.where((df['high'] - df['close_pre']) > 0, df['high'] - df['close_pre'], 0)
        df['down'] = numpy.where((df['close_pre'] - df['low']) > 0, df['close_pre'] - df['low'], 0)

        # 计算两个指标
        df['br1'] = df['up'].rolling(window=length).sum()
        df['br2'] = df['down'].rolling(window=length).sum()

        # 避免分母为零的情况
        df['br_sum'] = df['br1'] + df['br2']
        df['br_sum'] = numpy.where(df['br_sum'] == 0, numpy.nan, df['br_sum'])  # 避免分母为零

        # 计算特征值
        df[f'FCT_Br_1@{length}'] = (df['br1'] - df['br2']) / df['br_sum']

        # 返回特征值
        result = df[['datetime', f'FCT_Br_1@{length}']].copy()
        return result