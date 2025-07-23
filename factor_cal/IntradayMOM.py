# IntradayMOM：日内动量因子，衡量每根K线的收盘价相对开盘价的对数收益率

import pandas
import numpy
import os

# 设置工作目录为当前脚本所在的目录
os.chdir(os.path.dirname(os.path.abspath(__file__)))

class IntradayMOM:
    def __init__(self):
        self.factor_name = 'IntradayMOM'

    def formula(self, param):
        # 从字典中提取 DataFrame
        df = param.get('df', None)
        if df is None:
            raise ValueError("no 'df' in param")
        if not isinstance(df, pandas.DataFrame):
            raise TypeError("df must be DataFrame")

        # 检查必要字段
        if 'open' not in df.columns or 'close' not in df.columns:
            raise ValueError("DataFrame must contain 'open' and 'close' columns")

        # 提取基础数据为 NumPy 数组
        open_array = df['open'].values
        close_array = df['close'].values

        # 预分配结果数组
        intraday_mom_array = numpy.full(len(df), numpy.nan, dtype=numpy.float32)

        # 向量化计算：log(close / open)
        valid_mask = (open_array > 1e-10) & ~numpy.isclose(open_array, 0)
        intraday_mom_array[valid_mask] = numpy.log(close_array[valid_mask] / open_array[valid_mask])

        # 替换 inf 和 -inf 为 NaN，并填充 0（可选）
        intraday_mom_array = numpy.nan_to_num(intraday_mom_array, nan=0.0, posinf=0.0, neginf=0.0)

        # 构造新列 Series
        new_column = pandas.Series(
            data=intraday_mom_array,
            index=df.index,
            name='IntradayMOM'
        )

        # 使用 assign 添加新列，避免 concat，减少内存碎片
        df = df.assign(**{new_column.name: new_column})

        # 返回结果
        if 'datetime' in df.columns:
            df = df.rename(columns={'datetime': 'date'})
        result = df[['date', f'IntradayMOM']].copy()
        return result