# TSMOM: 常见的动量因子，用于衡量资产在过去一段时间内的累积收益情况
# 后续很多计算器需要调用 TSMOM 的计算结果

import pandas
import numpy
import os

# 设置工作目录为当前脚本所在的目录
os.chdir(os.path.dirname(os.path.abspath(__file__)))

class TSMOM:
    def __init__(self):
        self.factor_name = 'TSMOM'

    def formula(self, param):
        # 从字典中提取 DataFrame
        df = param.get('df', None)
        if df is None:
            raise ValueError("no 'df' in param")

        # 确保 df 是 pandas.DataFrame 类型
        if not isinstance(df, pandas.DataFrame):
            raise TypeError("df must be DataFrame")

        """
        从字典中读取 length
        """
        length = param.get('length', None)
        if length is None:
            raise ValueError("param missing 'length'")
        print(f"Using length:{length}")

        """
        计算 TSMOM 动量因子
        这里取收盘价进行计算
        """
        df[f'TSMOM@{length}'] = df['close'].pct_change(periods=length)
        df[f'TSMOM@{length}'] = df[f'TSMOM@{length}'].replace([numpy.inf, -numpy.inf], numpy.nan).fillna(0)

        # 返回结果
        if 'datetime' in df.columns:
            df = df.rename(columns={'datetime': 'date'})
        result = df[['date', f'TSMOM@{length}']].copy()
        return result