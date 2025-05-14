import pandas as pd
import numpy as np
import os

class FCT_Ac_Tr_1:
    def __init__(self):
        self.factor_name = "FCT_Ac_Tr_1" 

    def formula(self, param):
        
        df = param["df"].copy()
        k_line = param["k_line"]
        instrument = param["instrument"]
        length = param["length"]
        mindiff = param["mindiff"]

        close_pre = df["close"].shift(1)
        tr = np.maximum.reduce([
            np.abs(df["high"] - close_pre),
            np.abs(df["high"] - df["low"]),
            np.abs(close_pre - df["low"])
        ])
        tr_series=pd.Series(tr)
        ma_tr = tr_series.rolling(window=length).mean()

        mp = (df["high"] + df["low"]) / 2
        ao = mp.rolling(window=length).mean() - mp.rolling(window=4 * length).mean()
        ac = ao - ao.rolling(window=length).mean()
        out = np.where(ma_tr < mindiff, 0, ac / ma_tr)

        save_path = f"./data/{k_line}/{instrument}/{self.factor_name}.csv"
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        df[["date"]].assign(OUT=out).to_csv(save_path, index=False)
