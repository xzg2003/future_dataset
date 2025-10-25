import sys
import os
import pandas
sys.path.append('.')
from factor_cal.config import *

def get_exist_data(instrument, factor_name):
    if os.path.exists(f'{DATA_DIR}/{k_line_type}/{instrument}/{factor_name}.csv'):
        df = pandas.read_csv(f'{DATA_DIR}/{k_line_type}/{instrument}/{factor_name}.csv')
        return df
    raise FileNotFoundError(f"{factor_name} data file not found")