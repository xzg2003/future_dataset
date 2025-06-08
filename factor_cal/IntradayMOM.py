# IntradayMOM：日内动量因子，衡量每根K线的收盘价相对开盘价的对数收益率

import pandas
import numpy
import os

# 设置工作目录为当前脚本所在的目录
os.chdir(os.path.dirname(os.path.abspath(__file__)))

class IntradayMOM:
    def __init__(self):
        self.factor_name = 'IntradayMOM'

    def formula(self, param):
        # 从字典中提取 DataFrame
        df = param.get('df', None)
        if df is None:
            raise ValueError("no 'df' in param")
        if not isinstance(df, pandas.DataFrame):
            raise TypeError("df must be DataFrame")

        # 检查必要字段
        if 'open' not in df.columns or 'close' not in df.columns:
            raise ValueError("DataFrame must contain 'open' and 'close' columns")

        # 计算机每根 K 线的日内动量（对数收益率）
        df['IntradayMOM'] = numpy.log(df['close'] / df['open'])
        df['IntradayMOM'] = df['IntradayMOM'].replace([numpy.inf, -numpy.inf], numpy.nan).fillna(0)

        # 返回结果
        if 'datetime' in df.columns:
            df = df.rename(columns={'datetime': 'date'})
        result = df[['date', f'IntradayMOM']].copy()
        return result