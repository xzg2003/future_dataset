# FCT_Pubu_Atr_Dfive：衡量短期均线在长期均线窗口内的分位数位置，并用 ATR 归一化，适合捕捉价格分布于波动率的关系

import os
import numpy
import pandas
import sys
sys.path.append('.')
from factor_cal.get_exist_data import get_exist_data

class FCT_Pubu_Atr_Dfive:
    def __init__(self):
        pass

    def formula(self, param: dict):
        # 从参数字典中提取 DataFrame
        df = param.get('df', None)
        if df is None:
            raise ValueError("no 'df' in param")

        # 从参数字典中提取 Length
        length = param.get('length', None)

        # 从参数字典中提取 atr_length
        atr_length = param.get('atr_length', None)
        if atr_length is None:
            raise ValueError("param miss atr_length")

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

        # 修改为 pd.concat 批量合并方式
        new_columns = pandas.DataFrame(index=df.index)

        # 来自外部文件
        for fac in depend_on:
            if fac.startswith('Tr'):
                tr_df = get_exist_data(instrument, fac)
                new_columns[fac] = tr_df[fac]
            if fac.startswith('FCT_Pubu_1'):
                pubu_df = get_exist_data(instrument, fac)
                new_columns[fac] = pubu_df[fac]

        # 计算 ATR
        new_columns['ATR'] = new_columns['Tr'].rolling(window=atr_length).mean()

        # 用 ATR 归一化
        new_columns[f'{factor_name}'] = new_columns[f'FCT_Pubu_1@{length}'] / (new_columns['ATR'] + 1e-10)

        # 合并进原始 df
        df = pandas.concat([df, new_columns], axis=1)

        # 返回结果
        result = df[[f'{factor_name}']].copy()
        return result
