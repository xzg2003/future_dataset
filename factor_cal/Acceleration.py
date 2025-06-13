# Acceleration: 动量变化率。调用了 TSMOM 的计算结果

import pandas
import numpy
import os

# 设置工作目录为当前脚本所在的目录
os.chdir(os.path.dirname(os.path.abspath(__file__)))

class Acceleration:
    def __init__(self):
        self.factor_name = 'Acceleration'

    def formula(self, param):
        # 从字典中提取 DataFrame
        df = param.get('df', None)
        if df is None:
            raise ValueError("no 'df' in param")

        # 确保 df 是 pandas.DataFrame 类型
        if not isinstance(df, pandas.DataFrame):
            raise TypeError("df must be DataFrame")

        """
        从字典中读取 length
        获取 instrument 名称，用于提取mindiff中的数据
        """
        length = param.get('length', None)
        if length is None:
            raise ValueError("param missing 'length'")
        print(f"Using length: {length}")

        # 获取instrument
        instrument = param.get('instrument', None)
        if instrument is None:
            raise ValueError("param miss instrument")

        # 获取k_line_type
        k_line_type = param.get('k_line_type', None)
        if k_line_type is None:
            raise ValueError("param missing instrument")

        TSMOM_data_path = os.path.join(os.path.dirname(__file__), f'../data/{k_line_type}/{instrument}/TSMOM@{length}.csv')
        TSMOM_data_path = os.path.normpath(TSMOM_data_path)
        if not os.path.exists(TSMOM_data_path):
            raise FileNotFoundError(f"TSMOM_data_path not found:{TSMOM_data_path}")

        """
        TSMOM_df = pandas.read_csv(TSMOM_data_path)
        # TSMOM@{length}.csv 有 datetime 和 TSMOM@{length} 两列，且与主 df 按 datetime 对齐
        if 'datetime' in df.columns and 'datetime' in TSMOM_df.columns:
            df = df.merge(TSMOM_df[['datetime', f'TSMOM@{length}']], on='datetime', how='left')
        else:
            # 如果没有 datetime 列，直接用index对齐
            df[f'TSMOM@{length}'] = TSMOM_df[f'TSMOM@{length}']

        # df[f'Acceleration@{length}'] = df[f'TSMOM@{length}'].pct_change(periods=length)

        # 修改为 pd.concat 批量合并方式
        new_columns = pandas.DataFrame({
            f'Acceleration@{length}': df[f'TSMOM@{length}'].pct_change(periods=length)
        }, index=df.index)

        df = pandas.concat([df, new_columns], axis=1)
        """

        TSMOM_df = pandas.read_csv(TSMOM_data_path)
        if 'datetime' in df.columns and 'datetime' in TSMOM_df.columns:
            df = df.merge(TSMOM_df[['datetime', f'TSMOM@{length}']], on='datetime', how='left')
        else:
            df[f'TSMOM@{length}'] = TSMOM_df[f'TSMOM@{length}']

        # 使用 NumPy 数组计算 pct_change
        tsmom_values = df[f'TSMOM@{length}'].values
        acceleration_values = numpy.empty_like(tsmom_values)
        acceleration_values[:length] = numpy.nan
        acceleration_values[length:] = tsmom_values[length:] / (tsmom_values[:-length] + 1e-10) - 1

        # 构建新列
        new_columns = pandas.DataFrame({
            f'Acceleration@{length}': acceleration_values
        }, index=df.index)

        df = pandas.concat([df, new_columns], axis=1)

        if 'datetime' in df.columns:
            df = df.rename(columns={'datetime': 'date'})
        result = df[['date', f'Acceleration@{length}']].copy()
        return result