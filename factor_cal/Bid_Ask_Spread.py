# Bid_Ask_Spread：买卖差价因子，定义为（买一价 - 卖一价）/ 中间价
# 暂时无法计算，似乎是缺少 bid1 和 ask1 列数据所致

import pandas as pd

class Bid_Ask_Spread:
    def __init__(self):
        pass

    def formula(self, param):
        # 从字典中提取DataFrame
        df = param.get('df', None)

        if df is None:
            raise ValueError("参数 'param' 中缺少 'df' 键或其值为空")

        # 确保df是pandas.DataFrame类型
        if not isinstance(df, pd.DataFrame):
            raise TypeError("'df' 必须是 pandas.DataFrame 类型")

        # 计算买卖差价因子
        df['mid_price'] = (df['bid1'] + df['ask1']) / 2  # 中间价
        df['Bid_Ask_Spread'] = (df['ask1'] - df['bid1']) / df['mid_price']

        # 返回结果
        if 'datetime' in df.columns:
            df = df.rename(columns={'datetime': 'date'})
        result = df[['date', 'Bid_Ask_Spread']].copy()
        return result