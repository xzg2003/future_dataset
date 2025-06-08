# FCT_Sdrm_Atr_Dfive：标准差动量与 ATR 归一化因子，衡量价格波动性与波动率的关系

import pandas
import numpy
import os

# 设置工作目录为当前脚本所在的目录
os.chdir(os.path.dirname(os.path.abspath(__file__)))

class FCT_Sdrm_Atr_Dfive:
    def __init__(self):
        self.factor_name = 'FCT_Sdrm_Atr_Dfive'

    def formula(self, param):
        # 从字典中提取 DataFrame
        df = param.get('df', None)
        if df is None:
            raise ValueError("no 'df' in param")
        if not isinstance(df, pandas.DataFrame):
            raise TypeError("df must be DataFrame")

        # 参数
        length      = param.get('length', 20)
        atr_length  = param.get('atr_length', 14)
        print(f"Using length: {length}, atr_length: {atr_length}")

        # 计算收盘价标准差（动量波动性）
        df['std_close'] = df['close'].rolling(window=length).std()

        # 计算ATR
        high_low    = df['high'] - df['low']
        high_close  = numpy.abs(df['high'] - df['close'].shift(1))
        low_close   = numpy.abs(df['low'] - df['close'].shift(1))
        tr          = pandas.concat([high_low, high_close, low_close], axis=1).max(axis=1)
        df['ATR']   = tr.rolling(window=atr_length).mean()

        # 归一化：标准差/ATR
        df[f'FCT_Sdrm_Atr_Dfive@{length}_{atr_length}'] = df['std_close'] / (df['ATR'] + 1e-10)

        # 返回结果
        if 'datetime' in df.columns:
            df = df.rename(columns={'datetime': 'date'})
        result = df[['date', f'FCT_Sdrm_Atr_Dfive@{length}']].copy()
        return result