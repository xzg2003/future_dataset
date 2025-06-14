# FCT_Close_1_1 : 当前时刻的前1期收盘价（Close[t-1]）相对于前2期收盘价（Close[t-2]）的变化率
# 这相当于是“前一期的收益率”，或者 Close 的 Ref_1 的收益率形式。

import pandas as pd

class FCT_Close_1_1:
    def __init__(self):
        pass

    def formula(self, param):
        # 从字典中提取 DataFrame
        df = param.get('df', None)
        factor_name = 'FCT_Close_1_1'

        if df is None:
            raise ValueError("参数 'param' 中缺少 'df' 键或其值为空")

        # 确保 df 是 pandas.DataFrame 类型
        if not isinstance(df, pd.DataFrame):
            raise TypeError("'df' 必须是 pandas.DataFrame 类型")

        # 检查必要的列
        required_columns = ['close']
        for col in required_columns:
            if col not in df.columns:
                raise ValueError(f"DataFrame 必须包含列 '{col}'")

        # 计算收盘价的 1 日变化率 (FCT_Close_1_1)
        df[factor_name] = (df['close'].shift(1) - df['close'].shift(2)) / df['close'].shift(2)

        # 返回结果
        if 'datetime' in df.columns:
            df = df.rename(columns={'datetime': 'date'})
        result = df[['date', factor_name]].copy()
        return result
