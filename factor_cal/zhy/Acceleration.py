# Acceleration: 动量变化率。调用了 TSMOM 的计算结果
import os
import numpy
import pandas
import sys
sys.path.append('.')
from factor_cal.config import *
from factor_cal.get_exist_data import get_exist_data

class Acceleration:
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

        # 从参数字典中提取 instrument
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

        if 'datetime' in df.columns and 'datetime' in tsmom_df.columns:
            df = df.merge(tsmom_df[['datetime', f'TSMOM@{length}']], on='datetime', how='left')
        else:
            df[f'TSMOM@{length}'] = tsmom_df[f'TSMOM@{length}']

        # 使用 NumPy 数组计算 pct_change
        tsmom_values = df[f'TSMOM@{length}'].values
        acceleration_values = numpy.empty_like(tsmom_values)
        acceleration_values[:length] = numpy.nan
        acceleration_values[length:] = tsmom_values[length:] / (tsmom_values[:-length] + 1e-10) - 1

        # 构建新列
        new_columns = pandas.DataFrame({
            f'Acceleration@{length}': acceleration_values
        }, index=df.index)

        # 将新的列合并进来
        df = pandas.concat([df, new_columns], axis=1)

        # 返回结果（无日期）
        result = df[[f'Acceleration@{length}']].copy()
        return result
