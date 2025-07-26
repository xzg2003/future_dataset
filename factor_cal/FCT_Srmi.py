# FCT_Srmi：SRMI（相对动量指数）因子，衡量收盘价在指定窗口内的相对强弱位置

import os

import pandas

# 设置工作目录为当前脚本所在的目录
os.chdir(os.path.dirname(os.path.abspath(__file__)))


class FCT_Srmi:
    def __init__(self):
        self.factor_name = 'FCT_Srmi'

    def formula(self, param):
        # 从参数字典中提取 DataFrame
        df = param.get('df', None)
        if df is None:
            raise ValueError("no 'df' in param")

        # 从参数字典中读取 length
        length = param.get('length', None)
        if length is None:
            raise ValueError("param missing 'length'")

        # 从参数字典中获取 factor_name
        factor_name = param.get('factor_name', None)
        if factor_name is None:
            raise ValueError("param missing 'factor_name'")

        new_columns = pandas.DataFrame(index=df.index)

        # 计算滚动最小值和最大值
        rolling_min = df['close'].rolling(window=length).min()
        rolling_max = df['close'].rolling(window=length).max()

        # 计算 SRMI：(close - min) / (max - min)
        new_columns[f'{factor_name}'] = (df['close'] - rolling_min) / (rolling_max - rolling_min + 1e-10)

        # 合并进原始 df
        df = pandas.concat([df, new_columns], axis=1)

        # 返回结果（无日期）
        result = df[[f'{factor_name}']].copy()
        return result
