import rqdatac
import pandas as pd

# 初始化 RiceQuant 数据服务（你需要先注册账号，然后替换为你自己的账户信息）
rqdatac.init(username='17818228135', password='123456')

# 选择期货合约，这里以螺纹钢主力合约为例
symbol = 'RB9999.XSGE'  # 主力合约的代码，9999 表示主力

# 下载 K 线数据（这里是日线）
df = rqdatac.get_price(
    order_book_ids= [symbol],
    start_date='2023-01-01',
    end_date='2024-12-31',
    frequency='1d',   # 日线，可改为 '1m', '5m', '1h' 等
    fields=['open', 'high', 'low', 'close', 'volume', 'open_interest'],
    adjust_type='none'
)

# 输出前几行
print(df.head())

# 可选：保存为 CSV 文件
df.to_csv('RB9999_daily.csv')
