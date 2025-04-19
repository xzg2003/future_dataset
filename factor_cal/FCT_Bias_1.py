# 乖离率除以TR去量纲

import pandas
import numpy

class FCT_Bias_1:
    def __init__(self):
        self.fact_name = 'FCT_Bias_1'

    def formula(self, param, length):
        # 从字典中提取DataFrame
        df = param.get('df', None)
        if df is None:
            raise ValueError("参数 'param' 中缺少 'df' 键或其值为空")

        # 确保df是pandas.DataFrame类型
        if not isinstance(df, pandas.DataFrame):
            raise TypeError("'df' 必须是 pandas.DataFrame 类型")

        # 计算震荡指标（这里直接照搬了前面Tr的计算代码）
        # 前一k线的收盘价
        df['close_pre'] = df['close'].shift(1)

        # 逐行取三种差值的最大值作为 TR
        df['Tr'] = df[['close_pre', 'high', 'low']].apply(
            lambda row: max(row['high'] - row['close_pre'], row['high'] - row['low'], row['close_pre'] - row['low']),
            axis=1
        )

        # 计算因子，缺失mindiff，故这个函数是没有比较的
        df['FCT_Bias_1'] = (df['close'] - df['close'].rolling(window=length).mean()) / df['Tr'].rolling(window=length).mean()

        '''
        正确的计算函数
        df['FCT_Bias_1'] = numpy.where(df['Tr'].rolling(window=length).mean() < df['mindiff'], 0, (df['close'] - df['close'].rolling(window=length).mean()) / df['Tr'].rolling(window=length).mean())
        '''

        # 返回结果
        result = df[['trading_date', 'FCT_Bias_1']].copy()
        return result

