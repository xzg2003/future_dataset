# 资金流量指标，若收盘价在上半部分，且成交量放大，表示做多积极

import pandas

class FCT_Cmf_1:
    def __init__(self):
        pass

    def formula(self, param):
    # 从字典中提取DataFrame
        df = param.get('df', None)
        length = param.get('length', 5)
        factor_name = f'FCT_Cmf_1@{length}'

        if df is None:
            raise ValueError("参数 'param' 中缺少 'df' 键或其值为空")

        # 确保df是pandas.DataFrame类型
        if not isinstance(df, pandas.DataFrame):
            raise TypeError("'df' 必须是 pandas.DataFrame 类型")

        # 计算MFV
        df['MFV'] = ((2 * df['close'] - df['low'] - df['high']) / (df['high'] - df['low'])) * df['volume']

        # 计算CMF
        df[factor_name] = df['MFV'].rolling(window=length).sum() / df['volume'].rolling(window=length).sum()

        # 返回结果
        result = df[ factor_name].copy()
        return result