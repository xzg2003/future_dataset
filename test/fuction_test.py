import pandas as pd

# 创建一个 Series
rolling_mean_tr = pd.Series([0.01, 0.02, 0.03, 0.04, 0.05])

# 标量值
mindiff = 0.03

# 比较
result = rolling_mean_tr <= mindiff
print(result)