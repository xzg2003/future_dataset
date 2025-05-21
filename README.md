# 因子评价框架
## 运行方式
- 首先在 `/factor_cal` 目录下放入因子计算代码，并运行 `factor_cal.py` 计算因子值
- 需要评估的因子的名称存放在 `factor_name.csv` 中
- 运行 `main.py`，注意输入因子名称和 k 线类型
- `delete.py` 用于删除计算失误的因子

## 结果保存
- 结果保存在 `./result/{k_line}/{factor_name}` 中，每个因子一个独立的文件夹 