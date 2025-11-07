# FCT_Tsi_Vol_Dfive：趋势强度与成交量归一化因子，衡量单位成交量下的趋势强度

import pandas
import numpy
import os
import sys
sys.path.append(".")
from factor_cal.get_exist_data import get_exist_data

class FCT_Tsi_Vol_Dfive:
    def __init__(self):
        pass

    def formula(self, param: dict):
        # 从参数字典中提取 DataFrame
        df = param.get('df', None)
        if df is None:
            raise ValueError("no 'df' in param")

        # 从参数字典中提取length
        length = param.get('length', None)

        # 从参数字典中提取 vol_length
        vol_length = param.get('vol_length', None)
        if vol_length is None:
            raise ValueError("no 'vol_length' in param")
        
        # 从参数字典中获取 instrument
        instrument = param.get('instrument', None)
        if instrument is None:
            raise ValueError("param miss instrument")

        # 从参数字典中提取 factor_name
        factor_name = param.get('factor_name', None)
        if factor_name is None:
            raise ValueError("no 'factor_name' in param")

        # 从参数字典中获取 depend_on
        depend_on = param.get('depend_on', None)
        if depend_on is None:
            raise ValueError("param miss depend_on")

        # 初始化 new_columns 用于统一管理中间变量
        new_columns = pandas.DataFrame(index=df.index)

        # 导入先前Tsi的计算结果
        tsi_df = get_exist_data(instrument, depend_on)
        new_columns[depend_on] = tsi_df[depend_on]
        new_columns['TSI'] = tsi_df[depend_on]

        # 成交量归一化
        new_columns['vol_mean'] = df['volume'].rolling(window=vol_length).mean()
        new_columns[f'{factor_name}'] = new_columns['TSI'] / (new_columns['vol_mean'] + 1e-10)

        # 最终合并
        df = pandas.concat([df, new_columns[[f'{factor_name}']]], axis=1)

        # 返回结果（无日期）
        result = df[[f'{factor_name}']].copy()
        return result