# TSMOM: 常见的动量因子，用于衡量资产在过去一段时间内的累积收益情况
# 后续很多计算器需要调用 TSMOM 的计算结果

import pandas
import numpy
import os

# 设置工作目录为当前脚本所在的目录
os.chdir(os.path.dirname(os.path.abspath(__file__)))

class TSMOM:
    def __init__(self):
        self.factor_name = 'TSMOM'

    def formula(self, param):
        # 从字典中提取 DataFrame
        df = param.get('df', None)
        if df is None:
            raise ValueError("no 'df' in param")

        # 确保 df 是 pandas.DataFrame 类型
        if not isinstance(df, pandas.DataFrame):
            raise TypeError("df must be DataFrame")

        """
        从字典中读取 length
        """
        length = param.get('length', None)
        if length is None:
            raise ValueError("param missing 'length'")
        print(f"Using length:{length}")

        # 提取 close 数据为 NumPy 数组
        close_array = df['close'].values

        # 预分配结果数组
        tsmom_array = numpy.full(len(close_array), numpy.nan, dtype=numpy.float32)

        # 计算动量：pct_change(periods=length)
        valid_indices = numpy.arange(length, len(close_array))
        tsmom_array[valid_indices] = (close_array[valid_indices] - close_array[valid_indices - length]) / (
                close_array[valid_indices - length] + 1e-10
        )

        # 替换 inf 和 nan 为 0
        tsmom_array = numpy.nan_to_num(tsmom_array, nan=0.0, posinf=0.0, neginf=0.0)

        # 构造新列 Series
        col_name = f'{self.factor_name}@{length}'
        new_column = pandas.Series(data=tsmom_array, index=df.index, name=col_name)

        # 使用 assign 添加新列，避免 concat，减少内存碎片
        df = df.assign(**{col_name: new_column})

        # 返回结果
        if 'datetime' in df.columns:
            df = df.rename(columns={'datetime': 'date'})
        result = df[['date', f'TSMOM@{length}']].copy()
        return result