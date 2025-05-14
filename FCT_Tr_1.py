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
