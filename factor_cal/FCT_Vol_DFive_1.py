# FCT_Vol_DFive_1：成交量动量因子，衡量成交量在指定窗口内的变化幅度（如标准差或均值）

import os

import pandas

# 设置工作目录为当前脚本所在的目录
os.chdir(os.path.dirname(os.path.abspath(__file__)))


class FCT_Vol_DFive_1:
    def __init__(self):
        self.factor_name = 'FCT_Vol_DFive_1'

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

        # 初始化 new_columns 用于集中管理所有新列
        new_columns = pandas.DataFrame(index=df.index)

        # 计算成交量标准差作为动量指标
        new_columns[f'FCT_Vol_DFive_1@{length}'] = df['volume'].rolling(window=length).std()

        # 合并到原始 df（一次性操作）
        df = pandas.concat([df, new_columns], axis=1)

        # 返回结果（无日期）
        result = df[[f'FCT_Vol_DFive_1@{length}']].copy()
        return result
