# FCT_R_Div_RStd:   收益率与波动率比值因子，衡量单位波动下的收益率（动量/风险调整）

import pandas
import numpy
import os

# 设置工作目录为当前脚本所在的目录
os.chdir(os.path.dirname(os.path.abspath(__file__)))

class FCT_R_Div_RStd:
    def __init__(self):
        self.factor_name = 'FCT_R_Div_RStd'

    def formula(self, param):
        # 从字典中提取 DataFrame
        df = param.get('df', None)
        if df is None:
            raise ValueError("no 'df' in param")
        if not isinstance(df, pandas.DataFrame):
            raise TypeError("df must be DataFrame")

        # 从字典中提取 length
        length = param.get('length', None)
        if length is None:
            raise ValueError("param missing 'length'")
        print(f"Using length: {length}")

        # 计算对数收益率
        df['ret'] = numpy.log(df['close'] / df['close'].shift(1))

        # 计算 length 期累积收益率
        df['cum_ret'] = df['ret'].rolling(window=length).sum()

        # 计算 length 期收益率标准差
        df['ret_std'] = df['ret'].rolling(window=length).std()

        # 计算收益率与波动率的比值
        df[f'FCT_R_Div_RStd@{length}'] = df['cum_ret'] / (df['ret_std'] + 1e-10)

        # 返回结果
        result = df[['datetime', f'FCT_R_Div_RStd@{length}']].copy()
        return result