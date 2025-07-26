# FCT_Tsi_Atr_Dfive：趋势强度与ATR归一化因子，衡量单位波动下的趋势强度

import os

import numpy
import pandas

# 设置工作目录为当前脚本所在的目录
os.chdir(os.path.dirname(os.path.abspath(__file__)))


class FCT_Tsi_Atr_Dfive:
    def __init__(self):
        self.factor_name = 'FCT_Tsi_Atr_Dfive'

    def formula(self, param):
        # 从参数字典中提取 DataFrame
        df = param.get('df', None)
        if df is None:
            raise ValueError("no 'df' in param")

        # 从参数字典中提取 short, long
        short = param.get('short', None)
        long = param.get('long', None)
        if short or long is None:
            raise ValueError("no 'short' or 'long' in param")

        # 从参数字典中提取 atr_length
        atr_length = param.get('atr_length', None)
        if atr_length is None:
            raise ValueError("no 'atr_length' in param")

        # 从参数字典中提取 factor_name
        factor_name = param.get('factor_name', None)
        if factor_name is None:
            raise ValueError("no 'factor_name' in param")

        # 初始化 new_columns 用于统一管理中间变量
        new_columns = pandas.DataFrame(index=df.index)

        # 计算 TSI
        new_columns['diff'] = df['close'].diff()
        ema_1 = new_columns['diff'].ewm(span=short, adjust=False).mean()
        ema_2 = ema_1.ewm(span=long, adjust=False).mean()

        abs_diff = numpy.abs(new_columns['diff'])
        abs_ema_1 = abs_diff.ewm(span=short, adjust=False).mean()
        abs_ema_2 = abs_ema_1.ewm(span=long, adjust=False).mean()
        new_columns['TSI'] = 100 * (ema_2 / (abs_ema_2 + 1e-10))

        # 计算 ATR
        high_low = df['high'] - df['low']
        high_close = numpy.abs(df['high'] - df['close'].shift(1))
        low_close = numpy.abs(df['low'] - df['close'].shift(1))
        tr = pandas.concat([high_low, high_close, low_close], axis=1).max(axis=1)
        new_columns['ATR'] = tr.rolling(window=atr_length).mean()

        # 归一化：TSI / ATR
        new_columns[f'{factor_name}'] = new_columns['TSI'] / (new_columns['ATR'] + 1e-10)

        # 合并到主表
        df = pandas.concat([df, new_columns], axis=1)

        # 返回结果（无日期）
        result = df[[f'{factor_name}']].copy()
        return result
