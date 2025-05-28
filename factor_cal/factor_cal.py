import os       # 与路径操作相关的包，用于管理文件
import pandas

from .FCT_Ac_Tr_1                   import      FCT_Ac_Tr_1
from .FCT_Ar_1                      import      FCT_Ar_1
from .FCT_Bias_1                    import      FCT_Bias_1
from .FCT_Br_1                      import      FCT_Br_1
from .FCT_Cmf_1                     import      FCT_Cmf_1
from .FCT_Pubu_1                    import      FCT_Pubu_1
from .FCT_Pubu_Atr_Dfive            import      FCT_Pubu_Atr_Dfive
from .FCT_Pubu_Vol_Dfive            import      FCT_Pubu_Vol_Dfive
from .FCT_R_Div_RStd                import      FCT_R_Div_RStd
from .FCT_Return_Cumsum_1           import      FCT_Return_Cumsum_1
from .FCT_Sdrm_1                    import      FCT_Sdrm_1
from .FCT_Sdrm_Atr_Dfive            import      FCT_Sdrm_Atr_Dfive
from .FCT_Si                        import      FCT_Si
from .FCT_Srmi                      import      FCT_Srmi
from .FCT_Support_Close_Thr_1       import      FCT_Support_Close_Thr_1
from .FCT_Support_Close_Thr_Boll_1  import      FCT_Support_Close_Thr_Boll_1
from .FCT_Tsi_1                     import      FCT_Tsi_1
from .FCT_Tsi_Atr_Dfive             import      FCT_Tsi_Atr_Dfive
from .FCT_TSI_Ref_1                 import      FCT_TSI_Ref_1
from .FCT_Tsi_Vol_Dfive             import      FCT_Tsi_Vol_Dfive
from .FCT_Vmacd                     import      FCT_Vmacd
from .FCT_Vol_Close_Corr_1          import      FCT_Vol_Close_Corr_1
from .FCT_Vol_Cumsum_1              import      FCT_Vol_Cumsum_1
from .FCT_Vol_DFive_1               import      FCT_Vol_DFive_1
from .FCT_Vol_Return_Corr_1         import      FCT_Vol_Return_Corr_1
from .FCT_Vr                        import      FCT_Vr
from .Tr                            import      Tr

from .TSMOM                         import      TSMOM
from .IDMOM                         import      IDMOM
from .XSMOM                         import      XSMOM
from .RobustMOM                     import      RobustMOM
from .Acceleration                  import      Acceleration
from .Bias                          import      Bias
from .RSI                           import      RSI
from .IntradayMOM                   import      IntradayMOM
from .OvernightMOM                  import      OvernightMOM
from .TrendStrength                 import      TrendStrength

# 设置工作目录为当前脚本所在的目录
os.chdir(os.path.dirname(os.path.abspath(__file__)))

class factor_calculator:
    def __init__(self, instruments, k_line_type, lengths, instruments_mindiff):
        """
        初始化因子计算器
        :param instruments: 期货品种列表
        :param k_line_type: K线类型
        :param lengths:     滑动平均长度列表
        """
        self.instruments = instruments
        self.k_line_type = k_line_type
        self.lengths = lengths
        self.instruments_mindiff = instruments_mindiff

        """
        初始化所有因子计算器
        以字典的形式，将每个计算器与其名称进行对应，便于在程序中调用
        
        这里优先计算 Tr 因子，因为后续很多因子计算都需要调用 Tr 的数据
        先计算 Tr，在计算其他因子时可以调用 Tr.csv 文件中的数据，简化计算
        """
        self.factors_dict = {
            "TSMOM":                        TSMOM(),
            "IDMOM":                        IDMOM(),
            "XSMOM":                        XSMOM(),
            "Acceleration":                 Acceleration(),
            "Bias":                         Bias(),
            "RSI":                          RSI(),
            "IntradayMOM":                  IntradayMOM(),
            "OvernightMOM":                 OvernightMOM(),
            "RobustMOM":                    RobustMOM(),
            "TrendStrength":                TrendStrength(),
            "Tr":                           Tr(),
            "FCT_Ac_Tr_1":                  FCT_Ac_Tr_1(),
            "FCT_Ar_1":                     FCT_Ar_1(),
            "FCT_Bias_1":                   FCT_Bias_1(),
            "FCT_Br_1":                     FCT_Br_1(),
            "FCT_Cmf_1":                    FCT_Cmf_1(),
            "FCT_Pubu_1":                   FCT_Pubu_1(),
            "FCT_Pubu_Atr_Dfive":           FCT_Pubu_Atr_Dfive(),
            "FCT_Pubu_Vol_Dfive":           FCT_Pubu_Vol_Dfive(),
            "FCT_R_Div_RStd":               FCT_R_Div_RStd(),
            "FCT_Return_Cumsum_1":          FCT_Return_Cumsum_1(),
            "FCT_Sdrm_1":                   FCT_Sdrm_1(),
            "FCT_Sdrm_Atr_Dfive":           FCT_Sdrm_Atr_Dfive(),
            "FCT_Si":                       FCT_Si(),
            "FCT_Srmi":                     FCT_Srmi(),
            "FCT_Support_Close_Thr_1":      FCT_Support_Close_Thr_1(),
            "FCT_Support_Close_Thr_Boll_1": FCT_Support_Close_Thr_Boll_1(),
            "FCT_Tsi_1":                    FCT_Tsi_1(),
            "FCT_Tsi_Atr_Dfive":            FCT_Tsi_Atr_Dfive(),
            "FCT_TSI_Ref_1":                FCT_TSI_Ref_1(),
            "FCT_Tsi_Vol_Dfive":            FCT_Tsi_Vol_Dfive(),
            "FCT_Vmacd":                    FCT_Vmacd(),
            "FCT_Vol_Close_Corr_1":         FCT_Vol_Close_Corr_1(),
            "FCT_Vol_Cumsum_1":             FCT_Vol_Cumsum_1(),
            "FCT_Vol_DFive_1":              FCT_Vol_DFive_1(),
            "FCT_Vol_Return_Corr_1":        FCT_Vol_Return_Corr_1(),
            "FCT_Vr":                       FCT_Vr(),
        }

        self.no_length = ["Tr", "IDMOM", "IntradayMOM", "OvernightMOM", "FCT_Return_Cumsum_1", "FCT_Vmacd", "FCT_Vol_Cumsum_1"]
        self.length_atr = ["FCT_Sdrm_Atr_Dfive"]
        self.length_thr = ["FCT_Support_Close_Thr_1"]
        self.length_n_std = ["FCT_Support_Close_Thr_Boll_1"]
        self.short_long = ["FCT_Pubu_1", "FCT_Tsi_1", "FCT_TSI_Ref_1"]
        self.short_long_atr = ["FCT_Pubu_Atr_Dfive", "FCT_Tsi_Atr_Dfive"]
        self.short_long_vol = ["FCT_Pubu_Vol_Dfive", "FCT_Tsi_Vol_Dfive"]
        self.fast_slow_signal = ["FCT_Vmacd"]

    def factors_cal(self):
        """
        调用所有计算器，计算相应因子并保存到文件夹中
        """
        for instrument in self.instruments:
            # 构建数据路径
            data_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), f'../data/5m/{instrument}/{instrument}.csv')
            print(f"Trying to read the file:{data_path}")
            if not os.path.exists(data_path):
                print(f"Not exist:{data_path}")
                continue

            try:
                # 读取数据
                df = pandas.read_csv(data_path)
            except Exception as e:
                print(f'Read failed:{data_path}, error info:{e}')
                continue

            # 遍历因子字典，逐个计算因子
            for factor_name, calculator in self.factors_dict.items():
                for length in self.lengths:
                    # 构建param字典，包含df和length
                    param = {
                        'df':           df,
                        'instrument':   instrument,
                        'length':       length,
                        'mindiff':      self.instruments_mindiff.get(instrument, None),
                        'short':        5,
                        'long':         20,

                        'atr_length':   14,

                        'vol_length':   14,

                        'thr':          0.3,

                        'n_std':        2,

                        'fast':         12,
                        'slow':         26,
                        'signal':       9,
                    }

                    # 检查 mindiff 是否存在
                    if param['mindiff'] is None:
                        print(f"No mindiff for {instrument}, skip")
                        continue

                    try:
                        # 设置保存路径，根据命名规则分开讨论
                        if factor_name in self.no_length:
                            save_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), f'../data/{self.k_line_type}/{instrument}/{factor_name}.csv')
                        elif factor_name in self.short_long:
                            save_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), f'../data/{self.k_line_type}/{instrument}/{factor_name}@{param["short"]}_{param["long"]}.csv')
                        elif factor_name in self.length_thr:
                            save_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), f'../data/{self.k_line_type}/{instrument}/{factor_name}@{length}_{param["thr"]}.csv')
                        elif factor_name in self.length_atr:
                            save_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), f'../data/{self.k_line_type}/{instrument}/{factor_name}@{length}_{param["atr_length"]}.csv')
                        elif factor_name in self.length_n_std:
                            save_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), f'../data/{self.k_line_type}/{instrument}/{factor_name}@{length}_{param["n_std"]}.csv')
                        elif factor_name in self.short_long_atr:
                            save_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), f'../data/{self.k_line_type}/{instrument}/{factor_name}@{param["short"]}_{param["long"]}_{param["atr_length"]}.csv')
                        elif factor_name in self.short_long_vol:
                            save_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), f'../data/{self.k_line_type}/{instrument}/{factor_name}@{param["short"]}_{param["long"]}_{param["vol_length"]}.csv')
                        else:
                            save_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), f'../data/{self.k_line_type}/{instrument}/{factor_name}@{length}.csv')

                        # 检查文件是否存在，以跳出当前因子计算的循环
                        if os.path.exists(save_path):
                            print(f"{save_path}已存在，跳过该因子该长度的计算")
                            continue

                        # 计算每一个因子，调用 calculator.formula 并传入参数进行计算
                        result = calculator.formula(param)

                        # 利用 os.makedirs 设置一个路径，并利用to_csv保存结果
                        os.makedirs(os.path.dirname(save_path), exist_ok=True)
                        result.to_csv(save_path, index=False)

                        # 保存成功信息回报
                        print(f"instrument:{instrument} factor:{save_path} success.")
                    except Exception as e:
                        # 当因子计算出错时报错
                        print(f"error at{save_path}, {e}")


"""
# 主程序入口
if __name__ == "__main__":
    '''
    数据的初始化，在main.py里面也有相同的部分，便于使用者调整数据处理的范围
    instruments:    期货品种
    k_line_type:    k线类型
    lengths:        滑动平均长度
    '''
    instruments = ['A']
    k_line_type = '5m'
    lengths = [10, 20, 40, 80, 120, 180]

    # 创建因子计算器实例，以调用内部的函数
    calculator = factor_calculator(instruments, k_line_type, lengths, mindiff)

    # 计算所有因子
    calculator.factors_cal()
"""