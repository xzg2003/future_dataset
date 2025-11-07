# FCT_Sdrm_Atr_Dfive：标准差动量与 ATR 归一化因子，衡量价格波动性与波动率的关系

import os
import numpy
import pandas

class FCT_Sdrm_Atr_Dfive:
    def __init__(self):
        pass

    def formula(self, param: dict):
        # 从参数字典中提取 DataFrame
        df = param.get('df', None)
        if df is None:
            raise ValueError("no 'df' in param")

        # 从参数字典中提取 length
        length = param.get('length', None)
        if length is None:
            raise ValueError("no 'length' in param")

        # 从参数字典中提取 atr_length
        atr_length = param.get('atr_length', None)
        if atr_length is None:
            raise ValueError("no 'atr_length' in param")

        # 从参数字典中提取 factor_name
        factor_name = param.get('factor_name', None)
        if factor_name is None:
            raise ValueError("no 'factor_name' in param")

        new_columns = pandas.DataFrame(index=df.index)

        # 计算收盘价标准差（动量波动性）
        new_columns['std_close'] = df['close'].rolling(window=length).std()

        # 计算ATR
        high_low = df['high'] - df['low']
        high_close = numpy.abs(df['high'] - df['close'].shift(1))
        low_close = numpy.abs(df['low'] - df['close'].shift(1))
        tr = pandas.concat([high_low, high_close, low_close], axis=1).max(axis=1)
        new_columns['ATR'] = tr.rolling(window=atr_length).mean()

        # 归一化：标准差 / ATR
        new_columns[f'{factor_name}'] = new_columns['std_close'] / (new_columns['ATR'] + 1e-10)

        # 合并到原始 df
        df = pandas.concat([df, new_columns], axis=1)

        # 返回结果（无日期）
        result = df[[f'{factor_name}']].copy()
        return result
