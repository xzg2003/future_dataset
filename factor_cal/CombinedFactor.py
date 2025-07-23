import pandas as pd
import numpy as np


class CombinedFactor:
    def __init__(self, factors, weights):
        """
        初始化组合因子
        :param factors: 因子对象列表
        :param weights: 对应权重列表 (需与factors长度一致)
        """
        if len(factors) != len(weights):
            raise ValueError("因子数量和权重数量必须相同")
        self.factors = factors
        self.weights = weights
        self.factor_name = "CombinedFactor"

    def formula(self, param):
        """
        计算组合因子
        :param param: 参数字典 (需包含所有因子所需的参数)
        :return: 包含日期和组合因子的DataFrame
        """
        results = []

        # 计算每个因子并收集结果
        for factor in self.factors:
            factor_result = factor.formula(param)
            # 提取因子名和结果
            factor_col = [col for col in factor_result.columns if col != 'date'][0]
            results.append(factor_result[['date', factor_col]])

        # 合并所有因子结果
        combined_df = results[0]
        for i in range(1, len(results)):
            combined_df = pd.merge(combined_df, results[i], on='date', how='outer')

        # 提取因子值列
        factor_cols = [col for col in combined_df.columns if col != 'date']

        # 线性组合
        combined_values = np.zeros(len(combined_df))
        for col, weight in zip(factor_cols, self.weights):
            combined_values += combined_df[col] * weight

        # 创建结果DataFrame
        result_df = pd.DataFrame({
            'date': combined_df['date'],
            self.factor_name: combined_values
        })

        return result_df

