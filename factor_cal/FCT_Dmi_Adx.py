# FCT_Dmi_Adxr 因子：DX 的滚动均值
# 计算 +DM 和 -DM：分别计算正方向移动和负方向移动。
# 计算 ATR（平均真实波幅）：用滚动窗口计算 TR 的均值。
# 计算 +DI 和 -DI：使用 +DM 和 -DM 的均值除以 ATR，并乘以 100。
# 计算 DX 和 ADX：DX 表示方向性指标，ADX 是 DX 的滚动均值。

import pandas as pd

class FCT_Dmi_Adx:
    def __init__(self):
        pass

    def formula(self, param):
        # 从字典中提取 DataFrame
        df = param.get('df', None)
        length = param.get('length', 14)
        factor_name = f'FCT_Dmi_Adx@{length}'

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

        # 计算 TR（真实波幅）
        df['Tr'] = param.get('tr', None)
        if df['Tr'] is None:
            raise ValueError("参数 'param' 中缺少 'tr' 键或其值为空")

        # 计算 +DM 和 -DM
        df['+DM'] = df['high'].diff().clip(lower=0)
        df['-DM'] = df['low'].diff().clip(upper=0).abs()

        # 计算 ATR（平均真实波幅）
        df['ATR'] = df['Tr'].rolling(window=length).mean()

        # 计算 +DI 和 -DI
        df['+DI'] = (df['+DM'].rolling(window=length).mean() / df['ATR']) * 100
        df['-DI'] = (df['-DM'].rolling(window=length).mean() / df['ATR']) * 100

        # 计算 DX
        df['DX'] = (abs(df['+DI'] - df['-DI']) / (df['+DI'] + df['-DI'])) * 100

        # 计算 ADX
        df[factor_name] = df['DX'].rolling(window=length).mean()

        # 返回结果
        if 'datetime' in df.columns:
            df = df.rename(columns={'datetime': 'date'})
        result = df[['date', factor_name]].copy()
        return result
