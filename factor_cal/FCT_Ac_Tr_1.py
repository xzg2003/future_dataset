# Ac_Tr_1：技术指标AC除以MA（TR）去量纲

import pandas
import numpy

class FCT_Ac_Tr_1:
    def __init__(self):
        self.factor_name = 'FCT_Ac_Tr_1'

    def formula(self, param, length):
        # 从字典中提取DataFrame
        df = param.get('df', None)
        if df is None:
            raise ValueError("参数 'param' 中缺少 'df' 键或其值为空")

        # 确保df是pandas.DataFrame类型
        if not isinstance(df, pandas.DataFrame):
            raise TypeError("'df' 必须是 pandas.DataFrame 类型")

        # 计算价格均值，这里取价格的最高价与最低价的平均
        df['MP'] = (df['high'] + df['low']) / 2

        # 计算震荡指标
        df['AO'] = df['MP'].rolling(window=length).mean() - df['MP'].rolling(window=(4*length)).mean()

        # 计算 AC
        df['AC'] = df['AO'] - df['AO'].rolling(window=length).mean()

        # 计算震荡指标（这里直接照搬了前面Tr的计算代码）
        # 前一k线的收盘价
        df['close_pre'] = df['close'].shift(1)

        # 取三种差值的绝对值的最大值作为 TR
        df['Tr'] = df[['close_pre', 'high', 'low']].apply(
            lambda row: max(row['high'] - row['close_pre'], row['high'] - row['low'], row['close_pre'] - row['low']),
            axis=1
        )

        # 计算输出结果，这里没有最小变动单位，没有办法进行分类处理
        df['OUT'] = df['AC'] / df['Tr'].rolling(window=length).mean()

        '''
        以下是正确的处理函数
        df['OUT'] = numpy.where(df['Tr'].rolling(window=length).mean() < df['mindiff'], 0, df['AC'] / df['Tr'].rolling(length).mean())
        '''

        # 返回结果
        result = df[['trading_date', 'FCT_Ac_Tr_1']].copy()
        return result