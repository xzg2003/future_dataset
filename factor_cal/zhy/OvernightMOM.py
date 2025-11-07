# OvernightMOM：隔夜动量因子，衡量今开盘价相对昨收盘价的对数收益率
import numpy
import pandas

class OvernightMOM:
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
        open_array = df['open'].values
        close_array = df['close'].values

        # 预分配结果数组
        overnight_mom_array = numpy.full(len(df), numpy.nan, dtype=numpy.float32)

        # 计算昨日收盘价（shift 1）
        close_prev = numpy.roll(close_array, shift=1)
        close_prev[0] = numpy.nan  # 第一行无前一日数据

        # 向量化计算：log(open / close_prev)
        valid_mask = (close_prev > 1e-10) & ~numpy.isclose(close_prev, 0)
        overnight_mom_array[valid_mask] = numpy.log(open_array[valid_mask] / close_prev[valid_mask])

        # 替换 inf 和 -inf 为 NaN，并填充 0
        overnight_mom_array = numpy.nan_to_num(overnight_mom_array, nan=0.0, posinf=0.0, neginf=0.0)

        # 构造新列 Series
        new_column = pandas.Series(
            data=overnight_mom_array,
            index=df.index,
            name=factor_name
        )

        # 使用 assign 添加新列，避免 concat，减少内存碎片
        df = df.assign(**{new_column.name: new_column})

        # 返回结果（无日期）
        result = df[[factor_name]].copy()
        return result
