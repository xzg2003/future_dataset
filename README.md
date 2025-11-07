# 因子库&因子评价系统
## 期货数据库下载
- [rqsdk官方文档](https://www.ricequant.com/doc/rqsdk/)
- 运行 `pip install rqdatac`
- 用 `rqsdk` 库下载 k 线数据，日期范围设置为 `20100101—20250101`，每个期货品种的数据保存为 `{DATA_DIR}/{k_line}/{instrument}/{instrument}.csv`，其中 `k_line` 为 k 线的类型，5 分钟线记为 `5m`，1 日线纪为 `1d`。下载数据的代码为 `./get_data.py`
- `./delete.py` 用于删除计算错误的代码

## 因子库
### 配置文件说明
- 路径为 `./factor_cal/config.py`
```py
# 需要计算的期货类型
instruments= ['A','AG','AL','AP','AU','BU','C','CF','CJ','CS',
             'CU','EB','EG','FG','FU','HC','I','IC','IF','IH',
            'J','JD','JM','L','LU','LH','M','MA','NI','OI','P',
            'PB','PF','PG','PK','PP','RB','RM','RU','SA','SF',
            'SM','SN','SP','SR','SC','SS','TA','T','TF','UR','V','Y','ZN'] 

# 数据库的根目录
DATA_DIR = 'C:/wzx/KCL/dataset/future_data'

# k线类型
k_line_type = '1d'
```
### 代码编写规则
- 因子的计算代码存储在 `./factor_cal/xxx` 中，由 `factor_total.py` 集成调用
- 因子计算的参数存放在 `./factor_cal/xxx/factor_param.json` 中
- 获取已经计算出的因子数据的代码为 `./factor_cal/get_exist_data.py`
- 每一类因子的计算代码命名为 `./factor_cal/xxx/{factor}.py`，代码中类的封装规则如下：
``` py
import os
import numpy
import pandas
import sys
sys.path.append('.')
from factor_cal.get_exist_data import get_exist_data

class factor:
    def __init__(self):
        pass

    def formula(self, param: dict):
        # 参数由字典格式传入，事先在文件中定义好
        # df 为当前所计算的品种所对应的市场数据，instrument 为当前品种的名称，mindiff为当前品种的最小变动单位，factor_name为因子名称，这些都是必须传入的参数，已经在集成代码中传入
        # depend_on 

        # 从参数字典中获取 df
        df = param.get('df', None)
        if df is None:
            raise ValueError("no 'df' in param")

        # 从参数字典中获取 instrument
        instrument = param.get('instrument', None)
        if instrument is None:
            raise ValueError("param miss instrument")

        # 从参数字典中获取 factor_name
        factor_name = param.get('factor_name', None)
        if factor_name is None:
            raise ValueError("param missing factor_name")

        # 从参数字典中获取 mindiff
        mindiff = param.get('mindiff', None)
        if mindiff is None:
            raise ValueError("param missing mindiff")
        
        # 从参数字典中获取 depend_on
        depend_on = param.get('depend_on', None)
        if depend_on is None:
            raise ValueError("no 'depend_on' in param")

        # 获取已经存在的因子
        exist_data = get_exist_data(instrument, depend_on)

        # todo
        # df[facotr_name] = ...        
        result = df[[f'{factor_name}']].copy()
        return result
```
- 因子计算结果保存在 `f'{DATA_DIR}/{k_line_type}/{instrument}/{factor_name}.csv'` 中
### 因子参数命名规则
- 每个因子类的名称作为字典的一个键名
- 键名对应的键值是字典列表，列表中每个字典包含计算该因子需要用到的参数，键名表示参数名称，键值表示参数值
- 参数名和因子计算代码中的参数名对应，由代码编写者自定义
```py
{"FCT_Tsi_Vol_Dfive": [
    {
      "factor_name": "FCT_Tsi_Vol_Dfive@3_1_5",# 因子名称，由因子类名@{参数}组成，必须
      "length": 3, # 因子计算参数
      "vol_length": 5, # 因子计算参数
      "depend_on": "FCT_Tsi_1@3" # 需要依赖之前计算的因子，键值为已经存在的因子。如果需要多个因子可以使用列表传入。所依赖的因子必须在计算当前因子前计算出来。
    },
    {
      "factor_name": "FCT_Tsi_Vol_Dfive@5_1_5",
      "length": 5,
      "vol_length": 5,
      "depend_on": "FCT_Tsi_1@5"
    },
    {
      "factor_name": "FCT_Tsi_Vol_Dfive@10_1_5",
      "length": 10,
      "vol_length": 5,
      "depend_on": "FCT_Tsi_1@10"
    },
    {
      "factor_name": "FCT_Tsi_Vol_Dfive@20_1_5",
      "length": 20,
      "vol_length": 5,
      "depend_on": "FCT_Tsi_1@20"
    },
    {
      "factor_name": "FCT_Tsi_Vol_Dfive@30_1_5",
      "length": 30,
      "vol_length": 5,
      "depend_on": "FCT_Tsi_1@30"
    }
  ]
}
```
### 协作方式
1. 熟悉代码结构和传参规则（可以运行 `./factor_cal/test` 里面的文件）
2. 在本地按照目录结构搭建期货数据库（也可以直接使用服务器上现成的数据库）
3. 复制集成代码文件，在本地完成因子计算代码的编写并按格式规定参数
4. 运行调试，检查因子的评价报告是否符合验收标准
5. 确认无误后在 `./factor_cal` 下创建一个 `./factor_cal/xxx`，把因子计算代码、集成代码、参数文件复制进去，即可完成因子开发

### 注意事项
- 一定要确保代码运行无误才能上传
- 入库前需要运行因子评价代码对因子进行评价，确保因子有市场意义
- 计算结果只保留因子值的那一列，保留缺失值和极值（确保能和市场数据时序对齐），属性列用因子名称命名（包含参数后缀）

## 因子评价框架
### 配置文件说明
- 路径为 `./factor_cal/config.py`
```py
instruments= ['A','AG','AL','AP','AU','BU','C','CF','CJ','CS',
             'CU','EB','EG','FG','FU','HC','I','IC','IF','IH',
            'J','JD','JM','L','LU','LH','M','MA','NI','OI','P',
            'PB','PF','PG','PK','PP','RB','RM','RU','SA','SF',
            'SM','SN','SP','SR','SC','SS','TA','T','TF','UR','V','Y','ZN'] #期货类型

# 数据目录
DATA_DIR = 'C:/wzx/KCL/dataset/future_data'

# k线类型
k_line_type = '1d'

# 待评价因子
factors = ['FCT_Ac_Tr_1@5', 'FCT_Ar_1@5', 'FCT_Bias_1@5', 'FCT_Br_1@5', 'FCT_Cmf_1@5']
```

### 结构
- 评估代码存放在 `./factor_judge` 中，`layer_yiled.py` 计算分层收益，`statistic.py` 计算统计学参数，`mutal_IC.py` 计算不同因子之间的相关系数
- `main.py` 跑通整套流程

### 运行方法
- 在 `config.py` 中输入待评价的因子（必须提前计算好），运行 `main.py` 即可
- 结果保存在 `./result/{k_line_type}/{factor_name}` 中，为 html 文件