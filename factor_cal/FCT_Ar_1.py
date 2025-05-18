import pandas as pd
import numpy as np

class FCT_Ar_1():
    def __init__(self):
        self.factor_name = 'FCT_Ar_1'
        self.require_length = True

    def MA(self, series, length):
        return series.rolling(window=length).mean()

    def formula(self, param):
        df = param['df'].copy()
        length = param['length']
        k_line = param['k_line']
        instrument = param['instrument']

        high = df['high']
        low = df['low']
        open_ = df['open']

        # 计算 up 和 down
        up = (high - open_).clip(lower=0)
        down = (open_ - low).clip(lower=0)

        # 计算 ar1 和 ar2
        ar1 = up.rolling(window=length).sum()
        ar2 = down.rolling(window=length).sum()

        # 计算特征值
        out = (ar1 + ar2) / (ar1 - ar2).replace(0, np.nan)
        # 保存结果
        result = pd.DataFrame({
            'datetime': df['datetime'],
            self.factor_name + f'@{length}': out
        })

        save_path = f'./data/{k_line}/{instrument}/{self.factor_name}@{length}.csv'
        result.to_csv(save_path, index=False)