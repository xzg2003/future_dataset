# Robust Momentum （稳健动量）
# 这里采用过去 length 期收盘价的中位数与当前收盘价的对数收益率作为稳健动量

import pandas
import  numpy
import os

# 设置工作目录为当前脚本所在的目录
os.chdir(os.path.dirname(os.path.abspath(__file__)))

class RobustMOM:
    def __init__(self):
        self.factor_name = 'RobustMOM'

    def formula(self, param):
        # 从字典中提取 DataFrame
        df = param.get('df', None)
        if df is None:
            raise ValueError("no 'df' in param")
        if not isinstance(df, pandas.DataFrame):
            raise TypeError("df must be DataFrame")

        # 从字典中提取 length
        length = param.get('length', None)
        if length is None:
            raise ValueError("param missing length")
        print(f"Using length: {length}")

        # 计算过去 length 期收盘价的中位数
        df['median_close'] = df['close'].rolling(window=length).median()

        # 计算稳健动量（当前收盘价与过去 length 期中位数的对数收益率）
        df[f'RobustMOM@{length}'] = numpy.log(df['close'] / df['median_close'])
        df[f'RobustMOM@{length}'] = df[f'RobustMOM@{length}'].replace([numpy.inf, -numpy.inf], numpy.nan).fillna(0)

        # 返回结果
        if 'datetime' in df.columns:
            df = df.rename(columns={'datetime': 'date'})
        result = df[['date', f'RobustMOM@{length}']].copy()
        return result