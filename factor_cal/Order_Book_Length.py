# 订单簿深度因子 前五档买卖订单量之和 
# 由于缺少 bid_size 和 ask_size 而暂时无法计算

import pandas as pd

class Order_Book_Length:
    def __init__(self):
        pass

    def formula(self, param):
        # 从字典中提取 DataFrame
        df = param.get('df', None)
        factor_name = 'Order_Book_Length'

        if df is None:
            raise ValueError("参数 'param' 中缺少 'df' 键或其值为空")

        # 确保 df 是 pandas.DataFrame 类型
        if not isinstance(df, pd.DataFrame):
            raise TypeError("'df' 必须是 pandas.DataFrame 类型")

        # 检查必要的列
        if 'bid_size' not in df.columns or 'ask_size' not in df.columns:
            raise ValueError("DataFrame 必须包含 'bid_size' 和 'ask_size' 列")

        # 计算 Order Book Length 因子
        # Order Book Length = bid_size + ask_size
        df[factor_name] = df['bid_size'] + df['ask_size']

        # 返回结果
        if 'datetime' in df.columns:
            df = df.rename(columns={'datetime': 'date'})
        result = df[['date', factor_name]].copy()
        return result
