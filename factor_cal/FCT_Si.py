# FCT_Si：SI（波动率指标）因子，衡量收盘价的绝对变化幅度的均值

import pandas
import numpy
import os

# 设置工作目录为当前脚本所在的目录
os.chdir(os.path.dirname(os.path.abspath(__file__)))

class FCT_Si:
    def __init__(self):
        self.factor_name = 'FCT_Si'

    def formula(self, param):
        # 从字典中提取 DataFrame
        df = param.get('df', None)
        if df is None:
            raise ValueError("no 'df' in param")
        if not isinstance(df, pandas.DataFrame):
            raise TypeError("df must be DataFrame")

        # 从字典中读取 length
        length = param.get('length', None)
        if length is None:
            raise ValueError("param missing 'length'")
        print(f"Using length: {length}")

        """
        # 计算收盘价的绝对变化幅度
        df['abs_diff'] = numpy.abs(df['close'].diff())

        # 计算 SI 指标（绝对变化幅度的均值）
        df[f'FCT_Si@{length}'] = df['abs_diff'].rolling(window=length).mean()
        """

        new_columns = pandas.DataFrame(index=df.index)

        # 计算收盘价的绝对变化幅度
        new_columns['abs_diff'] = numpy.abs(df['close'].diff())

        # 计算 SI 指标（绝对变化幅度的均值）
        new_columns[f'FCT_Si@{length}'] = new_columns['abs_diff'].rolling(window=length).mean()

        # 合并进原始 df
        df = pandas.concat([df, new_columns], axis=1)

        # 返回结果
        if 'datetime' in df.columns:
            df = df.rename(columns={'datetime': 'date'})
        result = df[['date', f'FCT_Si@{length}']].copy()
        return result