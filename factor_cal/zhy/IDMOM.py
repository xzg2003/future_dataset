# IDMOM：日内动量。这里IDMOM进行了简写
import pandas
import numpy

class IDMOM:
    def __init__(self):
        pass

    def formula(self, param:dict):
       # 从字典中提取 factor_name
        factor_name = param.get('factor_name', None)
        if factor_name is None:
            raise ValueError("param missing factor_name")
        
        # 从字典中提取 DataFrame
        df = param.get('df', None)
        if df is None:
            raise ValueError("no 'df' in param")
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
        new_column = pandas.Series(idmom_array, index=df.index, name=factor_name)

        # 使用 assign 替代 concat，避免内存碎片
        df = df.assign(**{
            new_column.name: new_column
        })

        # 返回结果（无日期）
        result = df[[factor_name]].copy()
        return result