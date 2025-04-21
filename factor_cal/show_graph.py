import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

def show_graph():
    instrument = 'AG'
    k_line = '5m'
    factor_name = 'FCT_Tr'
    factor_path = f'./data/{k_line}/{instrument}/{factor_name}.csv'

    df = pd.read_csv(factor_path)
    data = df[factor_name]

    plt.figure(figsize=(10, 6))
    sns.histplot(df[factor_name], bins=np.arange(0, 100, 1), kde=True)

    plt.title(f'{instrument} - {factor_name}({k_line})')
    plt.xlabel(factor_name)
    plt.ylabel('Frequency')
    plt.xlim(0, 100)

    plt.tight_layout()
    plt.show()