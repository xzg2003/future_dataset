# FCT_Sdrm_1：标准差动量因子，衡量收盘价在指定窗口内的波动性

import os
import pandas

class FCT_Sdrm_1:
    def __init__(self):
        pass

    def formula(self, param: dict):
        # 从参数字典中提取 DataFrame
        df = param.get('df', None)
        if df is None:
            raise ValueError("no 'df' in param")

        # 从参数字典中读取 length
        length = param.get('length', None)
        if length is None:
            raise ValueError("param missing 'length'")

        # 从参数字典中获取 factor_name
        factor_name = param.get('factor_name', None)
        if factor_name is None:
            raise ValueError("param missing 'factor_name'")

        # 修改为 pd.concat 批量合并方式
        new_columns = pandas.DataFrame({
            f'{factor_name}': df['close'].rolling(window=length).std()
        }, index=df.index)

        df = pandas.concat([df, new_columns], axis=1)

        # 返回结果（无日期）
        result = df[[f'{factor_name}']].copy()
        return result
