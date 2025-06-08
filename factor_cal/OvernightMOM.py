# OvernightMOM：隔夜动量因子，衡量今开盘价相对昨收盘价的对数收益率

import pandas
import numpy
import os

# 设置工作目录为当前脚本所在的目录
os.chdir(os.path.dirname(os.path.abspath(__file__)))

class OvernightMOM:
    def __init__(self):
        self.factor_name = 'OvernightMOM'

    def formula(self, param):
        # 从字典中提取 DataFrame
        df = param.get('df', None)
        if df is None:
            raise ValueError("no 'df' in param")
        if not isinstance(df, pandas.DataFrame):
            raise TypeError("df must be DataFrame")

        # 计算做完收盘价
        df['close_pre'] = df['close'].shift(1)

        # 计算隔夜动量（今开盘/昨收盘的对数收益率）
        df['OvernightMOM'] = numpy.log(df['open'] / df['close_pre'])
        df['OvernightMOM'] = df['OvernightMOM'].replace([numpy.inf, -numpy.inf], numpy.nan).fillna(0)

        # 返回结果
        if 'datetime' in df.columns:
            df = df.rename(columns={'datetime': 'date'})
        result = df[['date', f'OvernightMoM']].copy()
        return result