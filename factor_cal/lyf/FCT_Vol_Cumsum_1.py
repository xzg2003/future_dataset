# FCT_Vol_Cumsum_1：成交量累计因子，衡量从起始到当前的累计成交量

import os

import pandas

# 设置工作目录为当前脚本所在的目录
os.chdir(os.path.dirname(os.path.abspath(__file__)))


class FCT_Vol_Cumsum_1:
    def __init__(self):
        self.factor_name = 'FCT_Vol_Cumsum_1'

    def formula(self, param):
        # 从字典中提取 DataFrame
        df = param.get('df', None)
        if df is None:
            raise ValueError("no 'df' in param")

        # 从字典中提取 factor_name
        factor_name = param.get('factor_name', None)
        if factor_name is None:
            raise ValueError("no 'factor_name' in param")

        # 从字典中提取 length
        length = param.get('length', None)

        # 初始化 new_columns 用于统一管理中间变量
        new_columns = pandas.DataFrame(index=df.index)

        # 计算累积成交量
        new_columns[f'{factor_name}'] = df['volume'].rolling(window=length).sum()

        # 合并到主表
        df = pandas.concat([df, new_columns], axis=1)

        # 返回结果（无日期）
        result = df[[f'{factor_name}']].copy()
        return result
