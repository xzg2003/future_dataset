# FCT_Pubu_Atr_Dfive：衡量短期均线在长期均线窗口内的分位数位置，并用 ATR 归一化，适合捕捉价格分布于波动率的关系

import os

import numpy
import pandas

# 设置工作目录为当前脚本所在的目录
os.chdir(os.path.dirname(os.path.abspath(__file__)))


class FCT_Pubu_Atr_Dfive:
    def __init__(self):
        self.factor_name = 'FCT_Pubu_Atr_Dfive'

    def formula(self, param):
        # 从参数字典中提取 DataFrame
        df = param.get('df', None)
        if df is None:
            raise ValueError("no 'df' in param")

        # 从参数字典中提取 short, long
        short = param.get('short', None)
        long = param.get('long', None)
        if short or long is None:
            raise ValueError("param miss short or long")

        # 从参数字典中提取 atr_length
        atr_length = param.get('atr_length', None)
        if atr_length is None:
            raise ValueError("param miss atr_length")

        # 从参数字典中获取 instrument
        instrument = param.get('instrument', None)
        if instrument is None:
            raise ValueError("param miss instrument")

        # 从参数字典中获取 k_line_type
        k_line_type = param.get('k_line_type', None)
        if k_line_type is None:
            raise ValueError("param missing instrument")

        # 从参数字典中获取 factor_name
        factor_name = param.get('factor_name', None)
        if factor_name is None:
            raise ValueError("param miss factor_name")

        # 修改为 pd.concat 批量合并方式
        new_columns = pandas.DataFrame(index=df.index)

        # Tr 数据来自外部文件
        tr_data_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                    f'../data/{k_line_type}/{instrument}/Tr.csv')
        if not os.path.exists(tr_data_path):
            raise FileNotFoundError(f"Tr file not found: {tr_data_path}")

        tr_df = pandas.read_csv(tr_data_path)
        if 'datetime' in df.columns and 'datetime' in tr_df.columns:
            tr_series = df[['datetime']].merge(tr_df[['datetime', 'Tr']], on='datetime', how='left')['Tr']
        else:
            tr_series = tr_df['Tr'].reindex(df.index, fill_value=numpy.nan)

        new_columns['Tr'] = tr_series

        # 计算 ATR
        new_columns['ATR'] = new_columns['Tr'].rolling(window=atr_length).mean()

        # 加载 FCT_Pubu_1 数据
        pubu_data_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                      f'../data/{k_line_type}/{instrument}/FCT_Pubu_1.csv')
        if not os.path.exists(pubu_data_path):
            raise FileNotFoundError(f"FCT_Pubu_1 file not found: {pubu_data_path}")

        pubu_df = pandas.read_csv(pubu_data_path)
        if 'datetime' in df.columns and 'datetime' in pubu_df.columns:
            pubu_series = df[['datetime']].merge(pubu_df[['datetime', 'FCT_Pubu_1']], on='datetime', how='left')[
                'FCT_Pubu_1']
        else:
            pubu_series = pubu_df['FCT_Pubu_1'].reindex(df.index, fill_value=numpy.nan)

        new_columns['FCT_Pubu_1'] = pubu_series

        # 用 ATR 归一化
        new_columns[f'{factor_name}'] = new_columns['FCT_Pubu_1'] / (new_columns['ATR'] + 1e-10)

        # 合并进原始 df
        df = pandas.concat([df, new_columns], axis=1)

        # 返回结果
        result = df[[f'{factor_name}']].copy()
        return result
