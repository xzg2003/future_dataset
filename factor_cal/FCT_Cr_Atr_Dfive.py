# FCT_Cr_Atr_Dfive : ATR 变化率的 5 日差分
# Cr_Atr_t = (ATR_t - ATR_{t-1}) / ATR_{t-1}
# FCT_Cr_Atr_Dfive = Cr_Atr_t - Cr_Atr_{t-5}

import pandas as pd

class FCT_Cr_Atr_Dfive:
    def __init__(self):
        pass

    def formula(self, param):
        # 从字典中提取 DataFrame
        df = param.get('df', None)
        length = 5  # 默认窗口长度为 5 天
        factor_name = 'FCT_Cr_Atr_Dfive'

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

        # 计算 ATR 变化率 (Cr_Atr_t)
        df['Cr_Atr_t'] = (df['ATR'] - df['ATR'].shift(1)) / df['ATR'].shift(1)

        # 计算 5 日差分
        df[factor_name] = df['Cr_Atr_t'] - df['Cr_Atr_t'].shift(length)

        # 返回结果
        if 'datetime' in df.columns:
            df = df.rename(columns={'datetime': 'date'})
        result = df[['date', factor_name]].copy()
        return result
