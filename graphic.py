import matplotlib.pyplot as plt
import pandas as pd
import os

# 设置基础路径为 C盘用户Admin目录下
base_path = r'C:\Users\Admin\.quantative\data\5m'

# 设置期货类型列表
instruments = ['A', 'AG', 'AL', 'AP', 'AU', 'BU', 'C', 'CF', 'CJ', 'CS',
               'CU', 'EB', 'EG', 'FG', 'FU', 'HC', 'I', 'IC', 'IF', 'IH',
               'J', 'JD', 'JM', 'L', 'LU', 'LH', 'M', 'MA', 'NI', 'OI', 'P',
               'PB', 'PF', 'PG', 'PK', 'PP', 'RB', 'RM', 'RU', 'SA', 'SF',
               'SM', 'SN', 'SP', 'SR', 'SC', 'SS', 'TA', 'T', 'TF', 'UR', 'V', 'Y', 'ZN']

# 创建一个分布图，并设置其大小
plt.figure(figsize=(14,10))

for instrument in instruments:
    # 构建绝对路径
    data_path = os.path.join(base_path, instrument, 'FCT_Cmf_1@10.csv')
    try:
        df = pd.read_csv(data_path)
        # 绘制曲线图
        plt.hist(df['FCT_Cmf_1@10'], label=instrument)

    except FileNotFoundError:
        print(f"错误：文件{data_path}未找到")
    except Exception as e:
        print(f"发生未知错误：{e}")

plt.title('FCT_Cmf_1@10 in every instruments')
plt.xlabel('FCT_Cmf_1@10')
plt.ylabel('Frequency')
plt.legend(loc="center right")
plt.grid(True)
plt.show()
