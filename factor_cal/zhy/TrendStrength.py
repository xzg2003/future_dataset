# TrendStrength: 趋势系数因子，衡量价格序列的趋势强度（如线性回归斜率/标准差）
import numpy
import pandas

class TrendStrength:
    def __init__(self):
        pass

    def formula(self, param:dict):
         # 从参数字典中提取 DataFrame
        df = param.get('df', None)
        if df is None:
            raise ValueError("no 'df' in param")

        # 从参数字典中提取 length
        length = param.get('length', None)
        if length is None:
            raise ValueError("param missing 'length'")

        # 从参数字典中提取 factor_name
        factor_name = param.get('factor_name', None)
        if factor_name is None:
            raise ValueError("param missing 'factor_name'")

        # 确保 df 是 pandas.DataFrame 类型
        if not isinstance(df, pandas.DataFrame):
            raise TypeError("df must be DataFrame")

        # 提取 close 数据为 NumPy 数组
        close_array = df['close'].values

        # 预分配趋势强度数组
        trend_strength_array = numpy.full(len(close_array), numpy.nan, dtype=numpy.float32)

        # 构造 x 轴（窗口内的索引）
        x = numpy.arange(length, dtype=numpy.float32)
        x_mean = x.mean()

        # 滑动窗口计算趋势强度
        for i in range(length - 1, len(close_array)):
            y = close_array[i - length + 1:i + 1]
            y_mean = y.mean()

            # 手动计算协方差和方差（可选替代 linregress）
            covariance = numpy.sum((x - x_mean) * (y - y_mean))
            variance = numpy.sum((x - x_mean) ** 2)
            slope = covariance / (variance + 1e-10)

            std = numpy.std(y)
            trend_strength_array[i] = slope / (std + 1e-10)

        # 构造新列 Series
        new_column = pandas.Series(trend_strength_array, index=df.index, name=factor_name)

        # 使用 assign 添加新列，避免 concat，减少内存碎片
        df = df.assign(**{factor_name: new_column})

        # 返回结果（无日期）
        result = df[[factor_name]].copy()
        return result
