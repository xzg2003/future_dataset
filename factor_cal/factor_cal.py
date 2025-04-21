from .FCT_Tr import FCT_Tr
import pandas as pd

def factors_cal():
    instrument_list =['A','AG','AL','AP','AU','BU','C','CF','CJ','CS',
                 'CU','EB','EG','FG','FU','HC','I','IC','IF','IH',
                 'J','JD','JM','L','LU','LH','M','MA','NI','OI','P',
                 'PB','PF','PG','PK','PP','RB','RM','RU','SA','SF',
                 'SM','SN','SP','SR','SC','SS','TA','T','TF','UR','V','Y','ZN']
    factor_list = {}
    f = FCT_Tr()
    factor_list[f.factor_name] = f
    for key, f in factor_list.items():
        for i in instrument_list:
            f.formula({'instrument': i, 'k_line': '5m', 'df': pd.read_csv(f'./data/5m/{i}/{i}.csv')})
