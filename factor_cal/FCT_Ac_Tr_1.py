import pandas as pd
import os

class FCT_Ac_Tr_1:
    def __init__(self):
        self.factor_name = 'FCT_Ac_Tr_1'

    def formula(self, param):
        df = param['df'].copy()
        N = param.get('length', 10)  # 默认为10期移动平均
        k_line = param['k_line']
        instrument = param['instrument']

        # 首先确保 FCT_Tr 存在（已计算）
        tr_path = f'./data/{k_line}/{instrument}/FCT_Tr.csv'
        if not os.path.exists(tr_path):
            raise FileNotFoundError(f'FCT_Tr.csv not found at {tr_path}')
        
        tr_df = pd.read_csv(tr_path)
        tr_df = tr_df.dropna()
        
        # 计算累计指标，这里用简单移动平均作为示例
        tr_df[self.factor_name] = tr_df['FCT_Tr'].rolling(N).mean()
        
        # 只保留日期和因子列
        out_df = tr_df[['date', self.factor_name]]
        
        # 保存
        save_path = f'./data/{k_line}/{instrument}/{self.factor_name}.csv'
        out_df.to_csv(save_path, index=False)