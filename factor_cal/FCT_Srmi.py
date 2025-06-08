# FCT_Srmi：SRMI（相对动量指数）因子，衡量收盘价在指定窗口内的相对强弱位置

import pandas
import numpy
import os

# 设置工作目录为当前脚本所在的目录
os.chdir(os.path.dirname(os.path.abspath(__file__)))

class FCT_Srmi:
    def __init__(self):
        self.factor_name = 'FCT_Srmi'

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

        # 计算STMI：收盘价在窗口内的相对位置
        rolling_min = df['close'].rolling(window=length).min()
        rolling_max = df['close'].rolling(window=length).max()
        df[f'FCT_Srmi@{length}'] = (df['close'] - rolling_min) / (rolling_max - rolling_min + 1e-10)

        # 返回结果
        if 'datetime' in df.columns:
            df = df.rename(columns={'datetime': 'date'})
        result = df[['date', f'FCT_Srmi@{length}']].copy()
        return result