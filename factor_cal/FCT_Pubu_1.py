# FCT_Pubu_1：普及率因子，由短期均线和长期均线两条均线组成，衡量短期均线在长期均线窗口内的分位数位置

import os

import numpy
import pandas

# 设置工作目录为当前脚本所在的目录
os.chdir(os.path.dirname(os.path.abspath(__file__)))


class FCT_Pubu_1:
    def __init__(self):
        self.factor_name = 'FCT_Pubu_1'

    def formula(self, param):
        # 从字典中提取 DataFrame
        df = param.get('df', None)
        if df is None:
            raise ValueError("no 'df' in param")
        if not isinstance(df, pandas.DataFrame):
            raise TypeError("df must be DataFrame")

        # 均线周期调用
        short = param.get('short', 5)  # 默认5
        long = param.get('long', 20)  # 默认20

        # 修改为 pd.concat 批量合并方式
        new_columns = pandas.DataFrame(index=df.index)

        # 计算短期均线和长期均线
        new_columns['ma_short'] = df['close'].rolling(window=short).mean()
        new_columns['ma_long'] = df['close'].rolling(window=long).mean()

        # 计算短期均线在长期窗口内的分位数位置
        def pubu_percentile(x):
            window = x[-long:]
            if len(window) < long or numpy.all(numpy.isnan(window)):
                return numpy.nan
            return numpy.sum(window <= window[-1]) / long

        new_columns[f'FCT_Pubu_1'] = new_columns['ma_short'].rolling(window=long, min_periods=long).apply(
            pubu_percentile, raw=True)

        # 合并进原始 df
        df = pandas.concat([df, new_columns], axis=1)

        # 返回结果（无日期）
        result = df[[f'FCT_Pubu_1']].copy()
        return result
