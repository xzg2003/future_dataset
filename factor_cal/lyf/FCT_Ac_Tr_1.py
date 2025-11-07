# Ac_Tr_1：技术指标AC除以MA（TR）去量纲

import os
import sys
import numpy
import pandas
sys.path.append('.')
from factor_cal.get_exist_data import get_exist_data

class FCT_Ac_Tr_1:
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
            raise ValueError("param missing mindiff")
        
        # 从参数字典中获取 depend_on
        depend_on = param.get('depend_on', None)
        if depend_on is None:
            raise ValueError("param missing depend_on")

        # 修改为 pd.concat 批量合并方式
        # 构建新的列 DataFrame
        new_columns = pandas.DataFrame(index=df.index)

        # 中间变量计算
        new_columns['MP'] = (df['high'] + df['low']) / 2
        new_columns['AO'] = new_columns['MP'].rolling(window=length).mean() - \
                            new_columns['MP'].rolling(window=4 * length).mean()
        new_columns['AC'] = new_columns['AO'] - new_columns['AO'].rolling(window=length).mean()

        # 前一k线收盘价
        new_columns['close_pre'] = df['close'].shift(1)

        # Tr 数据来自参数字典
        tr_df = get_exist_data(instrument, depend_on)
        new_columns[depend_on] = tr_df[depend_on]

        # 最终因子计算
        rolling_mean_tr = new_columns['Tr'].rolling(window=length).mean().fillna(0)
        new_columns[f'{factor_name}'] = numpy.where(
            rolling_mean_tr < mindiff,
            0,
            new_columns['AC'] / rolling_mean_tr
        )

        # 合并进原始 df
        df = pandas.concat([df, new_columns], axis=1)

        # 返回结果（无日期）
        result = df[[f'{factor_name}']].copy()
        return result
