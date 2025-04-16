# 人气意愿指标high, ref(close,1), low差值累加对比

import pandas
import numpy

class FCT_Br_1:
    def __init__(self):
        self.factor_name = 'FCT_Br_1'

    def formula(self, param, length):
        # 从字典中提取DataFrame
        df = param.get('df', None)
        if df is None:
            raise ValueError("参数 'param' 中缺少 'df' 键或其值为空")

        # 确保df是pandas.DataFrame类型
        if not isinstance(df, pandas.DataFrame):
            raise TypeError("'df' 必须是 pandas.DataFrame 类型")

        # 得到前一个收盘价
        df['close_pre'] = df['close'].shift(1)

        # 计算up和down两个值
        df['up'] = numpy.where((df['high'] - df['close_pre']) > 0, df['high'] - df['close_pre'], 0)
        df['down'] = numpy.where((df['close_pre'] - df['low']) > 0, df['close_pre'] - df['low'], 0)

        # 计算两个指标
        df['br1'] = df['up'].rolling(window=length).sum()
        df['br2'] = df['down'].rolling(window=length).sum()

        # 计算特征值
        df['feature'] = (df['br1'] - df['br2']) / (df['br1'] + df['br2'])

        # 返回特征值
        result = df[['trading_date', 'FCT_Br_1']].copy()
        return result