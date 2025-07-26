# FCT_Tsi_1：TSI（趋势强度指标）因子，衡量价格趋势的强弱

import os

import numpy
import pandas

# 设置工作目录为当前脚本所在的目录
os.chdir(os.path.dirname(os.path.abspath(__file__)))


class FCT_Tsi_1:
    def __init__(self):
        self.factor_name = 'FCT_Tsi_1'

    def formula(self, param):
        # 从参数字典中提取 DataFrame
        df = param.get('df', None)
        if df is None:
            raise ValueError("no 'df' in param")

        # 从参数字典中提取 short, long
        short = param.get('short', None)
        long = param.get('long', None)
        if short or long is None:
            raise ValueError("param missing 'short' or 'long'")

        # 从参数字典中提取 factor_name
        factor_name = param.get('factor_name', None)
        if factor_name is None:
            raise ValueError("param missing 'factor_name'")

        # 初始化 new_columns 用于集中管理中间变量
        new_columns = pandas.DataFrame(index=df.index)

        # 计算价格变化
        new_columns['diff'] = df['close'].diff()

        # 计算两次 EMA
        ema_1 = new_columns['diff'].ewm(span=short, adjust=False).mean()
        ema_2 = ema_1.ewm(span=short, adjust=False).mean()

        # 计算绝对值部分的两次 EMA
        abs_diff = numpy.abs(new_columns['diff'])
        abs_ema_1 = abs_diff.ewm(span=short, adjust=False).mean()
        abs_ema_2 = abs_ema_1.ewm(span=long, adjust=False).mean()

        # 计算 TSI
        new_columns[f'{factor_name}'] = 100 * (ema_2 / (abs_ema_2 + 1e-10))

        # 合并到原始 df
        df = pandas.concat([df, new_columns], axis=1)

        # 返回结果（无日期）
        result = df[[f'{factor_name}']].copy()
        return result
