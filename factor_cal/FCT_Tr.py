import pandas as pd

class FCT_Tr():
    def __init__(self):
        self.factor_name = 'FCT_Tr'
        self.require_length = False

    def formula(self, param):
        df = param['df'].copy()
        instrument = param['instrument']
        k_line = param['k_line']

        df['datetime'] = pd.to_datetime(df['datetime'])
        df['close_pre'] = df['close'].shift(1)

        tr1 = (df['high'] - df['close_pre']).abs()
        tr2 = (df['high'] - df['low']).abs()
        tr3 = (df['close_pre'] - df['low']).abs()

        out = pd.concat([tr1, tr2, tr3], axis=1).max(axis=1)

        result = pd.DataFrame({
            'datetime': df['datetime'],
            self.factor_name: out
        })

        save_path = f'./data/{k_line}/{instrument}/{self.factor_name}.csv'
        result.to_csv(save_path, index=False)