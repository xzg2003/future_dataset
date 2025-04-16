import pandas as pd
import numpy as np
import os

class FCT_Tr_1:
    def __init__(self):
        self.factor_name = "FCT_Tr_1" 
    
    def formula(self, param):
        df = param["df"].copy()
        k_line = param["k_line"]
        instrument = param["instrument"]
        
        high_low = df["high"] - df["low"]
        high_close = np.abs(df["high"] - df["close"].shift(1))
        low_close = np.abs(df["low"] - df["close"].shift(1))
        df["Tr"] = np.maximum.reduce([high_low, high_close, low_close])
        
        save_path = f"./data/{k_line}/{instrument}/{self.factor_name}.csv"
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        df[["date", "Tr"]].to_csv(save_path, index=False)

class FCT_Bias_1:
    def __init__(self):
        self.factor_name = "FCT_Bias_1" 

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
        ma_tr = tr.rolling(window=length).mean()

        ma_close = df["close"].rolling(window=length).mean()
        signal = np.where(ma_tr < mindiff, 0, (df["close"] - ma_close) / ma_tr)

        save_path = f"./data/{k_line}/{instrument}/{self.factor_name}.csv"
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        df[["date"]].assign(OUT=signal).to_csv(save_path, index=False)

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
        ma_tr = tr.rolling(window=length).mean()

        mp = (df["high"] + df["low"]) / 2
        ao = mp.rolling(window=length).mean() - mp.rolling(window=4 * length).mean()
        ac = ao - ao.rolling(window=length).mean()
        out = np.where(ma_tr < mindiff, 0, ac / ma_tr)

        save_path = f"./data/{k_line}/{instrument}/{self.factor_name}.csv"
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        df[["date"]].assign(OUT=out).to_csv(save_path, index=False)

class FCT_Ar_1:
    def __init__(self):
        self.factor_name = "FCT_Ar_1"  

    def formula(self, param):
        df = param["df"].copy()
        k_line = param["k_line"]
        instrument = param["instrument"]
        length = param["length"]

        up = df["high"] - df["open"]
        down = df["open"] - df["low"]
        ar1 = up.rolling(window=length).sum()
        ar2 = down.rolling(window=length).sum()
        feature = (ar1 - ar2) / (ar1 + ar2)

        save_path = f"./data/{k_line}/{instrument}/{self.factor_name}.csv"
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        df[["date"]].assign(OUT=feature).to_csv(save_path, index=False)

class FCT_Br_1:
    def __init__(self):
        self.factor_name = "FCT_Br_1" 

    def formula(self, param):
        df = param["df"].copy()
        k_line = param["k_line"]
        instrument = param["instrument"]
        length = param["length"]
        close_prev = df["close"].shift(1)
        up = np.where(df["high"] - close_prev > 0, df["high"] - close_prev, 0)
        down = np.where(close_prev - df["low"] > 0, close_prev - df["low"], 0)
        br1 = up.rolling(window=length).sum()
        br2 = down.rolling(window=length).sum()
        feature = (br1 - br2) / (br1 + br2)

        save_path = f"./data/{k_line}/{instrument}/{self.factor_name}.csv"
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        df[["date"]].assign(OUT=feature).to_csv(save_path, index=False)

class FCT_Cmf_1:
    def __init__(self):
        self.factor_name = "FCT_Cmf_1" 

    def formula(self, param):
        df = param["df"].copy()
        k_line = param["k_line"]
        instrument = param["instrument"]
        length = param["length"]

        mfv_numerator = 2 * df["close"] - df["low"] - df["high"]
        mfv_denominator = df["high"] - df["low"]
        mfv_denominator = np.where(mfv_denominator == 0, 1, mfv_denominator)
        mfv = (mfv_numerator / mfv_denominator) * df["vol"]
        cmf_numerator = mfv.rolling(window=length).sum()
        cmf_denominator = df["vol"].rolling(window=length).sum()
        cmf_denominator = np.where(cmf_denominator == 0, 1, cmf_denominator)
        cmf = cmf_numerator / cmf_denominator

        save_path = f"./data/{k_line}/{instrument}/{self.factor_name}.csv"
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        df[["date"]].assign(OUT=cmf).to_csv(save_path, index=False)
