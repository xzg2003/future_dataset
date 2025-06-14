# FCT_Donchian_Vol_Dfive 因子
# 计算 Donchian 通道：
#   上轨：最近 5 天的最高成交量。
#   下轨：最近 5 天的最低成交量。
#   宽度：上轨减去下轨。
# 因子值为(当前成交量 - 过去5日最低成交量) 与 Donchian 通道宽度比值。

import pandas as pd

class FCT_Donchian_Vol_Dfive:
    def __init__(self):
        pass

    def formula(self, param):
        # 从字典中提取 DataFrame
        df = param.get('df', None)
        length = 5
        factor_name = 'FCT_Donchian_Vol_Dfive'

        if df is None:
            raise ValueError("参数 'param' 中缺少 'df' 键或其值为空")

        # 确保 df 是 pandas.DataFrame 类型
        if not isinstance(df, pd.DataFrame):
            raise TypeError("'df' 必须是 pandas.DataFrame 类型")

        # 检查必要的列
        required_columns = ['volume']
        for col in required_columns:
            if col not in df.columns:
                raise ValueError(f"DataFrame 必须包含列 '{col}'")

        # 计算 Donchian 通道的上轨和下轨
        df['Donchian_High'] = df['volume'].rolling(window=length).max()
        df['Donchian_Low'] = df['volume'].rolling(window=length).min()

        # 计算 Donchian 通道的宽度
        df['Donchian_Width'] = df['Donchian_High'] - df['Donchian_Low']

        # 计算因子值：(当前成交量 - 过去5日最低成交量) / Donchian 通道的宽度
        df[factor_name] = (df['volume'] - df['Donchian_Low']) / df['Donchian_Width']

        # 返回结果
        if 'datetime' in df.columns:
            df = df.rename(columns={'datetime': 'date'})
        result = df[['date', factor_name]].copy()
        return result
