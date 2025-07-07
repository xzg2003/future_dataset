# 乖离率除以TR去量纲

import pandas as pd
import numpy as np

class FCT_Bias_1:
    def __init__(self):
        pass

    def formula(self, param):
        # 从字典中提取DataFrame
        df = param.get('df', None)
        length = param.get('length', 5)
        mindiff = param.get('mindiff', None)
        factor_name = f'FCT_Bias_1@{length}'

        if df is None:
            raise ValueError("参数 'param' 中缺少 'df' 键或其值为空")

        # 确保df是pandas.DataFrame类型
        if not isinstance(df,pd.DataFrame):
            raise TypeError("'df' 必须是 pandas.DataFrame 类型")

        # 计算震荡指标（这里直接照搬了前面Tr的计算代码）
        # 前一k线的收盘价
        df['close_pre'] = df['close'].shift(1)

        # 逐行取三种差值的最大值作为 TR
        df['Tr'] = param.get('tr', None)
        if df['Tr'] is None:
            raise ValueError("参数 'param' 中缺少 'tr' 键或其值为空")

        # 计算因子，缺失mindiff，故这个函数是没有比较的
        rolling_mean = df['Tr'].rolling(length).mean()
        df['signal'] = (df['close'] - df['close'].rolling(window=length).mean()) / rolling_mean
        df[factor_name] = np.where(rolling_mean < mindiff, 0, df['signal'])
        '''
        正确的计算函数
        df['FCT_Bias_1'] = numpy.where(df['Tr'].rolling(window=length).mean() < df['mindiff'], 0, (df['close'] - df['close'].rolling(window=length).mean()) / df['Tr'].rolling(window=length).mean())
        '''

        # 返回结果
        result = df[factor_name].copy()
        return result

