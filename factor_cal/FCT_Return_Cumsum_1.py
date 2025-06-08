# FCT_Return_Cumsum_1:  累积收益率因子，衡量从起始到当前的累积对数收益

import pandas
import numpy
import os

# 设置工作目录为当前脚本所在的目录
os.chdir(os.path.dirname(os.path.abspath(__file__)))

class FCT_Return_Cumsum_1:
    def __init__(self):
        self.factor_name = 'FCT_Return_Cumsum_1'

    def formula(self, param):
        # 从字典中提取 DataFrame
        df = param.get('df', None)
        if df is None:
            raise ValueError("no 'df' in param")
        if not isinstance(df, pandas.DataFrame):
            raise TypeError("df must be DataFrame")

        # 计算对数收益率
        df['ret'] = numpy.log(df['close'] / df['close'].shift(1))

        # 计算累积收益率
        df['FCT_Return_Cumsum_1'] = df['ret'].cumsum().fillna(0)

        # 返回结果
        if 'datetime' in df.columns:
            df = df.rename(columns={'datetime': 'date'})
        result = df[['date', f'FCT_Return_Cumsum_1']].copy()
        return result