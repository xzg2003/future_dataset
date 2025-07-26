# 资金流量指标，若收盘价在上半部分，且成交量放大，表示做多积极

import pandas


class FCT_Cmf_1:
    def __init__(self):
        self.factor_name = 'FCT_Cmf_1'

    def formula(self, param):

        # 从参数字典中提取 DataFrame
        df = param.get('df', None)
        if df is None:
            raise ValueError("no 'df' in param")

        # 从参数字典中读取 length
        length = param.get('length', None)
        if length is None:
            raise ValueError("param missing 'length'")

        # 从参数字典中读取 factor_name
        factor_name = param.get('factor_name', None)
        if factor_name is None:
            raise ValueError("param missing 'factor_name'")

        # 修改为 pd.concat 批量合并方式
        new_columns = pandas.DataFrame(index=df.index)

        # 计算 MFV
        new_columns['MFV'] = ((2 * df['close'] - df['low'] - df['high']) / (df['high'] - df['low'])) * df['volume']

        # 计算 CMF 所需滚动和
        rolling_sum_mfv = new_columns['MFV'].rolling(window=length).sum().fillna(0)
        rolling_sum_volume = df['volume'].rolling(window=length).sum().fillna(0)

        # 最终因子计算
        new_columns[f'{factor_name}'] = rolling_sum_mfv / rolling_sum_volume

        # 合并进原始 df
        df = pandas.concat([df, new_columns], axis=1)

        # 返回结果（无日期）
        result = df[[f'{factor_name}']].copy()
        return result
