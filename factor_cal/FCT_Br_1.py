import pandas as pd
import numpy as np

class FCT_Br_1():
    def __init__(self):
        self.factor_name = 'FCT_Br_1'
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
        close_pre = df['close'].shift(1)

        # 计算 up 和 down
        up = (high - close_pre).clip(lower=0)
        down = (close_pre - low).clip(lower=0)

        # 计算 br1 和 br2
        br1 = up.rolling(window=length).sum()
        br2 = down.rolling(window=length).sum()

        # 计算特征值
        out = (br1 + br2) / (br1 - br2)

        # 保存结果
        result = pd.DataFrame({
            'datetime': df['datetime'],
            self.factor_name + f'@{length}': out
        })

        save_path = f'./data/{k_line}/{instrument}/{self.factor_name}@{length}.csv'
        result.to_csv(save_path, index=False)
