# FCT_TSI_Ref_1：TSI（真实强度指标）参考因子，衡量价格趋势的强弱和方向
# TODO: 因子计算方法不明确，似乎与TSI因子重叠

import os

import numpy
import pandas


class FCT_TSI_Ref_1:
    def __init__(self):
        pass

    def formula(self, param):
        # 从参数字典中提取 DataFrame
        df = param.get('df', None)
        if df is None:
            raise ValueError("no 'df' in param")

        # 从参数字典中读取 short, long
        short = param.get('short', None)
        long = param.get('long', None)
        if short or long is None:
            raise ValueError("no 'short' or 'long' in param")

        # 从参数字典中读取 factor_name
        factor_name = param.get('factor_name', None)
        if factor_name is None:
            raise ValueError("no 'factor_name' in param")

        # 初始化 new_columns 用于统一管理中间变量
        new_columns = pandas.DataFrame(index=df.index)

        # 计算价格变化
        new_columns['diff'] = df['close'].diff()

        # 计算两次 EMA
        ema_1 = new_columns['diff'].ewm(span=short, adjust=False).mean()
        ema_2 = ema_1.ewm(span=long, adjust=False).mean()

        # 计算绝对值部分的两次 EMA
        abs_diff = numpy.abs(new_columns['diff'])
        abs_ema_1 = abs_diff.ewm(span=short, adjust=False).mean()
        abs_ema_2 = abs_ema_1.ewm(span=long, adjust=False).mean()

        # 计算 TSI
        new_columns[f'{factor_name}'] = 100 * (ema_2 / (abs_ema_2 + 1e-10))

        # 合并到主表
        df = pandas.concat([df, new_columns], axis=1)

        # 返回结果
        result = df[[f'{factor_name}']].copy()
        return result
