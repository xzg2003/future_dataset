# FCT_Vol_Close_Corr_1：成交量与收盘价相关系数因子，衡量指定窗口内成交量与收盘价的相关性

import pandas
import numpy
import os

# 设置工作目录为当前脚本所在的目录
os.chdir(os.path.dirname(os.path.abspath(__file__)))

class FCT_Vol_Close_Corr_1:
    def __init__(self):
        self.factor_name = 'FCT_Vol_Close_Corr_1'

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

        # 计算滑动窗口相关系数
        def corr_func(x):
            x = numpy.asarray(x)
            if x.ndim == 1:
                x = x.reshape(-1, 2)
            return numpy.corrcoef(x[:, 0], x[:, 1])[0, 1] if numpy.std(x[:, 0]) > 0 and numpy.std(x[:, 1]) > 0 else numpy.nan

        # 只保留两列，rolling后apply返回Series
        corr_series = (
            df[['volume', 'close']]
            .rolling(window=length, min_periods=length)
            .apply(corr_func, raw=True)
        )

        # apply后返回的是DataFrame，取一列即可
        df[f'FCT_Vol_Close_Corr_1@{length}'] = corr_series.iloc[:, 0]

        # 返回结果
        if 'datetime' in df.columns:
            df = df.rename(columns={'datetime': 'date'})
        result = df[['date', f'FCT_Vol_Close_Corr_1@{length}']].copy()
        return result