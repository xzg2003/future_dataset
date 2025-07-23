# 乖离率除以TR去量纲

import os

import numpy
import pandas


class FCT_Bias_1:
    def __init__(self):
        self.fact_name = 'FCT_Bias_1'

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

        # 修改为 pd.concat 批量合并方式
        new_columns = pandas.DataFrame(index=df.index)

        # close_pre
        new_columns['close_pre'] = df['close'].shift(1)

        # Tr 数据来自外部文件
        tr_data_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                    f'../data/{k_line_type}/{instrument}/Tr.csv')
        if not os.path.exists(tr_data_path):
            raise FileNotFoundError(f"Tr file not found: {tr_data_path}")

        tr_df = pandas.read_csv(tr_data_path)
        if 'datetime' in df.columns and 'datetime' in tr_df.columns:
            tr_series = df[['datetime']].merge(tr_df[['datetime', 'Tr']], on='datetime', how='left')['Tr']
        else:
            tr_series = tr_df['Tr'].reindex(new_columns.index, fill_value=numpy.nan)

        new_columns['Tr'] = tr_series

        # 计算因子所需中间变量
        rolling_mean_tr = new_columns['Tr'].rolling(window=length).mean().fillna(0)
        rolling_mean_close = df['close'].rolling(window=length).mean().fillna(0)

        # 最终因子计算
        new_columns[f'FCT_Bias_1@{length}'] = numpy.where(
            rolling_mean_tr < mindiff,
            0,
            (df['close'] - rolling_mean_close) / rolling_mean_tr
        )

        # 合并进原始 df
        df = pandas.concat([df, new_columns], axis=1)

        # 返回结果（无日期）
        result = df[['date', f'FCT_Bias_1@{length}']].copy()
        return result
