# 资金流量指标，若收盘价在上半部分，且成交量放大，表示做多积极

import pandas

class FCT_Cmf_1:
    def __init__(self):
        self.factor_name = 'FCT_Cmf_1'

    def formula(self, param):

        # 从字典中提取 DataFrame
        df = param.get('df', None)
        if df is None:
            raise ValueError("no 'df' in param")

        # 确保 df 是 pandas.DataFrame 类型
        if not isinstance(df, pandas.DataFrame):
            raise TypeError("df must be DataFrame")

        """
        从字典中读取 length
        获取 instrument 名称，用于提取mindiff中的数据
        """
        length = param.get('length', None)
        if length is None:
            raise ValueError("param missing 'length'")
        print(f"Using length: {length}")

        # 计算MFV
        df['MFV'] = ((2 * df['close'] - df['low'] - df['high']) / (df['high'] - df['low'])) * df['volume']

        # 计算CMF
        rolling_sum_mfv     = df['MFV'].rolling(window=length).sum().fillna(0)
        rolling_sum_volume  = df['volume'].rolling(window=length).sum().fillna(0)

        # 计算最终的值
        df[f'FCT_Cmf_1@{length}'] = rolling_sum_mfv / rolling_sum_volume

        # 返回结果
        result = df[['datetime', f'FCT_Cmf_1@{length}']].copy()
        return result