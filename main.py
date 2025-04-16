from factor_cal.factor_cal import factor_calculator

def main():
    '''
    各个参数的设置，
    instruments:    期货品种
    k_line_type:    k线类型
    lengths:        滑动平均长度
    '''
    instruments = ['A','AG','AL','AP','AU','BU','C','CF','CJ','CS',\
        'CU','EB','EG','FG','FU','HC','I','IC','IF','IH',\
        'J','JD','JM','L','LU','LH','M','MA','NI','OI','P',\
        'PB','PF','PG','PK','PP','RB','RM','RU','SA','SF',\
        'SM','SN','SP','SR','SC','SS','TA','T','TF','UR','V','Y','ZN']
    k_line_type = '5m'
    lengths = [10, 20, 40, 80, 120, 180]

    # 创建因子计算器实例，以调用内部的函数
    calculator = factor_calculator(instruments, k_line_type, lengths)

    # 调用计算函数
    calculator.factors_cal()

if __name__ == '__main__':
    main()