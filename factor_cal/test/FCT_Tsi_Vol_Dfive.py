# FCT_Tsi_Vol_Dfive：趋势强度与成交量归一化因子，衡量单位成交量下的趋势强度
import pandas
import numpy
import os
import sys
sys.path.append('.')
from factor_cal.config import *
from factor_cal.get_exist_data import get_exist_data
# 设置工作目录为当前脚本所在的目录
os.chdir(os.path.dirname(os.path.abspath(__file__)))

class FCT_Tsi_Vol_Dfive:
    def __init__(self):
        self.factor_name = 'FCT_Tsi_Vol_Dfive'

    def formula(self, param: dict):
        # 从参数字典中提取 DataFrame
        df = param.get('df', None)
        if df is None:
            raise ValueError("no 'df' in param")

        # 从参数字典中提取length
        length = param.get('length', None)
        if length is None:
            raise ValueError("no 'length' in param")

        # 从参数字典中提取 vol_length
        vol_length = param.get('vol_length', None)
        if vol_length is None:
            raise ValueError("no 'vol_length' in param")

        # 从参数字典中提取 factor_name
        factor_name = param.get('factor_name', None)
        if factor_name is None:
            raise ValueError("no 'factor_name' in param")

        # 从参数字典中提取 instrument
        instrument = param.get('instrument', None)

        # 从参数字典中提取 depend_on
        depend_on = param.get('depend_on', None)
        if depend_on is None:
            raise ValueError("no 'depend_on' in param")

        # 建议做法：初始化 new_columns 用于统一管理中间变量
        new_columns = pandas.DataFrame(index=df.index)

        # 获取依赖的因子
        tsi_df = get_exist_data(instrument, depend_on)

        if 'datetime' in df.columns and 'datetime' in tsi_df.columns:
            tsi_series = pandas.merge(df[['datetime']], tsi_df, on='datetime', how='left')[f'FCT_Tsi_1@{length}']
        else:
            tsi_series = tsi_df[f'FCT_Tsi_1@{length}']

        new_columns['TSI'] = tsi_series.reset_index(drop=True)

        # 成交量归一化
        new_columns['vol_mean'] = df['volume'].rolling(window=vol_length).mean()
        new_columns[f'{factor_name}'] = new_columns['TSI'] / (new_columns['vol_mean'] + 1e-10)

        # 最终合并
        df = pandas.concat([df, new_columns[[f'{factor_name}']]], axis=1)

        # 返回结果（无日期）
        result = df[[f'{factor_name}']].copy()
        return result