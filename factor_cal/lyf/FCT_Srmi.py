# FCT_Srmi：SRMI（相对动量指数）因子，衡量收盘价在指定窗口内的相对强弱位置

import os
import pandas

class FCT_Srmi:
    def __init__(self):
        pass

    def formula(self, param: dict):
        # 从参数字典中提取 DataFrame
        df = param.get('df', None)
        if df is None:
            raise ValueError("no 'df' in param")

        # 从参数字典中读取 length_momentum
        length_momentum = param.get('length_momentum', None)
        if length_momentum is None:
            raise ValueError("param missing 'length_momentum'")

        # 从参数字典中读取 length_mean
        length_mean = param.get('length_mean', None)

        # 从参数字典中获取 factor_name
        factor_name = param.get('factor_name', None)
        if factor_name is None:
            raise ValueError("param missing 'factor_name'")

        new_columns = pandas.DataFrame(index=df.index)

        # 计算原始动量
        new_columns['momentum'] = df['close'] - df['close'].shift(length_momentum)

        # 计算平滑动量
        new_columns['smooth_momentum'] = new_columns['momentum'].rolling(window=length_mean).mean()

        # 计算窗口期内的标准差
        new_columns['std'] = df['close'].rolling(window=length_mean).std()

        # 标准化，得到结果
        new_columns[f'{factor_name}'] = new_columns['smooth_momentum'] / new_columns['std']

        # 合并进原始 df
        df = pandas.concat([df, new_columns], axis=1)

        # 返回结果（无日期）
        result = df[[f'{factor_name}']].copy()
        return result
