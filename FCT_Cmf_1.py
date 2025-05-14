import pandas as pd
import numpy as np
import os

class FCT_Cmf_1:
    def __init__(self):
        self.factor_name = "FCT_Cmf_1" 

    def formula(self, param):
        df = param["df"].copy()
        k_line = param["k_line"]
        instrument = param["instrument"]
        length = param["length"]

        # 确保日期列为正确的格式，转换为 datetime 格式
        df["date"] = pd.to_datetime(df["date"], errors='coerce')

        # 计算 MFV (Money Flow Volume)
        mfv_numerator = 2 * df["close"] - df["low"] - df["high"]
        mfv_denominator = df["high"] - df["low"]
        mfv_denominator[mfv_denominator == 0] = 1  # 避免除以0
        mfv = (mfv_numerator / mfv_denominator) * df["vol"]

        # 计算 CMF (Chaikin Money Flow)
        cmf_numerator = mfv.rolling(window=length).sum()
        cmf_denominator = df["vol"].rolling(window=length).sum()
        cmf_denominator[cmf_denominator == 0] = 1  # 避免除以0
        cmf = cmf_numerator / cmf_denominator

        # 添加因子列
        factor_col = f'{self.factor_name}@{length}'
        df[factor_col] = cmf

        # 保存结果到 CSV（只保留 date 和计算结果列）
        save_path = f".quantative/data/{k_line}/{instrument}/{factor_col}.csv"
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        df[["date", factor_col]].to_csv(save_path, index=False)
        print(f"Factor {self.factor_name} saved to {save_path}")
