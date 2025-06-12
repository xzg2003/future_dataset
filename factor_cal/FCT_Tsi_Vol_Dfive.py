# FCT_Tsi_Vol_Dfive：趋势强度与成交量归一化因子，衡量单位成交量下的趋势强度

import pandas
import numpy
import os

# 设置工作目录为当前脚本所在的目录
os.chdir(os.path.dirname(os.path.abspath(__file__)))

class FCT_Tsi_Vol_Dfive:
    def __init__(self):
        self.factor_name = 'FCT_Tsi_Vol_Dfive'

    def formula(self, param):
        # 从字典中提取 DataFrame
        df = param.get('df', None)
        if df is None:
            raise ValueError("no 'df' in param")
        if not isinstance(df, pandas.DataFrame):
            raise TypeError("df must be DataFrame")

        # 参数
        short = param.get('short', 25)
        long = param.get('long', 13)
        vol_length = param.get('vol_length', 14)
        if short is None or long is None or vol_length is None:
            raise ValueError("param missing 'short', 'long' or 'vol_length'")
        print(f"Using short: {short}, long: {long}, vol_length: {vol_length}")

        # 计算TSI
        df['diff'] = df['close'].diff()
        ema1 = df['diff'].ewm(span=short, adjust=False).mean()
        ema2 = ema1.ewm(span=long, adjust=False).mean()
        abs_diff = numpy.abs(df['diff'])
        abs_ema1 = abs_diff.ewm(span=short, adjust=False).mean()
        abs_ema2 = abs_ema1.ewm(span=long, adjust=False).mean()
        df['TSI'] = 100 * (ema2 / (abs_ema2 + 1e-10))

        # 计算成交量均值
        df['vol_mean'] = df['volume'].rolling(window=vol_length).mean()

        # 归一化
        df[f'FCT_Tsi_Vol_Dfive'] = df['TSI'] / (df['vol_mean'] + 1e-10)

        # 返回结果
        if 'datetime' in df.columns:
            df = df.rename(columns={'datetime': 'date'})
        result = df[['date', f'FCT_Tsi_Vol_Dfive']].copy()
        return result