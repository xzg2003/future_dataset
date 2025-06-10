# XSMOM: 横截面动量，计算商品在同类品种中的收益率排名，做多前20%，做空后20%.
# 但是需要计算多种类型的期货，这里无法进行处理

import pandas
import numpy
import os

# 设置工作目录为当前脚本所在的目录
os.chdir(os.path.dirname(os.path.abspath(__file__)))

class XSMOM:
    def __init__(self):
        self.factor_name = 'XSMOM'

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
        获取 instrument 名称，用于提取 TSMOM 中的数据
        """
        length = param.get('length', None)
        if length is None:
            raise ValueError("param missing 'length'")
        print(f"Using length: {length}")

        # 获取 instrument
        instrument = param.get('instrument', None)
        if instrument is None:
            raise ValueError("param missing instrument")

        # 获取 TSMOM@{length}，并优先判断文件是否存在
        TSMOM_data_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), f'../data/1d/{instrument}/TSMOM@{length}.csv')
        if not os.path.exists(TSMOM_data_path):
            raise FileNotFoundError(f"TSMOM file not found: {TSMOM_data_path}")

        TSMOM_df = pandas.read_csv(TSMOM_data_path)
        # TSMOM@{length}.csv 有 datetime 和 TSMOM 两列，且与主 df 按 datetime 对齐
        if 'datetime' in df.columns and 'datetime' in TSMOM_df.columns:
            df = df.merge(TSMOM_df[['datetime', f'TSMOM@{length}']], on='datetime', how='left')
        else:
            # 如果没有 datetime 列，直接用 index 对齐
            df[f'TSMOM@{length}'] = TSMOM_df[f'TSMOM@{length}']

        # 利用滑动窗口计算极端分组均值差
        # 结果初始化
        xs_result = []
        for i in range(len(df) - length + 1):
            """
            读取窗口内的数据
            再进行排序
            """
            window_data = df[f'TSMOM@{length}'].iloc[i : i + length].values
            window_data_sorted = numpy.sort(window_data)

            # 计算滑动窗口的20%对应的位置
            percentile_pos = max(int(len(window_data_sorted) * 0.2), 1)

            # 计算排序前面和后面的均值
            bottom_mean = numpy.mean(window_data_sorted[:percentile_pos])
            top_mean    = numpy.mean(window_data_sorted[-percentile_pos:])

            # 计算两个均值的差值，存储在 xs_result 中
            xs_result.append(top_mean - bottom_mean)

        # 空的数据用 NaN 对齐
        xs_result = [numpy.nan] * (length - 1) + xs_result
        df[f'XSMOM@{length}'] = xs_result

        # 返回结果
        if 'datetime' in df.columns:
            df = df.rename(columns={'datetime': 'date'})
        result = df[['date', f'XSMOM@{length}']].copy()
        return result

