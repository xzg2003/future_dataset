# RSI：强弱相对指标

import pandas
import numpy
import os

# 设置工作目录为当前脚本所在的目录
os.chdir(os.path.dirname(os.path.abspath(__file__)))

class RSI:
    def __init__(self):
        self.factor_name = 'RSI'

    def formula(self, param):
        # 从字典中提取 DataFrame
        df = param.get('df', None)
        if df is None:
            raise ValueError("no 'df' in param")

        # 确保 df 是 pandas.DataFrame 类型
        if not isinstance(df, pandas.DataFrame):
            raise TypeError("df must be DataFrame")


        # 从字典中读取 length
        length = param.get('length', None)
        if length is None:
            raise ValueError("param missing 'length'")
        print(f"Using length: {length}")

        # 计算收盘涨跌
        df['diff'] = df['close'].diff()
        df['up']   = numpy.where(df['diff'] > 0, df['diff'], 0)
        df['down'] = numpy.where(df['diff'] < 0, -df['diff'], 0)

        # 计算平均涨幅和平均跌幅
        avg_up   = df['up'].rolling(window=length).mean()
        avg_down = df['dwon'].rolling(window=length).mean()

        # 计算 RSI
        rs = avg_up / (avg_down + 1e-10)    # 防止除零的情况
        df[f'RSI@{length}'] = 100 - (100 / (1 + rs))

        # 返回结果
        result = df[['datetime', f'RSI@{length}']].copy()
        return result
