# Ac_Tr_1：技术指标AC除以MA（TR）去量纲

import pandas as pd
import numpy as np

class FCT_Ac_Tr_1:
    def __init__(self):
        pass
        

    def formula(self, param):
        # 从字典中提取DataFrame
        df = param.get('df', None)
        length = param.get('length', 5)
        mindiff = param.get('mindiff', None)
        factor_name = f'FCT_Ac_Tr_1@{length}'

        if df is None:
            raise ValueError("参数 'param' 中缺少 'df' 键或其值为空")

        # 确保df是pandas.DataFrame类型
        if not isinstance(df, pd.DataFrame):
            raise TypeError("'df' 必须是 pandas.DataFrame 类型")

        # 计算价格均值，这里取价格的最高价与最低价的平均
        df['MP'] = (df['high'] + df['low']) / 2

        # 计算震荡指标
        df['AO'] = df['MP'].rolling(window=length).mean() - df['MP'].rolling(window=(4*length)).mean()

        # 计算 AC
        df['AC'] = df['AO'] - df['AO'].rolling(window=length).mean()
        
        # 取三种差值的绝对值的最大值作为 TR
        df['Tr'] = param.get('tr', None)
        if df['Tr'] is None:
            raise ValueError("参数 'param' 中缺少 'tr' 键或其值为空")

        # 计算输出结果，这里没有最小变动单位，没有办法进行分类处理
        rolling_mean = df['Tr'].rolling(length).mean().fillna(0)  # 填充NaN值为0
        df[factor_name] = np.where(rolling_mean < mindiff, 0,df['AC'] / rolling_mean)
        
        '''
        以下是正确的处理函数
        df['FCT_Ac_Tr_1'] = numpy.where(df['Tr'].rolling(window=length).mean() < df['mindiff'], 0, df['AC'] / df['Tr'].rolling(length).mean())
        '''

        # 返回结果
        if 'datetime' in df.columns:
            df = df.rename(columns={'datetime': 'date'})
        result = df[['date', factor_name]].copy()
        return result