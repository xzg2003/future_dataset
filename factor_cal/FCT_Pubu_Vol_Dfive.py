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

        # 获取 instrument
        instrument = param.get('instrument', None)
        if instrument is None:
            raise ValueError("param miss instrument")
        # 计算成交量均值
        df['vol_mean'] = df['volume'].rolling(window=vol_length).mean()

        # 获取k_line_type
        k_line_type = param.get('k_line_type', None)
        if k_line_type is None:
            raise ValueError("param missing instrument")

        # 计算短期均线在长期窗口内的分位数位置
        def pubu_percentile(x):
            window = x[-long:]
            if len(window) < long or numpy.all(numpy.isnan(window)):
                return numpy.nan
            return numpy.sum(window <= window[-1]) / long

        # 判断 FCT_Pubu@{short}_{long}.csv 文件是否存在，便于调用
        pubu_data_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), f'../data/{k_line_type}/{instrument}/FCT_Pubu_1@{short}_{long}.csv')
        if not os.path.exists(pubu_data_path):
            raise FileNotFoundError(F"Pubu file noot fount: {pubu_data_path}")

        pubu_df = pandas.read_csv(pubu_data_path)
        # FCT_Pubu_q@{short}_{long}.csv 有datetime 和 FCT_Pubu@{short}_{long} 两列，且与主 df 按 datetime 对齐
        if 'datetime' in df.columns and 'datetime' in pubu_df.columns:
            df = df.merge(pubu_df[['datetime', f'FCT_Pubu_1@{short}_{long}']], on='datetime', how='left')
        else:
            # 如果没有 datetime 列，直接用 index 对齐
            df[f'FCT_Pubu_1@{short}_{long}'] = pubu_df[f'FCT_Pubu_1@{short}_{long}']

        # 用成交量均值归一化
        df[f'FCT_Pubu_Vol_Dfive@{short}_{long}_{vol_length}'] = df[f'FCT_Pubu_1@{short}_{long}'] / (df['vol_mean'] + 1e-10)

        # 返回结果
        if 'datetime' in df.columns:
            df = df.rename(columns={'datetime': 'date'})
        result = df[['date', f'FCT_Pubu_Vol_Dfive@{short}_{long}_{vol_length}']].copy()
        return result