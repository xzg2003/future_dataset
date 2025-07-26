# Ac_Tr_1：技术指标AC除以MA（TR）去量纲

import pandas
import numpy
import os

# 设置工作目录为当前脚本所在的目录
os.chdir(os.path.dirname(os.path.abspath(__file__)))

class FCT_Ac_Tr_1:
    def __init__(self):
        self.factor_name = 'FCT_Ac_Tr_1'

    def formula(self, param):
        # 从字典中提取 DataFrame
        df = param.get('df', None)
        if df is None:
            raise ValueError("no 'df' in param")

        # 确保 df 是 pandas.DataFrame 类型
        if not isinstance(df, pandas.DataFrame):
            raise TypeError("df must be DataFrame")

        """
        从字典中读取 length
        获取 instrument 名称，用于提取mindiff中的数据
        """
        length = param.get('length', None)
        if length is None:
            raise ValueError("param missing 'length'")
        print(f"Using length: {length}")

        # 获取instrument
        instrument = param.get('instrument', None)
        if instrument is None:
            raise ValueError("param miss instrument")

        # 获取mindiff
        mindiff = param.get('mindiff', None)
        if mindiff is None:
            raise ValueError(f"param miss mindiff for instrument: {param.get('instrument', 'unknown')}")
        print(f"Using mindiff: {mindiff}")

        # 获取k_line_type
        k_line_type = param.get('k_line_type', None)
        if k_line_type is None:
            raise ValueError("param missing instrument")

        # 获取因子名称
        factor_name = param.get('factor_name', None)
        if factor_name is None:
            raise ValueError("param missing factor_name for FCT_Ac_Tr_1")
        
        # 构建新的列 DataFrame
        new_columns = pandas.DataFrame(index=df.index)

        # 中间变量计算
        new_columns['MP'] = (df['high'] + df['low']) / 2
        new_columns['AO'] = new_columns['MP'].rolling(window=length).mean() - \
                            new_columns['MP'].rolling(window=4 * length).mean()
        new_columns['AC'] = new_columns['AO'] - new_columns['AO'].rolling(window=length).mean()

        # 前一k线收盘价
        new_columns['close_pre'] = df['close'].shift(1)

        # Tr 数据来自外部文件
        tr = param.get('Tr', None)
        if tr is None:
            raise ValueError("param missing 'Tr' for FCT_Ac_Tr_1")

        new_columns['Tr'] = tr

        # 最终因子计算
        rolling_mean_tr = new_columns['Tr'].rolling(window=length).mean().fillna(0)
        new_columns[factor_name] = numpy.where(
            rolling_mean_tr < mindiff,
            0,
            new_columns['AC'] / rolling_mean_tr
        )


        result = new_columns[factor_name].copy()
        return result