import matplotlib.pyplot as plt
import pandas as pd
import os

# 当前脚本的绝对路径目录
base_dir = os.path.dirname(os.path.abspath(__file__))

# 设置期货类型列表
instruments = ['A', 'AG', 'AL', 'AP', 'AU', 'BU', 'C', 'CF', 'CJ', 'CS',
               'CU', 'EB', 'EG', 'FG', 'FU', 'HC', 'I', 'IC', 'IF', 'IH',
               'J', 'JD', 'JM', 'L', 'LU', 'LH', 'M', 'MA', 'NI', 'OI', 'P',
               'PB', 'PF', 'PG', 'PK', 'PP', 'RB', 'RM', 'RU', 'SA', 'SF',
               'SM', 'SN', 'SP', 'SR', 'SC', 'SS', 'TA', 'T', 'TF', 'UR', 'V', 'Y', 'ZN']

plt.figure(figsize=(14, 10))

for instrument in instruments:
    data_path = os.path.join(base_dir, 'data', '5m', instrument, 'FCT_Bias_1@10.csv')
    try:
        df = pd.read_csv(data_path)
        plt.plot(df['FCT_Bias_1@10'], label=instrument)
    except FileNotFoundError:
        print(f"错误：文件 {data_path} 未找到")
    except Exception as e:
        print(f"发生未知错误：{e}")

# 处理整体数据曲线
main_data_path = os.path.join(base_dir, 'data', '5m', instrument,'FCT_Bias_1@10.csv')
try:
    df = pd.read_csv(main_data_path)
    plt.plot(df['FCT_Bias_1@10'], label='All', linewidth=3, color='black')
except FileNotFoundError:
    print(f"错误：文件 {main_data_path} 未找到")
except Exception as e:
    print(f"发生未知错误：{e}")

plt.title('FCT_Bias_1@10 for Different Instruments')
plt.xlabel('Index')
plt.ylabel('Value')
plt.legend()
plt.grid(True)
plt.show()




