# FCT_Vol_DFive_1：成交量动量因子，衡量成交量在指定窗口内的变化幅度（如标准差或均值）

import pandas
import os

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

        # 计算成交量的标准差作为动量指标
        df[f'FCT_Vol_DFive_1@{length}'] = df['volume'].rolling(window=length).std()

        # 返回结果
        if 'datetime' in df.columns:
            df = df.rename(columns={'datetime': 'date'})
        result = df[['date', f'FCT_Vol_DFive_1@{length}']].copy()
        return result