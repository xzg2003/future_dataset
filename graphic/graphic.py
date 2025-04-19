import matplotlib.pyplot as plt
import pandas as pd
import os

# 设置相对路径
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# 创建一个分布图，并设置其大小
plt.figure(figsize=(14,10))



# 设置文件读取路径，并读取其中的数据
data_path = (f'../data/merge/5m/FCT_Ac_Tr_1@10.csv')
df = pd.read_csv(data_path)
try:
    # 绘制曲线图
    plt.plot(df['FCT_Ac_Tr_1@10'])

except FileExistsError:
    print(f"错误：文件{data_path}未找到")
except Exception as e:
    print(f"发生未知错误：{e}")

"""
title:  设置图表的名称
xlabel：设置x轴的名称
ylabel：设置y轴的名称
legend：在图中添加图例
grid：  添加网格线
show：  显示图
"""

plt.title('Factor FCT_Ac_Tr_1@10 in every instruments')
plt.xlabel('FCT_Ac_Tr_1@10')
plt.ylabel('Frequency')

plt.legend(loc="center right")
plt.grid(True)
plt.show()
