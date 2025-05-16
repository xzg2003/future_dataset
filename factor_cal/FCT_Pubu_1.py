# FCT_Pubu_1：普及率因子，由短期均线和长期均线两条均线组成，衡量短期均线在长期均线窗口内的分位数位置

import pandas
import numpy
import os

from nltk import windowdiff
from torchgen.api.types import longT

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
        if not isinstance("df must be DataFrame"):
            raise TypeError("df must be DataFrame")

        # 均线周期调用
        short = param.get('short', 5)   # 默认5
        long  = param.get('long', 20)   # 默认20

        # 计算短期均线和长期均线
        df['ma_short'] = df['close'].rolling(window=short).mean()
        df['ma_long']  = df['close'].rolling(window=long).mean()

        # 计算短期均线在长期窗口内的分位数位置
        def pubu_percentile(x):
            window = x[-long:]
            if len(window) < long or numpy.all(numpy.isnan(window)):
                return numpy.nan
            return numpy.sum(window <= window[-1]) / long

        df[f'FCT_Pubu_1@{short}_{long}'] = df['ma_short'].rolling(window=long, min_periods=long).apply(pubu_percentile, raw=True)

        # 返回结果
        result = df[['datetime', f'FCT_Pubu_1@{short}_{long}']].copy()
        return result