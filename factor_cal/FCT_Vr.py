# FCT_Vr：量比因子，衡量当前成交量与过去一段时间平均成交量的比值

import os

import pandas

# 设置工作目录为当前脚本所在的目录
os.chdir(os.path.dirname(os.path.abspath(__file__)))


class FCT_Vr:
    def __init__(self):
        self.factor_name = 'FCT_Vr'

    def formula(self, param):
        # 从字典中提取 DataFrame
        df = param.get('df', None)
        if df is None:
            raise ValueError("no 'df' in param")
        if not isinstance(df, pandas.DataFrame):
            raise TypeError("df must be DataFrame")

        # 从字典中读取 length
        length = param.get('length', None)
        if length is None:
            raise ValueError("param missing 'length'")
        print(f"Using length: {length}")

        # 确保索引有序
        if not df.index.is_monotonic_increasing:
            df = df.sort_index()

        # 提取并计算成交指标
        volume = df['volume'].clip(lower=0)  # 确保成交量非负

        # 计算平均成交量
        avg_vol = volume.rolling(window=length).mean().clip(lower=1e-5)  # 设置最小值防止除以零

        # 计算量比因子
        new_column = volume / avg_vol
        new_column.name = f'{self.factor_name}@{length}'

        # 合并进原始 df
        df = pandas.concat([df, new_column], axis=1)

        # 返回结果（无日期）
        result = df[[f'FCT_Vr@{length}']].copy()
        return result
