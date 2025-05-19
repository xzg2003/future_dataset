import pandas as pd
import numpy as np

class FCT_Bias_1():
    def __init__(self):
        self.factor_name = 'FCT_Bias_1'
        self.require_length = True

    def MA(self, series, length):
        return series.rolling(window=length).mean()

    def formula(self, param):
        df = param['df'].copy()
        length = param['length']
        k_line = param['k_line']
        mindiff = param['mindiff']
        instrument = param['instrument']

        close_pre = df['close'].shift(1)
        close = df['close']
        high = df['high']
        low = df['low']

        tr1 = (high - close_pre).abs()
        tr2 = (high - low).abs()
        tr3 = (close_pre - low).abs()
        tr = pd.concat([tr1, tr2, tr3], axis=1).max(axis=1)

        ma_tr = self.MA(tr, length)
        close_tr = self.MA(close, length)

        # 构造 OUT
        out = pd.Series(0, index=df.index, dtype='float64')  # Explicitly set dtype to float64
        mask = (ma_tr >= mindiff) 
        out[mask] = (close - close_tr) / ma_tr[mask]
        mask = ((close - close_tr).isna()) | (ma_tr.isna())
        out[mask] = np.nan

        # 保存结果
        result = pd.DataFrame({
            'datetime': df['datetime'],
            self.factor_name + f'@{length}': out
        })

        save_path = f'./data/{k_line}/{instrument}/{self.factor_name}@{length}.csv'
        result.to_csv(save_path, index=False)