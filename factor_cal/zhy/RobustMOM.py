# Robust Momentum （稳健动量）
# 这里采用过去 length 期收盘价的中位数与当前收盘价的对数收益率作为稳健动量
import numpy
import pandas

class RobustMOM:
    def __init__(self):
        pass

    def formula(self, param: dict):
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

        # 预分配结果数组
        robust_mom_array = numpy.full(len(df), numpy.nan, dtype=numpy.float32)

        # 滑动窗口计算中位数
        for i in range(length - 1, len(close_array)):
            window = close_array[i - length + 1:i + 1]
            if numpy.isnan(window).any():
                continue
            median = numpy.median(window)
            robust_mom_array[i] = numpy.log(close_array[i] / median) if median > 1e-10 else numpy.nan

        # 替换 inf 和 nan 为 0
        robust_mom_array = numpy.nan_to_num(robust_mom_array, nan=0.0, posinf=0.0, neginf=0.0)

        # 构造新列 Series
        new_column = pandas.Series(
            data=robust_mom_array,
            index=df.index,
            name=factor_name
        )

        # 使用 assign 添加新列，避免 concat，减少内存碎片
        df = df.assign(**{factor_name: new_column})

        # 返回结果（无日期）
        result = df[[factor_name]].copy()
        return result
