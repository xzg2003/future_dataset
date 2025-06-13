# FCT_Tsi_Atr_Dfive：趋势强度与ATR归一化因子，衡量单位波动下的趋势强度

import pandas
import numpy
import os

# 设置工作目录为当前脚本所在的目录
os.chdir(os.path.dirname(os.path.abspath(__file__)))

class FCT_Tsi_Atr_Dfive:
    def __init__(self):
        self.factor_name = 'FCT_Tsi_Atr_Dfive'

    def formula(self, param):
        # 从字典中提取 DataFrame
        df = param.get('df', None)
        if df is None:
            raise ValueError("no 'df' in param")
        if not isinstance(df, pandas.DataFrame):
            raise TypeError("df must be DataFrame")

        # 调取参数
        short = param.get('short', 25)
        long  = param.get('long', 13)
        atr_length = param.get('atr_length', 14)
        if short is None or long is None or atr_length is None:
            raise ValueError("param missing 'short', 'long' or 'atr_length'")
        print(f"Using short: {short}, long: {long}, atr_length: {atr_length}")

        """
        # 计算 TSI
        df['diff'] = df['close'].diff()
        ema_1 = df['diff'].ewm(span=short, adjust=False).mean()
        ema_2 = ema_1.ewm(span=long, adjust=False).mean()
        abs_diff = numpy.abs(df['diff'])
        abs_ema_1 = abs_diff.ewm(span=short, adjust=False).mean()
        abs_ema_2 = abs_ema_1.ewm(span=long, adjust=False).mean()
        df['TSI'] = 100 * (ema_2 / (abs_ema_2 + 1e-10))

        # 计算 ATR
        high_low = df['high'] - df['low']
        high_close = numpy.abs(df['high'] - df['close'].shift(1))
        low_close = numpy.abs(df['low'] - df['close'].shift(1))
        tr = pandas.concat([high_low, high_close, low_close], axis=1).max(axis=1)
        df['ATR'] = tr.rolling(window=atr_length).mean()

        # 归一化
        df[f'FCT_Tsi_Atr_Dfive'] = df['TSI'] / (df['ATR'] + 1e-10)
        """

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
        new_columns[f'FCT_Tsi_Atr_Dfive'] = new_columns['TSI'] / (new_columns['ATR'] + 1e-10)

        # 合并到主表
        df = pandas.concat([df, new_columns], axis=1)

        # 返回结果
        if 'datetime' in df.columns:
            df = df.rename(columns={'datetime': 'date'})
        result = df[['date', f'FCT_Tsi_Atr_Dfive']].copy()
        return result