import os       # 与路径操作相关的包，用于管理文件
import pandas as pd
import sys
from FCT_Ac_Tr_1   import      FCT_Ac_Tr_1
from FCT_Ar_1      import      FCT_Ar_1
from FCT_Bias_1    import      FCT_Bias_1
from FCT_Br_1      import      FCT_Br_1
from FCT_Cmf_1     import      FCT_Cmf_1
from Tr            import      Tr
from CombinedFactor import *

class NewFactor:
    def __init__(self):
        pass

    def formula(self, param):
        # 从字典中提取DataFrame
        df = param.get('df', None)
        length = param.get('length', 5)
        mindiff = param.get('mindiff', None)
        factor_name = f'NewFactor@{length}'

        if df is None:
            raise ValueError("参数 'param' 中缺少 'df' 键或其值为空")

        # 确保df是pandas.DataFrame类型
        if not isinstance(df,pd.DataFrame):
            raise TypeError("'df' 必须是 pandas.DataFrame 类型")

        # 1. 创建单个因子实例
        factor1 = FCT_Ac_Tr_1()
        factor2 = FCT_Ar_1()  # 假设有其他因子类
        factor3 = FCT_Bias_1()
        factor4 = FCT_Br_1()
        factor5 = FCT_Cmf_1()

        # 2. 创建组合因子实例 (假设权重为0.5, 0.3, 0.2)
        combined_factor = CombinedFactor(
            factors=[factor1, factor2, factor3, factor4, factor5],
            weights=[0.2,0.2,0.2,0.2,0.2]
        )

        #3.准备组合因子专用参数
        params = {
            'df': df.copy(),
            'length': param.get('length', 5),
            'mindiff': param.get('mindiff', None),
            'tr': df.get('tr', None),

        }

        df['Tr'] = param.get('tr', None)
        if df['Tr'] is None:
            raise ValueError("参数 'param' 中缺少 'tr' 键或其值为空")

        # 4. 计算组合因子
        result_df = combined_factor.formula(params)

        # 5. 重命名因子列为 Newfactor@{length}
        result_df = result_df.rename(columns={'CombinedFactor': factor_name})

        return result_df


