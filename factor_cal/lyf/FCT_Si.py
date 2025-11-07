# FCT_Si：SI（波动率指标）因子，衡量收盘价的绝对变化幅度的均值

import os
import numpy
import pandas

class FCT_Si:
    def __init__(self):
        pass

    def formula(self, param: dict):
        # 从参数字典中提取 DataFrame
        df = param.get('df', None)
        if df is None:
            raise ValueError("no 'df' in param")

        # 从参数字典中读取 length
        length = param.get('length', None)
        if length is None:
            raise ValueError("param missing 'length'")

        # 从参数字典中读取 factor_name
        factor_name = param.get('factor_name', None)
        if factor_name is None:
            raise ValueError("param missing 'factor_name'")

        new_columns = pandas.DataFrame(index=df.index)

        # 计算收盘价的绝对变化幅度
        new_columns['abs_diff'] = numpy.abs(df['close'].diff())

        # 计算 SI 指标（绝对变化幅度的均值）
        new_columns[f'{factor_name}'] = new_columns['abs_diff'].rolling(window=length).mean()

        # 合并进原始 df
        df = pandas.concat([df, new_columns], axis=1)

        # 返回结果（无日期）
        result = df[[f'{factor_name}']].copy()
        return result
