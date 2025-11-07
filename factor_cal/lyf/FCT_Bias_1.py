# 乖离率除以TR去量纲

import os
import numpy
import pandas
import sys
sys.path.append('.')
from factor_cal.get_exist_data import get_exist_data

class FCT_Bias_1:
    def __init__(self):
        pass

    def formula(self, param: dict):
        # 从参数字典中获取 df
        df = param.get('df', None)
        if df is None:
            raise ValueError("no 'df' in param")

        # 从参数字典中获取 length
        length = param.get('length', None)
        if length is None:
            raise ValueError("param missing 'length'")

        # 从参数字典中获取 instrument
        instrument = param.get('instrument', None)
        if instrument is None:
            raise ValueError("param miss instrument")

        # 从参数字典中获取 factor_name
        factor_name = param.get('factor_name', None)
        if factor_name is None:
            raise ValueError("param missing factor_name")

        # 从参数字典中获取 mindiff
        mindiff = param.get('mindiff', None)
        if mindiff is None:
            raise ValueError(f"param miss mindiff for instrument: {param.get('instrument', 'unknown')}")
        
        # 从参数字典中获取 depend_on
        depend_on = param.get('depend_on', None)
        if depend_on is None:
            raise ValueError("param missing depend_on")
        
        # 获取依赖因子数据
        Tr_df = get_exist_data(instrument, depend_on)
        
        # 修改为 pd.concat 批量合并方式
        new_columns = pandas.DataFrame(index=df.index)
        new_columns['Tr'] = Tr_df['Tr']

        # close_pre
        new_columns['close_pre'] = df['close'].shift(1)

        # 计算因子所需中间变量
        rolling_mean_tr = new_columns['Tr'].rolling(window=length).mean().fillna(0)
        rolling_mean_close = df['close'].rolling(window=length).mean().fillna(0)

        # 最终因子计算
        new_columns[f'{factor_name}'] = numpy.where(
            rolling_mean_tr < mindiff,
            0,
            (df['close'] - rolling_mean_close) / rolling_mean_tr
        )

        # 合并进原始 df
        df = pandas.concat([df, new_columns], axis=1)

        # 返回结果（无日期）
        result = df[[f'{factor_name}']].copy()
        return result
