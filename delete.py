# 计算错误的因子可以进行删除
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

def delete_factor(k_line, factor_lists):
    for name in factor_lists:
        for i in instruments:
            if os.path.exists(f'{DATA_DIR}/{k_line}/{i}/{name}.csv'):
                os.remove(f'{DATA_DIR}/{k_line}/{i}/{name}.csv')
        print(f'{name} 删除成功')
    
if __name__ == "__main__":
    delete_factor(k_line_type , ['1','2','3','4','5','6','7'])