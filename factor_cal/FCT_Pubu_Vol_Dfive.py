# FCT_Pubu_Vol_Dfive：衡量短期均线在长期均线窗口内的分位数位置，并用成交量归一化，适合捕捉价格分布与成交活跃度的关系

import pandas
import numpy
import os

# 设置工作目录为当前脚本所在的目录
os.chdir(os.path.dirname(os.path.abspath(__file__)))

class FCT_Pubu_Vol_Dfive:
    def __init__(self):
        self.factor_name = 'FCT_Pubu_Vol_Dfive'

    def formula(self, param):
        # 从字典中提取 DataFrame
        df = param.get('df', None)
        if df is None:
            raise ValueError("no 'df' in param")
        if not isinstance(df, pandas.DataFrame):
            raise TypeError("df must be DataFrame")

        # 均线和成交量周期参数
        short       = param.get('short', 5)
        long        = param.get('long', 20)
        vol_length  = param.get('vol_length', 14)
        print(f"Using short: {short}, long: {long}, vol_length: {vol_length}")

        # 计算短期和长期均线
        df['ma_short']  = df['close'].rolling(window=short).mean()
        df['ma_long']   = df['close'].rolling(window=long).mean()

        # 计算成交量均值
        df['vol_mean'] = df['volume'].rolling(window=vol_length).mean()

        # 计算短期均线在长期窗口内的分位数位置
        def pubu_percentile(x):
            window = x[-long:]
            if len(window) < long or numpy.all(numpy.isnan(window)):
                return numpy.nan
            return numpy.sum(window <= window[-1]) / long

        df['pubu'] = df['ma_short'].rolling(window=long, min_periods=long).apply(pubu_percentile, raw=True)

        # 用成交量均值归一化
        df[f'FCT_Pubu_Vol_Dfive@{short}_{long}_{vol_length}'] = df['pubu'] / (df['vol_mean'] + 1e-10)

        # 返回结果
        result = df[['datetime', f'FCT_Pubu_Vol_Dfive@{short}_{long}_{vol_length}']].copy()
        return result