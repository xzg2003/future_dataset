# FCT_Pubu_Vol_Dfive：衡量短期均线在长期均线窗口内的分位数位置，并用成交量归一化，适合捕捉价格分布与成交活跃度的关系

import os
import sys
import numpy
import pandas
sys.path.append('.')
from factor_cal.get_exist_data import get_exist_data

class FCT_Pubu_Vol_Dfive:
    def __init__(self):
        pass

    def formula(self, param: dict):
        # 从参数字典中获取 DataFrame
        df = param.get('df', None)
        if df is None:
            raise ValueError("no 'df' in param")

        # 从参数字典中获取 vol_length
        vol_length = param.get('vol_length', None)

        # 从参数字典中获取 length
        length = param.get('length', None)

        # 从参数字典中获取 instrument
        instrument = param.get('instrument', None)
        if instrument is None:
            raise ValueError("param miss instrument")

        # 从参数字典中获取 factor_name
        factor_name = param.get('factor_name', None)
        if factor_name is None:
            raise ValueError("param miss factor_name")
        
        # 从参数字典中获取 depend_on
        depend_on = param.get('depend_on', None)
        if depend_on is None:
            raise ValueError("param miss depend_on")

        # 计算成交量均值
        df['vol_mean'] = df['volume'].rolling(window=vol_length).mean()

        # 修改为 pd.concat 批量合并方式
        new_columns = pandas.DataFrame(index=df.index)

        # 计算成交量均值
        new_columns['vol_mean'] = df['volume'].rolling(window=vol_length).mean()

        # 加载 FCT_Pubu_1 数据
        pubu_df = get_exist_data(instrument, depend_on)
        new_columns[depend_on] = pubu_df[depend_on]

        # 用成交量均值归一化
        new_columns[f'{factor_name}'] = new_columns[f'FCT_Pubu_1@{length}'] / (new_columns['vol_mean'] + 1e-10)

        # 合并进原始 df
        df = pandas.concat([df, new_columns], axis=1)

        # 返回结果（无日期）
        result = df[[f'{factor_name}']].copy()
        return result
