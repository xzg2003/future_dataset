# FCT_Support_Close_Thr_1：收盘价接近支撑位的次数因子，衡量收盘价在窗口内低于一定分位数的次数

import pandas
import numpy
import os

from torch.ao.nn.quantized.functional import threshold

# 设置工作目录为当前脚本所在的目录
os.chdir(os.path.dirname(os.path.abspath(__file__)))

class FCT_Support_Close_Thr_1:
    def __init__(self):
        self.factor_name = 'FCT_Support_Close_Thr_1'

    def formula(self, param):
        # 从字典中提取 DataFrame
        df = param.get('df', None)
        if df is None:
            raise ValueError("no 'df' in param")
        if not isinstance(df, pandas.DataFrame):
            raise TypeError("df must be DataFrame")

        # 从字典中读取 length 和 thr（分位数阈值，默认0.3）
        length = param.get('length', None)
        thr    = param.get('thr', 0.3)
        if length is None:
            raise ValueError("param missing 'length'")
        print(f"Using length: {length}, thr: {thr}")

        # 计算每个窗口内的分位数阈值
        def support_count(x):
            threshold = numpy.quantile(x, thr)
            return numpy.sum(x <= threshold)

        df[f'FCT_Support_Close_Thr_1@{length}_{thr}'] = df['close'].rolling(window=length, min_periods=length).apply(support_count, raw=True)

        # 返回结果
        if 'datetime' in df.columns:
            df = df.rename(columns={'datetime': 'date'})
        result = df[['date', f'FCT_Support_Close_Thr_1@{length}_{thr}']].copy()
        return result