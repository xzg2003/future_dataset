# tr：波动幅度，当前k线的高低点与上根k线收盘价三者两两做差，取绝对值的最大作为tr波幅

import pandas

class Tr:
    def __init__(self):
        self.factor_name = 'Tr'     # 设置因子的名称


    def formula(self, param):
        # 从字典中提取DataFrame
        df = param.get('df', None)
        if df is None:
            raise ValueError("参数 'param' 中缺少 'df' 键或其值为空")

        # 确保df是pandas.DataFrame类型
        if not isinstance(df, pandas.DataFrame):
            raise TypeError("'df' 必须是 pandas.DataFrame 类型")

        # 前一k线的收盘价
        df['close_pre'] = df['close'].shift(1)

        # 逐行取三种差值的最大值作为 TR
        df['Tr'] = df[['close_pre', 'high', 'low']].apply(
            lambda row: max(row['high'] - row['close_pre'], row['high'] - row['low'], row['close_pre'] - row['low']),
            axis=1
        )

        # 返回包含日期和Tr的结果
        result = df[['trading_date', 'Tr']].copy()
        return result

