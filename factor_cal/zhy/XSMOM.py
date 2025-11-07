# XSMOM: 横截面动量，计算商品在同类品种中的收益率排名，做多前20%，做空后20%.
# 但是需要计算多种类型的期货，这里无法进行处理
import os
import numpy
import pandas
import sys
sys.path.append('.')
from factor_cal.config import *
from factor_cal.get_exist_data import get_exist_data

class XSMOM:
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
        
        # 从参数字典中提前 instrument
        instrument = param.get('instrument', None)

        # 确保 df 是 pandas.DataFrame 类型
        if not isinstance(df, pandas.DataFrame):
            raise TypeError("df must be DataFrame")
        
        # 从参数字典中提取 depend_on
        depend_on = param.get('depend_on', None)
        if depend_on is None:
            raise ValueError("param missing 'depend_on'")

        # 获取 TSMOM 数据
        tsmom_df = get_exist_data(instrument, depend_on)

        # 合并 TSMOM 数据
        if 'datetime' in df.columns and 'datetime' in tsmom_df.columns:
            df = df.merge(tsmom_df[['datetime', f'TSMOM@{length}']], on='datetime', how='left')
        else:
            df[f'TSMOM@{length}'] = tsmom_df[f'TSMOM@{length}'].values[:len(df)]

        # 提取 TSMOM 列用于后续计算
        tsmom_array = df[f'TSMOM@{length}'].values

        # 预分配结果数组
        xs_result_array = numpy.full(len(df), numpy.nan, dtype=numpy.float32)

        percentile_pos = max(int(length * 0.2), 1)

        # 使用滑动窗口向量化方式计算分组均值差
        for i in range(length - 1, len(df)):
            window = tsmom_array[i - length + 1:i + 1]
            if numpy.isnan(window).any():
                continue
            window_sorted = numpy.sort(window)
            bottom_mean = numpy.mean(window_sorted[:percentile_pos])
            top_mean = numpy.mean(window_sorted[-percentile_pos:])
            xs_result_array[i] = top_mean - bottom_mean

        # 构造新列 Series
        new_column = pandas.Series(xs_result_array, index=df.index, name=factor_name)

        # 使用 assign 添加新列，避免 concat，减少内存碎片
        df = df.assign(**{factor_name: new_column})

        # 返回结果
        result = df[[f'XSMOM@{length}']].copy()
        return result
