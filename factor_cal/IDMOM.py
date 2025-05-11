# IDMOM：日内动量

import pandas
import numpy
import os

# 设置工作目录为当前脚本所在的目录
os.chdir(os.path.dirname(os.path.abspath(__file__)))

class IDMOM:
    def __init__(self):
        self.factor_name = 'IDMOM'

    def formula(self, param):
        # 从字典中提取 DataFrame
        df = param.get('df', None)
        if df is None:
            raise ValueError("no 'df' in param")

        # 确保 df 是 pandas.DataFrame 类型
        if not isinstance(df, pandas.DataFrame):
            raise TypeError("df must be DataFrame")

        # 计算日内动量
        df['IDMOM'] = (df['close'] - df['open']) / df['open']

        # 返回结果
        result = df[['datetime', 'IDMOM']].copy()
        return result