# FCT_Pubu_Atr_Dfive：衡量短期均线在长期均线窗口内的分位数位置，并用 ATR 归一化，适合捕捉价格分布于波动率的关系

import pandas
import numpy
import os

from torchgen.api.types import longT

# 设置工作目录为当前脚本所在的目录
os.chdir(os.path.dirname(os.path.abspath(__file__)))

class FCT_Pubu_Atr_Dfive:
    def __init__(self):
        self.factor_name = 'FCT_Pubu_Atr_Dfive'

    def formula(self, param):
        # 从字典中提取 DataFrame
        df = param.get('df', None)
        if df is None:
            raise ValueError("no 'df' in param")
        if not isinstance(df, pandas.DataFrame):
            raise TypeError("df must be DataFrame")

        # 均线和 ATR 周期参数
        short = param.get('short', 5)   # 默认为5
        long  = param.get('long', 20)   # 默认为20
        atr_length = param.get('atr_length', 14)
        print(f"Using short: {short}, long: {long}, atr_length: {atr_length}")

        # 计算短期均线和长期均线
        df['ma_short'] = df['close'].rolling(window=short).mean()
        df['ma_long']  = df['close'].rolling(window=long).mean()

        # 计算 ATR（这里应该可以直接调用 Tr 里面的计算结果）
        high_low    = df['high'] - df['low']
        high_close  = numpy.abs(df['high'] - df['close'].shift(1))
        low_close   = numpy.abs(df['low'] - df['close'].shift(1))
        tr          = pandas.concat([high_low, high_close, low_close], axis=1).max(axis=1)
        df['ATR']   = tr.rolling(window=atr_length).mean()

        # 计算短期均线在长期窗口内的分位数位置
        def pubu_percentile(x):
            window = x[-long:]
            if len(window) < long or numpy.all(numpy.isnan(window)):
                return numpy.nan
            return numpy.sum(window <= window[-1]) / long

        df['pubu'] = df['ma_short'].rolling(window=long, min_periods=long).apply(pubu_percentile, raw=True)

        # 用 ATR 归一化
        df[f'FCT_Pubu_Atr_Dfive@{short}_{long}_{atr_length}'] = df['pubu'] / (df['ATR'] + 1e-10)

        # 返回结果
        result = df[['datetime', f'FCT_Pubu_Atr_Dfive@{short}_{long}_{atr_length}']].copy()
        return result