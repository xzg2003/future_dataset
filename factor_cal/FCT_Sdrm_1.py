# FCT_Sdrm_1：标准差动量因子，衡量收盘价在指定窗口内的波动性

import os

import pandas

# 设置工作目录为当前脚本所在的目录
os.chdir(os.path.dirname(os.path.abspath(__file__)))


class FCT_Sdrm_1:
    def __init__(self):
        self.factor_name = 'FCT_Sdrm_1'

    def formula(self, param):
        # 从字典中提取 DataFrame
        df = param.get('df', None)
        if df is None:
            raise ValueError("no 'df' in param")
        if not isinstance(df, pandas.DataFrame):
            raise TypeError("df must be DataFrame")

        # 从字典中读取 length
        length = param.get('length', None)
        if length is None:
            raise ValueError("param missing 'length'")
        print(f"Using length: {length}")

        # 修改为 pd.concat 批量合并方式
        new_columns = pandas.DataFrame({
            f'FCT_Sdrm_1@{length}': df['close'].rolling(window=length).std()
        }, index=df.index)

        df = pandas.concat([df, new_columns], axis=1)

        # 返回结果（无日期）
        result = df[[f'FCT_Sdrm_1@{length}']].copy()
        return result
