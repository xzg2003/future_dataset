# FCT_TSI_Ref_1：TSI（真实强度指标）参考因子，衡量价格趋势的强弱和方向

import pandas
import numpy
import os

# 设置工作目录为当前脚本所在的目录
os.chdir(os.path.dirname(os.path.abspath(__file__)))

class FCT_TSI_Ref_1:
    def __init__(self):
        self.factor_name = 'FCT_TSI_Ref_1'

    def formula(self, param):
        # 从字典中提取 DataFrame
        df = param.get('df', None)
        if df is None:
            raise ValueError("no 'df' in param")
        if not isinstance(df, pandas.DataFrame):
            raise TypeError("df must be DataFrame")

        # 从字典中读取短期和长期参数
        short = param.get('short', 25)
        long = param.get('long', 13)
        if short is None or long is None:
            raise ValueError("param missing 'short' or 'long'")
        print(f"Using short: {short}, long: {long}")

        """
        # 计算价格变化
        df['diff'] = df['close'].diff()

        # 计算两次 EMA
        ema_1 = df['diff'].ewm(span=short, adjust=False).mean()
        ema_2 = ema_1.ewm(span=long, adjust=False).mean()

        # 计算绝对值部分的两次 EMA
        abs_diff = numpy.abs(df['diff'])
        abs_ema_1 = abs_diff.ewm(span=short, adjust=False).mean()
        abs_ema_2 = abs_ema_1.ewm(span=long, adjust=False).mean()

        # 计算 TSI
        df[f'FCT_TSI_Ref_1'] = 100 * (ema_2 / (abs_ema_2 + 1e-10))
        """

        # 初始化 new_columns 用于统一管理中间变量
        new_columns = pandas.DataFrame(index=df.index)

        # 计算价格变化
        new_columns['diff'] = df['close'].diff()

        # 计算两次 EMA
        ema_1 = new_columns['diff'].ewm(span=short, adjust=False).mean()
        ema_2 = ema_1.ewm(span=long, adjust=False).mean()

        # 计算绝对值部分的两次 EMA
        abs_diff = numpy.abs(new_columns['diff'])
        abs_ema_1 = abs_diff.ewm(span=short, adjust=False).mean()
        abs_ema_2 = abs_ema_1.ewm(span=long, adjust=False).mean()

        # 计算 TSI
        new_columns[f'FCT_TSI_Ref_1'] = 100 * (ema_2 / (abs_ema_2 + 1e-10))

        # 合并到主表
        df = pandas.concat([df, new_columns], axis=1)

        # 返回结果
        if 'datetime' in df.columns:
            df = df.rename(columns={'datetime': 'date'})
        result = df[['date', f'FCT_TSI_Ref_1']].copy()
        return result