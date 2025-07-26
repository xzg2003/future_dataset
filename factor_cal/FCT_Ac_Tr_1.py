# Ac_Tr_1：技术指标AC除以MA（TR）去量纲

import os

import numpy
import pandas

# 设置工作目录为当前脚本所在的目录
os.chdir(os.path.dirname(os.path.abspath(__file__)))


class FCT_Ac_Tr_1:
    def __init__(self):
        self.factor_name = 'FCT_Ac_Tr_1'

    def formula(self, param):
        # 从参数字典中获取 df
        df = param.get('df', None)
        if df is None:
            raise ValueError("no 'df' in param")

        # 从参数字典中获取 length
        length = param.get('length', None)

        if length is None:
            raise ValueError("param missing 'length'")

        # 从参数字典中获取 instrument
        instrument = param.get('instrument', None)
        if instrument is None:
            raise ValueError("param miss instrument")

        # 从参数字典中获取 k_line_type
        k_line_type = param.get('k_line_type', None)
        if k_line_type is None:
            raise ValueError("param missing k_line_type")

        # 从参数字典中获取 factor_name
        factor_name = param.get('factor_name', None)
        if factor_name is None:
            raise ValueError("param missing factor_name")

        # 从参数字典中获取 mindiff
        mindiff = param.get('mindiff', None)
        if mindiff is None:
            raise ValueError("param missing mindiff")

        # 修改为 pd.concat 批量合并方式
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
        tr_data_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                    f'../data/{k_line_type}/{instrument}/Tr.csv')
        if not os.path.exists(tr_data_path):
            raise FileNotFoundError(f"Tr file not found: {tr_data_path}")

        tr_df = pandas.read_csv(tr_data_path)
        if 'datetime' in df.columns and 'datetime' in tr_df.columns:
            tr_series = pandas.merge(df[['datetime']], tr_df, on='datetime', how='left')['Tr']
        else:
            tr_series = tr_df['Tr']

        new_columns['Tr'] = tr_series.reset_index(drop=True)

        # 最终因子计算
        rolling_mean_tr = new_columns['Tr'].rolling(window=length).mean().fillna(0)
        new_columns[f'{factor_name}'] = numpy.where(
            rolling_mean_tr < mindiff,
            0,
            new_columns['AC'] / rolling_mean_tr
        )

        # 合并进原始 df
        df = pandas.concat([df, new_columns], axis=1)

        # 返回结果（无日期）
        result = df[[f'{factor_name}']].copy()
        return result
