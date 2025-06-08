# FCT_Vr：量比因子，衡量当前成交量与过去一段时间平均成交量的比值

import pandas
import numpy
import os

# 设置工作目录为当前脚本所在的目录
os.chdir(os.path.dirname(os.path.abspath(__file__)))

class FCT_Vr:
    def __init__(self):
        self.factor_name = 'FCT_Vr'

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

        # 计算过去 length 期的平均成交量
        avg_vol = df['volume'].rolling(window=length).mean()

        # 计算量比
        df[f'FCT_Vr@{length}'] = df['volume'] / (avg_vol + 1e-10)

        # 返回结果
        if 'datetime' in df.columns:
            df = df.rename(columns={'datetime': 'date'})
        result = df[['date', f'FCT_Vr@{length}']].copy()
        return result