import pandas as pd
import numpy as np
import os

class FCT_Br_1:
    def __init__(self):
        self.factor_name = "FCT_Br_1" 

    def formula(self, param):
        df = param["df"].copy()
        k_line = param["k_line"]
        instrument = param["instrument"]
        length = param["length"]
        
        # 确保日期格式正确，避免日期格式化问题
        df["date"] = pd.to_datetime(df["date"], errors='coerce')  # 如果日期无效，则转换为NaT
        close_prev = df["close"].shift(1)  # 获取前一日收盘价
        up = np.maximum(df["high"] - close_prev, 0)  # 如果 high > close_prev，计算差值，否则为 0
        down = np.maximum(close_prev - df["low"], 0)  # 如果 close_prev > low，计算差值，否则为 0

        # 计算 br1 和 br2
        br1 = up.rolling(window=length).sum()  # 向前滚动求和
        br2 = down.rolling(window=length).sum()  # 向前滚动求和

        # 计算最终的因子值
        feature = (br1 - br2) / (br1 + br2)
        df[f'FCT_Br_1@{length}'] = feature

        # 保存文件路径
        save_path = f".quantative/data/{k_line}/{instrument}/{self.factor_name@{length}}.csv"
        os.makedirs(os.path.dirname(save_path), exist_ok=True)

        # 保存到 CSV，确保 date 列为字符串
        df[["date", f'FCT_Br_1@{length}']].to_csv(save_path, index=False)
        print(f"Factor {self.factor_name} saved to {save_path}")
