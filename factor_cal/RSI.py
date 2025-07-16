# RSI：强弱相对指标

import pandas
import numpy
import os

# 设置工作目录为当前脚本所在的目录
os.chdir(os.path.dirname(os.path.abspath(__file__)))

class RSI:
    def __init__(self):
        self.factor_name = 'RSI'

    def formula(self, param):
        # 从字典中提取 DataFrame
        df = param.get('df', None)
        if df is None:
            raise ValueError("no 'df' in param")

        # 确保 df 是 pandas.DataFrame 类型
        if not isinstance(df, pandas.DataFrame):
            raise TypeError("df must be DataFrame")


        # 从字典中读取 length
        length = param.get('length', None)
        if length is None:
            raise ValueError("param missing 'length'")
        print(f"Using length: {length}")

        # 提取 close 数据为 NumPy 数组
        close = df['close'].values

        # 预分配中间数组
        up_array = numpy.zeros_like(close)
        down_array = numpy.zeros_like(close)
        rsi_array = numpy.full_like(close, numpy.nan, dtype=numpy.float32)

        # 计算涨跌值
        diff = numpy.diff(close, prepend=numpy.nan)
        up_array = numpy.where(numpy.isnan(diff), 0, numpy.maximum(diff, 0))
        down_array = numpy.where(numpy.isnan(diff), 0, numpy.maximum(-diff, 0))

        # 滑动窗口计算 avg_up / avg_down
        avg_up = numpy.full_like(close, numpy.nan, dtype=numpy.float32)
        avg_down = numpy.full_like(close, numpy.nan, dtype=numpy.float32)

        for i in range(length - 1, len(close)):
            window_up = up_array[i - length + 1:i + 1]
            window_down = down_array[i - length + 1:i + 1]
            if numpy.isnan(window_up).any() or numpy.isnan(window_down).any():
                continue
            avg_up[i] = numpy.mean(window_up)
            avg_down[i] = numpy.mean(window_down)

        # 计算 RS 和 RSI
        rs = avg_up / (avg_down + 1e-10)
        valid_mask = ~numpy.isnan(rs)
        rsi_array[valid_mask] = 100 - (100 / (1 + rs[valid_mask]))

        # 构造新列 Series
        col_name = f'{self.factor_name}@{length}'
        new_column = pandas.Series(rsi_array, index=df.index, name=col_name)

        # 使用 assign 添加新列，避免 concat，减少内存碎片
        df = df.assign(**{col_name: new_column})

        # 返回结果
        if 'datetime' in df.columns:
            df = df.rename(columns={'datetime': 'date'})
        result = df[['date', f'RSI@{length}']].copy()
        return result
