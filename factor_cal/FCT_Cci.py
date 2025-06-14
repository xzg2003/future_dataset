# FCT_Cci : 商品通道指数 (CCI)
# CCI = (TP - MA(TP, Length)) / (0.015 * MD)
# MD = (1/Length) * Σ|TP - MA(TP, Length)|
# TP = (High + Low + Close) / 3

import pandas as pd

class FCT_Cci:
    def __init__(self):
        pass

    def formula(self, param):
        # 从字典中提取 DataFrame
        df = param.get('df', None)
        length = param.get('length', 20)  # 默认窗口长度为 20
        factor_name = f'FCT_Cci@{length}'

        if df is None:
            raise ValueError("参数 'param' 中缺少 'df' 键或其值为空")

        # 确保 df 是 pandas.DataFrame 类型
        if not isinstance(df, pd.DataFrame):
            raise TypeError("'df' 必须是 pandas.DataFrame 类型")

        # 检查必要的列
        required_columns = ['high', 'low', 'close']
        for col in required_columns:
            if col not in df.columns:
                raise ValueError(f"DataFrame 必须包含列 '{col}'")

        # 计算 TP
        df['Typical_Price'] = (df['high'] + df['low'] + df['close']) / 3

        # 计算 MA(TP, N)
        df['TP_MA'] = df['Typical_Price'].rolling(window=length).mean()

        # 计算 Mean Deviation
        def mean_deviation(series):
            mean = series.mean()
            return (series - mean).abs().mean()

        df['Mean_Deviation'] = df['Typical_Price'].rolling(window=length).apply(mean_deviation, raw=False)

        # 计算 CCI
        df[factor_name] = (df['Typical_Price'] - df['TP_MA']) / (0.015 * df['Mean_Deviation'])

        # 返回结果
        if 'datetime' in df.columns:
            df = df.rename(columns={'datetime': 'date'})
        result = df[['date', factor_name]].copy()
        return result
