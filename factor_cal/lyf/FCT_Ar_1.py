# Ac_Tr_1：人气意愿指标，high、open、low差值累加对比

import pandas

class FCT_Ar_1:
    def __init__(self):
        pass

    def formula(self, param: dict):
        # 从参数字典中获取 df
        df = param.get('df', None)
        if df is None:
            raise ValueError("no 'df' in param")

        # 从参数字典中获取length
        length = param.get('length', None)
        if length is None:
            raise ValueError("param missing 'length'")

        # 从参数字典中获取factor_name
        factor_name = param.get('factor_name', None)
        if factor_name is None:
            raise ValueError("param missing factor_name")

        # 修改为 pd.concat 批量合并方式
        new_columns = pandas.DataFrame(index=df.index)

        new_columns['up'] = df['high'] - df['open']
        new_columns['down'] = df['open'] - df['low']

        new_columns['ar1'] = new_columns['up'].rolling(window=length).sum()
        new_columns['ar2'] = new_columns['down'].rolling(window=length).sum()

        new_columns[f'{factor_name}'] = (new_columns['ar1'] - new_columns['ar2']) / (
                new_columns['ar1'] + new_columns['ar2'])

        # 合并进原始 df
        df = pandas.concat([df, new_columns], axis=1)

        # 返回结果（无日期）
        result = df[[f'{factor_name}']].copy()
        return result
