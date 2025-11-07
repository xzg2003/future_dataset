"""
因子计算模块

该模块包含量化交易回测系统中使用的各种技术因子计算函数，
用于生成模型训练和回测所需的特征数据。

Submodules
----------
FCT_Ac_Tr_1 : 模块
    Accumulation/Swing Index (ASI) 累积摆动指数因子计算

FCT_Ar_1 : 模块
    Active Return 活跃收益因子计算

FCT_Bias_1 : 模块
    BIAS 乖离率因子计算

FCT_Br_1 : 模块
    BR 多空指标因子计算

FCT_Cmf_1 : 模块
    Chaikin Money Flow 蔡金货币流量因子计算

FCT_Pubu_1 : 模块
    能量潮（OBV）相关因子计算

FCT_R_Div_RStd : 模块
    收益率与收益率标准差比值因子计算

FCT_Return_Cumsum_1 : 模块
    累计收益率因子计算

FCT_Rsi_1 : 模块
    RSI 相对强弱指数因子计算

FCT_Sdrm_1 : 模块
    标准差修正因子计算

FCT_Si : 模块
    摆动指数因子计算

FCT_Srmi : 模块
    SRMI 因子计算

FCT_Support_Close_Thr_1 : 模块
    支撑位收盘价阈值因子计算

FCT_Support_Close_Thr_Boll_1 : 模块
    布林带支撑位相关因子计算

FCT_Tsi_1 : 模块
    TSI 真实强度指数因子计算

FCT_Tsi_Atr_Dfive : 模块
    TSI 结合 ATR 的因子计算

FCT_Tsi_Ref_1 : 模块
    TSI 参考值因子计算

FCT_Tsi_Vol_Dfive : 模块
    TSI 结合成交量的因子计算

FCT_Vmacd : 模块
    VMACD 量价 MACD 因子计算

FCT_Vol_Close_Corr_1 : 模块
    成交量与收盘价相关性因子计算

FCT_Vol_Cumsum_1 : 模块
    累计成交量因子计算

FCT_Vol_DFive_1 : 模块
    成交量五日变化因子计算

FCT_Vol_Return_Corr_1 : 模块
    成交量与收益率相关性因子计算

FCT_Vr : 模块
    VR 成交量变异率因子计算

Tr : 模块
    趋势判断相关因子计算

factor_cal : 模块
    因子计算主程序，协调各因子的计算流程

主要功能
--------
1. 技术指标因子计算
2. 价格相关因子生成
3. 成交量相关因子生成
4. 波动率相关因子生成
5. 动量相关因子生成

使用方法
--------
因子计算通常由 factor_cal.factor_cal 函数统一调用，会自动遍历
并计算所有因子模块中定义的因子。

每个因子模块通常包含以下函数：
- calc_fct(df, param) : 计算因子值
- get_factor_name() : 获取因子名称

该模块为机器学习模型提供特征数据，是量化策略开发的基础。
"""
