# FCT_Return_Cumsum_1:  累积收益率因子，衡量从起始到当前的累积对数收益

import os

import numpy
import pandas

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

        # 修改为 pd.concat 批量合并方式
        new_columns = pandas.DataFrame(index=df.index)

        # 计算对数收益率
        new_columns['ret'] = numpy.log(df['close'] / df['close'].shift(1))

        # 计算累积收益率
        new_columns['FCT_Return_Cumsum_1'] = new_columns['ret'].cumsum().fillna(0)

        # 合并进原始 df
        df = pandas.concat([df, new_columns], axis=1)

        # 返回结果（无日期）
        result = df[[f'FCT_Return_Cumsum_1']].copy()
        return result
