# FCT_Cr_Vol_Dfive : 成交量变化率的 5 日差分
# Cr_Vol_t = (Vol_t - Vol_{t-1}) / Vol_{t-1}
# FCT_Cr_Vol_Dfive = Cr_Vol_t - Cr_Vol_{t-5}

import pandas as pd

class FCT_Cr_Vol_Dfive:
    def __init__(self):
        pass

    def formula(self, param):
        # 从字典中提取 DataFrame
        df = param.get('df', None)
        length = 5  # 默认窗口长度为 5 天
        factor_name = 'FCT_Cr_Vol_Dfive'

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

        # 计算成交量变化率 
        df['Cr_Vol_t'] = (df['volume'] - df['volume'].shift(1)) / df['volume'].shift(1)

        # 计算 5 日差分
        df[factor_name] = df['Cr_Vol_t'] - df['Cr_Vol_t'].shift(length)

        # 返回结果
        if 'datetime' in df.columns:
            df = df.rename(columns={'datetime': 'date'})
        result = df[['date', factor_name]].copy()
        return result
