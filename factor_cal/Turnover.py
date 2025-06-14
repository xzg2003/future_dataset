# FCT_Turnover : 换手率：成交量与未平仓合约量的比值
# FCT_Turnover = volume / open_interest

import pandas as pd

class Turnover:
    def __init__(self):
        pass

    def formula(self, param):
        # 从字典中提取 DataFrame
        df = param.get('df', None)
        factor_name = 'Turnover'

        if df is None:
            raise ValueError("参数 'param' 中缺少 'df' 键或其值为空")

        # 确保 df 是 pandas.DataFrame 类型
        if not isinstance(df, pd.DataFrame):
            raise TypeError("'df' 必须是 pandas.DataFrame 类型")

        # 检查必要的列
        required_columns = ['volume', 'open_interest']
        for col in required_columns:
            if col not in df.columns:
                raise ValueError(f"DataFrame 必须包含列 '{col}'")

        # 计算 Turnover
        df[factor_name] = df['volume'] / df['open_interest']

        # 返回结果
        if 'datetime' in df.columns:
            df = df.rename(columns={'datetime': 'date'})
        result = df[['date', factor_name]].copy()
        return result
