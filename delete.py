# 删除期货因子的代码，万一大家算出来的因子有问题可以删了重新算
import os
# 期货类型
instruments=['A','AG','AL','AP','AU','BU','C','CF','CJ','CS',\
      'CU','EB','EG','FG','FU','HC','I','IC','IF','IH',\
        'J','JD','JM','L','LU','LH','M','MA','NI','OI','P',\
      'PB','PF','PG','PK','PP','RB','RM','RU','SA','SF',\
        'SM','SN','SP','SR','SC','SS','TA','T','TF','UR','V','Y','ZN']

def delete_factor(k_line,factor_lists):
    for name in factor_lists:
        for i in instruments:
            if os.path.exists(f'./data/{k_line}/{i}/{name}.csv'):
                os.remove(f'./data/{k_line}/{i}/{name}.csv')
        print(f'{name} 删除成功')
    
delete_factor('1d',['1','2','3','4','5','6',\
                    'Tr','FCT_Ac_Tr_1@5','FCT_Ac_Tr_1@10','FCT_Ac_Tr_1@20','FCT_Ac_Tr_1@40','FCT_Ac_Tr_1@80',\
                    'FCT_Ac_Tr_1@120','FCT_Ac_Tr_1@180','FCT_Ar_1@5','FCT_Ar_1@10','FCT_Ar_1@20','FCT_Ar_1@40',\
                      'FCT_Ar_1@80','FCT_Ar_1@120','FCT_Ar_1@180','FCT_Bias_1@5','FCT_Bias_1@10','FCT_Bias_1@20',\
                        'FCT_Bias_1@40','FCT_Bias_1@80','FCT_Bias_1@120','FCT_Bias_1@180',\
                          'FCT_Br_1@5','FCT_Br_1@10','FCT_Br_1@20','FCT_Br_1@40','FCT_Br_1@80',\
                            'FCT_Br_1@120','FCT_Br_1@180','FCT_Cmf_1@5',\
                              'FCT_Cmf_1@10','FCT_Cmf_1@20','FCT_Cmf_1@40','FCT_Cmf_1@80',\
                                'FCT_Cmf_1@120','FCT_Cmf_1@180', 'FCT_Donchian_Vol_Dfive@5', 'FCT_Donchian_Vol_Dfive@10',\
                                  'FCT_Donchian_Vol_Dfive@20', 'FCT_Donchian_Vol_Dfive@40', 'FCT_Donchian_Vol_Dfive@80',\
                                    'FCT_Donchian_Vol_Dfive@120', 'FCT_Donchian_Vol_Dfive@180', 'FCT_Donchian_Vol_Dfive'])