# FCT_R_Div_RStd:   收益率与波动率比值因子，衡量单位波动下的收益率（动量/风险调整）

import os

import numpy
import pandas

class FCT_R_Div_RStd:
    def __init__(self):
        self.factor_name = 'FCT_R_Div_RStd'

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

        # 修改为 pd.concat 批量合并方式
        new_columns = pandas.DataFrame(index=df.index)

        # 计算对数收益率
        new_columns['ret'] = numpy.log(df['close'] / df['close'].shift(1))

        # 计算 length 期累积收益率
        new_columns['cum_ret'] = new_columns['ret'].rolling(window=length).sum()

        # 计算 length 期收益率标准差
        new_columns['ret_std'] = new_columns['ret'].rolling(window=length).std()

        # 计算最终因子值
        new_columns[f'{factor_name}'] = new_columns['cum_ret'] / (new_columns['ret_std'] + 1e-10)

        # 合并进原始 df
        df = pandas.concat([df, new_columns], axis=1)

        # 返回结果（无日期）
        result = df[[f'{factor_name}']].copy()
        return result
