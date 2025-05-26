# 删除期货因子的代码，万一大家算出来的因子有问题可以删了重新算
import os

# 期货类型
instruments = [
    'A', 'AG', 'AL', 'AP', 'AU', 'BU', 'C', 'CF', 'CJ', 'CS',
    'CU', 'EB', 'EG', 'FG', 'FU', 'HC', 'I', 'IC', 'IF', 'IH',
    'J', 'JD', 'JM', 'L', 'LU', 'LH', 'M', 'MA', 'NI', 'OI', 'P',
    'PB', 'PF', 'PG', 'PK', 'PP', 'RB', 'RM', 'RU', 'SA', 'SF',
    'SM', 'SN', 'SP', 'SR', 'SC', 'SS', 'TA', 'T', 'TF', 'UR', 'V', 'Y', 'ZN'
]


def delete_factor(k_line, factor_lists):
    for name in factor_lists:
        # 保证有.csv后缀
        if not name.endswith('.csv'):
            name_csv = name + '.csv'
        else:
            name_csv = name
        deleted = False
        for i in instruments:
            file_path = f'./data/{k_line}/{i}/{name_csv}'
            if os.path.exists(file_path):
                os.remove(file_path)
                print(f'已删除: {file_path}')
                deleted = True
        if not deleted:
            print(f'{name_csv} 在 {k_line} 下未找到对应文件')


if __name__ == '__main__':
    # 支持多周期
    k_lines = ['1d', '5m']
    factor_lists = [
        "FCT_Pubu_1@5_20"
    ]
    for k_line in k_lines:
        delete_factor(k_line, factor_lists)