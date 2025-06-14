# FCT_Cr_1 : 收盘价变化率
# FCT_Cr_1[t] = (Close[t] - Close[t-1]) / Close[t-1]

import pandas as pd

class FCT_Cr_1:
    def __init__(self):
        pass

    def formula(self, param):
        # 从字典中提取 DataFrame
        df = param.get('df', None)
        factor_name = 'FCT_Cr_1'

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

        # 计算收盘价变化率 (FCT_Cr_1)
        df[factor_name] = (df['close'] - df['close'].shift(1)) / df['close'].shift(1)

        # 返回结果
        if 'datetime' in df.columns:
            df = df.rename(columns={'datetime': 'date'})
        result = df[['date', factor_name]].copy()
        return result
