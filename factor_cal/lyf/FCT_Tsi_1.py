# FCT_Tsi_1：TSI（趋势强度指标）因子，衡量价格趋势的强弱

import os
import pandas

class FCT_Tsi_1:
    def __init__(self):
        pass

    def formula(self, param: dict):
        # 从参数字典中提取 DataFrame
        df = param.get('df', None)
        if df is None:
            raise ValueError("no 'df' in param")

        # 从参数字典中提取 length
        length = param.get('length', None)

        # 从参数字典中提取 factor_name
        factor_name = param.get('factor_name', None)
        if factor_name is None:
            raise ValueError("param missing 'factor_name'")

        # 初始化 new_columns 用于集中管理中间变量
        new_columns = pandas.DataFrame(index=df.index)

        new_columns['price_change'] = df['close'].diff()  # 计算价格变化
        new_columns['pc_ema1'] = new_columns['price_change'].ewm(span=length).mean()  # 第一次平滑
        new_columns['pc_ema2'] = new_columns['pc_ema1'].ewm(span=length).mean()  # 第二次平滑

        # 对价格变化绝对值进行相同处理
        new_columns['abs_pc'] = new_columns['price_change'].abs()
        new_columns['abs_pc_ema1'] = new_columns['abs_pc'].ewm(span=length).mean()
        new_columns['abs_pc_ema2'] = new_columns['abs_pc_ema1'].ewm(span=length).mean()

        # 计算 TSI
        new_columns[f'{factor_name}'] = (new_columns['pc_ema2'] / new_columns['abs_pc_ema2'])
        # 合并到原始 df
        df = pandas.concat([df, new_columns], axis=1)

        # 返回结果（无日期）
        result = df[[f'{factor_name}']].copy()
        return result
