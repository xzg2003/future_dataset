# FCT_Vol_Cumsum_1：成交量累计因子，衡量从起始到当前的累计成交量

import pandas
import numpy
import os

# 设置工作目录为当前脚本所在的目录
os.chdir(os.path.dirname(os.path.abspath(__file__)))

class FCT_Vol_Cumsum_1:
    def __init__(self):
        self.factor_name = 'FCT_Vol_Cumsum_1'

    def formula(self, param):
        # 从字典中提取 DataFrame
        df = param.get('df', None)
        if df is None:
            raise ValueError("no 'df' in param")
        if not isinstance(df, pandas.DataFrame):
            raise TypeError("df must be DataFrame")

        # 计算累积成交量
        df['FCT_Vol_Cumsum_1'] = df['volume'].cumsum().fillna(0)

        # 返回结果
        result = df[['datetime', 'FCT_Vol_Cumsum_1']].copy()
        return result