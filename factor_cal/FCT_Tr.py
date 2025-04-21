import pandas as pd
import os

class FCT_Tr():
    def __init__(self):
        self.factor_name = 'FCT_Tr'

    def formula(self, param):
        df = param['df'].copy()
        instrument = param['instrument']
        k_line = param['k_line']

        df['datetime'] = pd.to_datetime(df['datetime'])
        df['close_pre'] = df['close'].shift(1)

        tr1 = (df['high'] - df['close_pre']).abs()
        tr2 = (df['high'] - df['low']).abs()
        tr3 = (df['close_pre'] - df['low']).abs()

        df[self.factor_name] = pd.concat([tr1, tr2, tr3], axis=1).max(axis=1)

        result = df[['datetime', self.factor_name]].copy()
        result.rename(columns={'datetime': 'date'}, inplace=True)

        output_path = f'./data/{k_line}/{instrument}/{self.factor_name}.csv'
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        result.to_csv(output_path, index=False)