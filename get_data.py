import rqdatac
import pandas as pd
import os

instruments= ['A','AG','AL','AP','AU','BU','C','CF','CJ','CS',
             'CU','EB','EG','FG','FU','HC','I','IC','IF','IH',
            'J','JD','JM','L','LU','LH','M','MA','NI','OI','P',
            'PB','PF','PG','PK','PP','RB','RM','RU','SA','SF',
            'SM','SN','SP','SR','SC','SS','TA','T','TF','UR','V','Y','ZN'] #期货类型

# 数据目录
DATA_DIR = 'C:/wzx/KCL/dataset/future_data'

# k线类型
k_line_type = '1d'

# 替换为自己的 api
rqdatac.init('tcp://license:VTqc-ZwvOlHCT5nNmXQjR7gSJwEtmN0Me22-InEjOUFYedUrx6-_4rhn38qDND9KqdKHsnYmdF11b9-RrKBh69KBv5DeunHQDHAAjqqWdHjmbOn7GrlF5I2a5L8PldQd7DOesmuzu6dYr9j5oNaTMLQcl6YZaSwNHf-e_68kwic=GyleF5p7e_7edxztYNsGXaNdUbf8nHjIejkBsyhAIq-cfDfnunf4jTxex69jid9P3jUHW9IUiMTSrc6buqq1lbHOb56nlq0AvvryDN-BUCHCGNG2d-btc7KoGRec-3RrfUU46Y9iCWiL64_qtsj06DE6ClE8gHZg5JQjRw6TkEQ=@rqdatad-pro.ricequant.com:16011')

if __name__=='__main__':
    for i in instruments:
        if not os.path.exists(f'{DATA_DIR}/{k_line_type}/{i}'):
            os.makedirs(f'{DATA_DIR}/{k_line_type}/{i}')

        df_domiant = pd.DataFrame(rqdatac.futures.get_dominant_price(underlying_symbols=i, frequency=k_line_type,\
                            adjust_type='post', adjust_method='prev_close_ratio',start_date='20241225',end_date='20250101'))
        #df_domiant.to_csv(f'.{DATA_DIR}/{k_line_type}/{i}/{i}.csv',index=True,  encoding='utf-8')
        print(df_domiant.columns)