import matplotlib.pyplot as plt
import pandas as pd
import os
import numpy as np

# 设置相对路径
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# 创建一个分布图，并设置其大小
plt.figure(figsize=(14,10))

# 自定义区间范围
bins = np.linspace(-15, 20, 40000)

# 设置文件读取路径，并读取其中的数据
data_path = (f'../data/merge/5m/FCT_Ac_Tr_1@10.csv')
df = pd.read_csv(data_path)

# 统计每个区间内的数据点数量
hist, _ = np.histogram(df['FCT_Ac_Tr_1@10'], bins=bins)

# 计算每个区间的中心位置
interval_centers = bins[:-1] + np.diff(bins) / 2

# 绘制柱状图
plt.bar(interval_centers, hist, width=np.diff(bins)[0], edgecolor='black')

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
