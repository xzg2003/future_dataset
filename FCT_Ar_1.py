import pandas as pd
import numpy as np
import os

class FCT_Ar_1:
    def __init__(self):
        self.factor_name = "FCT_Ar_1"  

    def formula(self, param):
        df = param["df"].copy()
        k_line = param["k_line"]
        instrument = param["instrument"]
        length = param["length"]

        # 计算 up 和 down
        up = df["high"] - df["open"]
        down = df["open"] - df["low"]

        # 使用滚动窗口计算 AR1 和 AR2
        ar1 = up.rolling(window=length).sum()
        ar2 = down.rolling(window=length).sum()

        # 计算最终因子值
        feature = (ar1 - ar2) / (ar1 + ar2)

        # 确保日期列为正确的格式，转换为 datetime 格式
        df["date"] = pd.to_datetime(df["date"], errors='coerce')
        df[f'FCT_Ar_1@{length}'] = feature
        

        # 保存结果到 CSV
        save_path = f".quantative/data/{k_line}/{instrument}/{self.factor_name}@{length}.csv"
        os.makedirs(os.path.dirname(save_path), exist_ok=True)

        # 转换日期列为字符串并保存
        #df["date"] = df["date"].astype(str)
        df.to_csv(save_path, index=False)

        print(f"Factor {self.factor_name} saved to {save_path}")

