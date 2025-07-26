# tr：波动幅度，当前k线的高低点与上根k线收盘价三者两两做差，取绝对值的最大作为tr波幅

import pandas
import numpy

class Tr:
    def __init__(self):
        pass

    def formula(self, param):
        # 从字典中提取DataFrame
        df = param.get('df', None)
        if df is None:
            raise ValueError("参数 'param' 中缺少 'df' 键或其值为空")

        # 确保df是pandas.DataFrame类型
        if not isinstance(df, pandas.DataFrame):
            raise TypeError("'df' 必须是 pandas.DataFrame 类型")

        # 提取必要字段
        if not {'high', 'low', 'close'}.issubset(df.columns):
            raise ValueError("DataFrame 缺少必要字段：'high', 'low', 'close'")

        # 转换为 NumPy 数组以提高性能
        high = df['high'].values
        low = df['low'].values
        close = df['close'].values

        # 预分配结果数组
        tr_array = numpy.full_like(close, numpy.nan, dtype=numpy.float32)

        # 计算前一日收盘价（shift 1）
        close_pre = numpy.roll(close, shift=1)
        close_pre[0] = numpy.nan  # 第一行无前值

        # 向量化计算 TR：max(H - C_pre, H - L, C_pre - L)
        diff1 = high - close_pre
        diff2 = high - low
        diff3 = close_pre - low

        tr_array = numpy.maximum(numpy.maximum(diff1, diff2), diff3)

        # 构造新列 Series
        new_column = pandas.Series(tr_array, index=df.index, name='Tr')

        # 使用 assign 添加新列，避免 concat，减少内存碎片
        df = df.assign(**{new_column.name: new_column})

        # Tr的结果
        result = df['Tr'].copy()
        return result

