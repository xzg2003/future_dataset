instruments= ['A','AG','AL','AP','AU','BU','C','CF','CJ','CS',
             'CU','EB','EG','FG','FU','HC','I','IC','IF','IH',
            'J','JD','JM','L','LU','LH','M','MA','NI','OI','P',
            'PB','PF','PG','PK','PP','RB','RM','RU','SA','SF',
            'SM','SN','SP','SR','SC','SS','TA','T','TF','UR','V','Y','ZN'] #期货类型

# k线类型
k_line_type = '5m'

# 滑动长度
lengths = [10, 20, 40, 80, 120, 180]

# 因子名称列表，存放所有因子名称
factor_names = [
    "TSMOM",
    "IDMOM",
    "XSMOM",
    "Acceleration",
    "Bias",
    "RSI",
    "IntradayMOM",
    "OvernightMOM",
    "RobustMOM",
    "TrendStrength",
    "Tr",
    "FCT_Ac_Tr_1",
    "FCT_Ar_1",
    "FCT_Bias_1",
    "FCT_Br_1",
    "FCT_Cmf_1",
    "FCT_Pubu_1",
    "FCT_Pubu_Atr_Dfive",
    "FCT_Pubu_Vol_Dfive",
    "FCT_R_Div_RStd",
    "FCT_Return_Cumsum_1",
    "FCT_Sdrm_1",
    "FCT_Sdrm_Atr_Dfive",
    "FCT_Si",
    "FCT_Srmi",
    "FCT_Support_Close_Thr_1",
    "FCT_Support_Close_Thr_Boll_1",
    "FCT_Tsi_1",
    "FCT_Tsi_Atr_Dfive",
    "FCT_TSI_Ref_1",
    "FCT_Tsi_Vol_Dfive",
    "FCT_Vmacd",
    "FCT_Vol_Close_Corr_1",
    "FCT_Vol_Cumsum_1",
    "FCT_Vol_DFive_1",
    "FCT_Vol_Return_Corr_1",
    "FCT_Vr"
]

"""
由于各个因子对应的计算结果文件名称不同，这里需要对每个因子进行分类
一级分类，是一个字典，对所有因子命名规则进行分类
二级分类，是多个列表，将对应的因子命名规则归类到列表中
由于大部分因子的命名都需要length，这些因子就不列在这些列表中，在程序中默认加length即可

较为特殊的是 Vmacd 这个因子，这个因子计算出的数据是3个不同的子数据，暂时无法给出明确的命名，归为默认
"""
factor_categories = {
    # 不需要滑动窗口的因子
    "no_length":            ["Tr", "IDMOM", "IntradayMOM", "OvernightMOM", "FCT_Return_Cumsum_1", "FCT_Vmacd", "FCT_Vol_Cumsum_1"],

    # 需要 length 与 atr 的因子
    "length_atr":           ["FCT_Sdrm_Atr_Dfive"],

    # 需要 length 与 thr 的因子
    "length_thr":           ["FCT_Support_Close_Thr_1"],

    # 需要 length 与 n_std 的因子
    "length_n_std":         ["FCT_Support_Close_Thr_Boll_1"],

    # 需要 short 与 long 的因子
    "short_long":           ["FCT_Pubu_1", "FCT_Tsi_1", "FCT_TSI_Ref_1"],

    # 需要 short，long 与 atr 的因子
    "short_long_atr":       ["FCT_Pubu_Atr_Dfive", "FCT_Tsi_Atr_Dfive"],

    # 需要 short，long 与 vol 的因子
    "short_long_vol":       ["FCT_Pubu_Vol_Dfive", "FCT_Tsi_Vol_Dfive"],

    # 需要 fast，slow 与 signal 的因子
    "fast_slow_signal":     ["FCT_Vmacd"],
}

"""
一些程序中默认的数据，如 short，long 等等
由于目前一直没有拿到准确的计算，这里给出的数值都是默认的
"""
default_data = {
    # 短期均线长度
    "short":            5,

    # 长期均线长度
    "long":             20,

    # 平均真实波幅 计算长度
    "atr_length":       14,

    # 波动率 计算长度
    "vol_length":       14,

    # 百分位数
    "thr":              0.3,

    # n_std 计算
    'n_std':            2,

    # 短期交易的计算长度（Vmacd）
    'fast':             12,

    # 长期交易的计算长度（Vmacd）
    'slow':             26,

    # 计算特征值（Vmacd）
    'signal':           9,
}