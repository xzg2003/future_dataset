# Ac_Tr_1：人气意愿指标，high、open、low差值累加对比

import pandas

class FCT_Ar_1:
    def __init__(self):
        self.factor_name = 'FCT_Ar_1'

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

        # 修改为 pd.concat 批量合并方式
        new_columns = pandas.DataFrame(index=df.index)

        new_columns['up'] = df['high'] - df['open']
        new_columns['down'] = df['open'] - df['low']

        new_columns['ar1'] = new_columns['up'].rolling(window=length).sum()
        new_columns['ar2'] = new_columns['down'].rolling(window=length).sum()

        new_columns[f'FCT_Ar_1@{length}'] = (new_columns['ar1'] - new_columns['ar2']) / (
                new_columns['ar1'] + new_columns['ar2'])

        # 合并进原始 df
        df = pandas.concat([df, new_columns], axis=1)

        # 返回结果
        if 'datetime' in df.columns:
            df = df.rename(columns={'datetime': 'date'})
        result = df[['date', f'FCT_Ar_1@{length}']].copy()
        return result