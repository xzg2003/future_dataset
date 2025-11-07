# FCT_Vmacd：成交量 MACD 因子，衡量成交量的趋势变化和动能拐点

import os

import pandas

# 设置工作目录为当前脚本所在的目录
os.chdir(os.path.dirname(os.path.abspath(__file__)))


class FCT_Vmacd:
    def __init__(self):
        self.factor_name = 'FCT_Vmacd'

    def formula(self, param):
        # 从字典中提取 DataFrame
        df = param.get('df', None)
        if df is None:
            raise ValueError("no 'df' in param")
        if not isinstance(df, pandas.DataFrame):
            raise TypeError("df must be DataFrame")

        # MACD 参数
        fast = param.get('fast', 12)
        slow = param.get('slow', 26)
        signal = param.get('signal', 9)
        print(f"Using fast: {fast}, slow: {slow}, signal: {signal}")

        # 初始化 new_columns 用于统一管理中间变量
        new_columns = pandas.DataFrame(index=df.index)

        # 计算成交量的 EMA
        ema_fast = df['volume'].ewm(span=fast, adjust=False).mean()
        ema_slow = df['volume'].ewm(span=slow, adjust=False).mean()

        # DIF 线
        new_columns['vmacd_dif'] = ema_fast - ema_slow
        # DEA 线
        new_columns['vmacd_dea'] = new_columns['vmacd_dif'].ewm(span=signal, adjust=False).mean()
        # MACD 柱
        new_columns['vmacd_macd'] = new_columns['vmacd_dif'] - new_columns['vmacd_dea']

        # 合并到主表
        df = pandas.concat([df, new_columns], axis=1)

        result = df[['vmacd_dif', 'vmacd_dea', 'vmacd_macd']].copy()
        # TODO：一个因子计算器只可能返回一个结果，这里需要对这个结果进行调整
        return result
