# FCT_Support_Close_Thr_1：收盘价接近支撑位的次数因子，衡量收盘价在窗口内低于一定分位数的次数

import os
import numpy
import pandas

class FCT_Support_Close_Thr_1:
    def __init__(self):
        pass

    def formula(self, param: dict):
        # 从参数字典中提取 DataFrame
        df = param.get('df', None)
        if df is None:
            raise ValueError("no 'df' in param")

        # 从参数字典中读取 length
        length = param.get('length', None)
        if length is None:
            raise ValueError("param missing 'length'")

        # 从参数字典中读取thr，原数据为百分比，这里修正为小数形式
        thr = param.get('thr', None) / 100
        if thr is None:
            raise ValueError("param missing 'thr'")

        # 从参数字典中读取 factor_name
        factor_name = param.get('factor_name', None)
        if factor_name is None:
            raise ValueError("param missing 'factor_name'")

        # 初始化 new_columns 用于统一管理新增列
        new_columns = pandas.DataFrame(index=df.index)

        # 计算支撑位计数（使用 rolling + apply）
        def support_count(x):
            threshold = numpy.quantile(x, thr)
            return numpy.sum(x <= threshold)

        # 使用 rolling.apply 获取结果，并赋值给 new_columns
        new_columns[f'{factor_name}'] = df['close'].rolling(window=length, min_periods=length).apply(
            support_count, raw=True)

        # 合并到主表（一次性合并）
        df = pandas.concat([df, new_columns], axis=1)

        # 返回结果（无日期）
        result = df[[f'{factor_name}']].copy()
        return result
