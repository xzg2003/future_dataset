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

        """
        # 计算过去 length 期收盘价的中位数
        df['median_close'] = df['close'].rolling(window=length).median()

        # 计算稳健动量（当前收盘价与过去 length 期中位数的对数收益率）
        df[f'RobustMOM@{length}'] = numpy.log(df['close'] / df['median_close'])
        df[f'RobustMOM@{length}'] = df[f'RobustMOM@{length}'].replace([numpy.inf, -numpy.inf], numpy.nan).fillna(0)
        """

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
        col_name = f'{self.factor_name}@{length}'
        new_column = pandas.Series(
            data=robust_mom_array,
            index=df.index,
            name=col_name
        )

        # 使用 assign 添加新列，避免 concat，减少内存碎片
        df = df.assign(**{col_name: new_column})

        # 返回结果
        if 'datetime' in df.columns:
            df = df.rename(columns={'datetime': 'date'})
        result = df[['date', f'RobustMOM@{length}']].copy()
        return result