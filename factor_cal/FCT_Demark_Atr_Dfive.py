# FCT_Demark_Vol_Dfive: vol 值在 5 天长度内的 Demarker 指标

import pandas as pd

class FCT_Demark_Atr_Dfive:
    def __init__(self):
        pass

    def formula(self, param):
        # 从字典中提取 DataFrame
        df = param.get('df', None)
        length = 5  # 窗口长度为 5 天
        factor_name = 'FCT_Demark_Atr_Dfive'

        if df is None:
            raise ValueError("参数 'param' 中缺少 'df' 键或其值为空")

        # 确保 df 是 pandas.DataFrame 类型
        if not isinstance(df, pd.DataFrame):
            raise TypeError("'df' 必须是 pandas.DataFrame 类型")

        # 检查必要的列
        required_columns = ['high', 'low', 'close']
        for col in required_columns:
            if col not in df.columns:
                raise ValueError(f"DataFrame 必须包含列 '{col}'")

        # 计算 TR（真实波幅）
        df['TR'] = df[['high', 'low', 'close']].apply(
            lambda row: max(row['high'] - row['low'], 
                            abs(row['high'] - row['close']), 
                            abs(row['low'] - row['close'])),
            axis=1
        )

        # 计算 ATR（平均真实波幅）
        df['ATR'] = df['TR'].rolling(window=length).mean()

        # 计算 Demarker 指标
        df['DeMax'] = df['ATR'].diff().clip(lower=0)  # ATR 的正变化
        df['DeMin'] = -df['ATR'].diff().clip(upper=0)  # ATR 的负变化
        df['DeMax_Sum'] = df['DeMax'].rolling(window=length).sum()
        df['DeMin_Sum'] = df['DeMin'].rolling(window=length).sum()
        df[factor_name] = df['DeMax_Sum'] / (df['DeMax_Sum'] + df['DeMin_Sum'])

        # 返回结果
        if 'datetime' in df.columns:
            df = df.rename(columns={'datetime': 'date'})
        result = df[['date', factor_name]].copy()
        return result
