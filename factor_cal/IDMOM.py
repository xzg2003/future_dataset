# IDMOM：日内动量。这里IDMOM进行了简写

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

        # 提取 open 和 close 列为 NumPy 数组
        open_price = df['open'].values
        close_price = df['close'].values

        # 预分配结果数组
        idmom_array = numpy.full(len(df), numpy.nan, dtype=numpy.float32)

        # 向量化计算 IDMOM：(close - open) / open
        valid_mask = open_price != 0
        idmom_array[valid_mask] = (close_price[valid_mask] - open_price[valid_mask]) / open_price[valid_mask]

        # 构造新列
        new_column = pandas.Series(idmom_array, index=df.index, name='IDMOM')

        # 使用 assign 替代 concat，避免内存碎片
        df = df.assign(**{
            new_column.name: new_column
        })

        # 返回结果（无日期）
        result = df[[f'IDMOM']].copy()
        return result