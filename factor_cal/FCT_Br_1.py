# 人气意愿指标high, ref(close,1), low差值累加对比

import numpy
import pandas


class FCT_Br_1:
    def __init__(self):
        self.factor_name = 'FCT_Br_1'

    def formula(self, param):
        # 从字典中提取DataFrame
        df = param.get('df', None)
        if df is None:
            raise ValueError("no 'df' in param")

        # 确保df是pandas.DataFrame类型
        if not isinstance(df, pandas.DataFrame):
            raise TypeError("df must be DataFrame")

        """
        从字典中读取 length
        获取 instrument 名称，用于提取mindiff中的数据
        """
        length = param.get('length', None)
        if length is None:
            raise ValueError("param missing 'length'")
        print(f"Using length:{length}")

        # 修改为 pd.concat 批量合并方式
        new_columns = pandas.DataFrame(index=df.index)

        # close_pre
        new_columns['close_pre'] = df['close'].shift(1)

        # up 和 down
        new_columns['up'] = numpy.where((df['high'] - new_columns['close_pre']) > 0,
                                        df['high'] - new_columns['close_pre'], 0)
        new_columns['down'] = numpy.where((new_columns['close_pre'] - df['low']) > 0,
                                          new_columns['close_pre'] - df['low'], 0)

        # br1 和 br2
        new_columns['br1'] = new_columns['up'].rolling(window=length).sum()
        new_columns['br2'] = new_columns['down'].rolling(window=length).sum()

        # 避免分母为零
        new_columns['br_sum'] = new_columns['br1'] + new_columns['br2']
        new_columns['br_sum'] = numpy.where(new_columns['br_sum'] == 0, numpy.nan, new_columns['br_sum'])

        # 最终因子计算
        new_columns[f'FCT_Br_1@{length}'] = (new_columns['br1'] - new_columns['br2']) / new_columns['br_sum']

        # 合并进原始 df
        df = pandas.concat([df, new_columns], axis=1)

        # 返回结果（无日期）
        result = df[['date', f'FCT_Br_1@{length}']].copy()
        return result
