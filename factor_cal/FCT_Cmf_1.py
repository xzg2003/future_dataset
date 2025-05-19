import pandas as pd
import numpy as np

class FCT_Cmf_1():
    def __init__(self):
        self.factor_name = 'FCT_Cmf_1'
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
        close = df['close']
        volume = df['volume']

        # 计算 MFV
        mfv = ((close - low) - (high - close)) / (high - low) * volume

        # 计算 CMF
        cmf = mfv.rolling(window=length).sum() / volume.rolling(window=length).sum()

        # 构造 OUT
        out = cmf

        # 保存结果
        result = pd.DataFrame({
            'datetime': df['datetime'],
            self.factor_name + f'@{length}': out
        })

        save_path = f'./data/{k_line}/{instrument}/{self.factor_name}@{length}.csv'
        result.to_csv(save_path, index=False)
