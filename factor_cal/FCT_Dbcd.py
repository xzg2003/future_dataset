# DBCD异同离差乖离率是一种技术指标。原理、构造方法、用法与乖离率相同。
# 优点是能够保持指标的紧密同步，并且线条光滑，信号明确，能够有效的过滤掉伪信号。

# 指标源内容查询自 http://cftsc.com/qushizhibiao/603.html
# BIAS1:=(CLOSE-MA(CLOSE,N))/MA(CLOSE,N);
# DIF:=(BIAS1-REF(BIAS1,M));
# DBCD1:SMA(DIF,T,1);
# MM:MA(DBCD1,5)
# N = 5, M = 16, T = 17

import pandas as pd

class FCT_Dbcd:
    def __init__(self):
        pass

    def formula(self, param):
        # 从字典中提取 DataFrame
        df = param.get('df', None)
        N = param.get('N', 5)  # 默认 N 为 5
        M = param.get('M', 16)   # 默认 M 为 16
        T = param.get('T', 17)  # 默认 T 为 17
        factor_name = 'FCT_Dbcd'

        if df is None:
            raise ValueError("参数 'param' 中缺少 'df' 键或其值为空")

        # 确保 df 是 pandas.DataFrame 类型
        if not isinstance(df, pd.DataFrame):
            raise TypeError("'df' 必须是 pandas.DataFrame 类型")

        # 检查必要的列
        required_columns = ['close']
        for col in required_columns:
            if col not in df.columns:
                raise ValueError(f"DataFrame 必须包含列 '{col}'")

        # 计算 BIAS1
        df['MA_Close_N'] = df['close'].rolling(window=N).mean()
        df['BIAS1'] = (df['close'] - df['MA_Close_N']) / df['MA_Close_N']

        # 计算 DIF
        df['REF_BIAS1'] = df['BIAS1'].shift(M)
        df['DIF'] = df['BIAS1'] - df['REF_BIAS1']

        # 计算 DBCD1
        df['DBCD1'] = df['DIF'].rolling(window=T).mean()

        # 计算 MM
        df['MM'] = df['DBCD1'].rolling(window=5).mean()

        # 保存最终因子值
        df[factor_name] = df['MM']

        # 返回结果
        if 'datetime' in df.columns:
            df = df.rename(columns={'datetime': 'date'})
        result = df[['date', factor_name]].copy()
        return result
