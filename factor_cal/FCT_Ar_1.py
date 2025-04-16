# Ac_Tr_1：人气意愿指标，high、open、low差值累加对比

import pandas

class FCT_Ar_1:
    def __init__(self):
        self.factor_name = 'FCT_Ar_1'

    def formula(self, param, length):
        # 从字典中提取DataFrame
        df = param.get('df', None)
        if df is None:
            raise ValueError("参数 'param' 中缺少 'df' 键或其值为空")

        # 确保df是pandas.DataFrame类型
        if not isinstance(df, pandas.DataFrame):
            raise TypeError("'df' 必须是 pandas.DataFrame 类型")

        # 计算开盘价与最高、最低价的差值
        df['up']   = df['high'] - df['open']
        df['down'] = df['open'] - df['low']

        # 计算滑动求和
        df['ar1'] = df['up'].rolling(window=length).sum()
        df['ar2'] = df['down'].rolling(window=length).sum()

        # 计算特征值
        df['feature'] = (df['ar1'] - df['ar2']) / (df['ar1'] + df['ar2'])

        # 返回结果
        result = df[['trading_date', 'feature']].copy()
        return result