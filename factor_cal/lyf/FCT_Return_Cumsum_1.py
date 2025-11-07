# FCT_Return_Cumsum_1:  累积收益率因子，衡量从起始到当前的累积对数收益

import os

import numpy
import pandas

class FCT_Return_Cumsum_1:
    def __init__(self):
        pass

    def formula(self, param: dict):
        # 从参数字典中提取 DataFrame
        df = param.get('df', None)
        if df is None:
            raise ValueError("no 'df' in param")

        # 从参数字典中获取 factor_name
        factor_name = param.get('factor_name', None)
        if factor_name is None:
            raise ValueError("no 'factor_name' in param")

        # 从参数字典中获取 length
        length = param.get('length', None)

        # 修改为 pd.concat 批量合并方式
        new_columns = pandas.DataFrame(index=df.index)

        # 计算每日的收益率
        new_columns['Return'] = numpy.log(df['close'] - df['close'].shift(1) / df['close'].shift(1))

        # 计算累积收益率
        new_columns[f'{factor_name}'] = new_columns['Return'].rolling(window=length).sum()

        # 合并进原始 df
        df = pandas.concat([df, new_columns], axis=1)

        # 返回结果（无日期）
        result = df[[f'{factor_name}']].copy()
        return result
