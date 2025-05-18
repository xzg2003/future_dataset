from .FCT_Tr import FCT_Tr
from .FCT_Ac_Tr_1 import FCT_Ac_Tr_1
import pandas as pd


def get_mindiff(mindiff_pd: pd.DataFrame) -> dict:
    """
    Get the minimum difference of each instrument from the mindiff_pd DataFrame.
    :param mindiff_pd: DataFrame containing the minimum difference for each instrument.
    :return: Dictionary with instrument names as keys and their minimum differences as values.
    """
    mindiff_dict = {}
    for index, row in mindiff_pd.iterrows():
        instrument = row['instrument']
        mindiff = row['mindiff']
        mindiff_dict[instrument] = mindiff
        # print(f"Instrument: {instrument}, Mindiff: {mindiff}")
    return mindiff_dict

def factors_cal():
    """
    Calculate factors for all instruments and save them to CSV files.
    """
    # Read the mindiff DataFrame from a CSV file
    mindiff_pd = pd.read_csv('./data/mindiff.csv')
    mindiff_dict = get_mindiff(mindiff_pd)

    instrument_list =['A','AG','AL','AP','AU','BU','C','CF','CJ','CS',
                 'CU','EB','EG','FG','FU','HC','I','IC','IF','IH',
                 'J','JD','JM','L','LU','LH','M','MA','NI','OI','P',
                 'PB','PF','PG','PK','PP','RB','RM','RU','SA','SF',
                 'SM','SN','SP','SR','SC','SS','TA','T','TF','UR','V','Y','ZN']
    factor_list = []

    factor_list.append(FCT_Tr())
    factor_list.append(FCT_Ac_Tr_1())

    for f in factor_list:
        for instr in instrument_list:
            if f.require_length:
                for length in (10, 20, 40, 80, 120, 180):
                    f.formula({'instrument': instr, 'k_line': '5m', 
                               'df': pd.read_csv(f'./data/5m/{instr}/{instr}.csv'), 
                               'mindiff': mindiff_dict[instr], 
                               'length': length})
            else:
                f.formula({'instrument': instr, 'k_line': '5m', 
                           'df': pd.read_csv(f'./data/5m/{instr}/{instr}.csv'), 
                           'mindiff': mindiff_dict[instr]})

if __name__ == '__main__':
    factors_cal()
