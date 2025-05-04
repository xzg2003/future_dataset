# Ac_Tr_1：人气意愿指标，high、open、low差值累加对比

import pandas

class FCT_Ar_1:
    def __init__(self):
        self.factor_name = 'FCT_Ar_1'

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

        # 计算开盘价与最高、最低价的差值
        df['up']   = df['high'] - df['open']
        df['down'] = df['open'] - df['low']

        # 计算滑动求和
        df['ar1'] = df['up'].rolling(window=length).sum()
        df['ar2'] = df['down'].rolling(window=length).sum()

        # 计算特征值
        df[f'FCT_Ar_1@{length}'] = (df['ar1'] - df['ar2']) / (df['ar1'] + df['ar2'])

        # 返回结果
        result = df[['datetime', f'FCT_Ar_1@{length}']].copy()
        return result