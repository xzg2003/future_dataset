# FCT_Pubu_1：普及率因子，由短期均线和长期均线两条均线组成，衡量短期均线在长期均线窗口内的分位数位置

import os

import numpy
import pandas

class FCT_Pubu_1:
    def __init__(self):
        pass

    def formula(self, param: dict):
        # 从参数字典中提取 DataFrame
        df = param.get('df', None)
        if df is None:
            raise ValueError("no 'df' in param")

        # 从参数字典中提取 length
        length = param.get('length', None)

        # 从参数字典中提取 factor_name
        factor_name = param.get('factor_name', None)
        if factor_name is None:
            raise ValueError("no 'factor_name' in param")

        # 修改为 pd.concat 批量合并方式
        new_columns = pandas.DataFrame(index=df.index)

        # 计算系数
        coefficient = 2 /(length + 1)

        # 计算指数移动平均、二层、四层均值
        new_columns['EMA'] = df['close'] * coefficient + df['close'].shift(1) * (1 - coefficient)
        new_columns['SMA_2n'] = df['close'].rolling(window=2 * length).mean()
        new_columns['SMA_4n'] = df['close'].rolling(window=4 * length).mean()

        # 计算因子
        new_columns[f'{factor_name}'] = (new_columns['EMA'] + new_columns['SMA_2n'] + new_columns['SMA_4n']) / 3

        # 合并进原始 df
        df = pandas.concat([df, new_columns], axis=1)

        # 返回结果（无日期）
        result = df[[f'{factor_name}']].copy()
        return result
