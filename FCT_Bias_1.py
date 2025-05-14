import pandas as pd
import numpy as np
import os

class FCT_Bias_1:
    def __init__(self):
        self.factor_name = "FCT_Bias_1" 

    def formula(self, param):
        df = param["df"].copy()
        k_line = param["k_line"]
        instrument = param["instrument"]
        length = param["length"]
        mindiff = float(param["mindiff"])  # 确保 mindiff 为浮动值

        # 确保日期列为正确的格式，转换为 datetime 格式
        df["date"] = pd.to_datetime(df["date"], errors='coerce')
        close_pre = df["close"].shift(1)

        # 计算 TR（真实波动范围）
        tr = np.maximum.reduce([
            np.abs(df["high"] - close_pre),
            np.abs(df["high"] - df["low"]),
            np.abs(close_pre - df["low"])
        ])

        # 计算移动平均
        ma_tr = pd.Series(tr).rolling(window=length).mean()
        ma_close = df["close"].rolling(window=length).mean()

        # 计算信号
        signal = np.where(ma_tr < mindiff, 0, (df["close"] - ma_close) / ma_tr)

        # 添加因子列
        factor_col = f"{self.factor_name}@{length}"
        df[factor_col] = signal

        # 保存结果到 CSV（只保留 date 和计算结果列）
        save_path = f".quantative/data/{k_line}/{instrument}/{factor_col}.csv"
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        df[["date", factor_col]].to_csv(save_path, index=False)
        print(f"Factor {self.factor_name} saved to {save_path}")
