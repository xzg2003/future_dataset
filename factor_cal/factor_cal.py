import os       # 与路径操作相关的包，用于管理文件
import pandas as pd
import sys     

from FCT_Ac_Tr_1   import      FCT_Ac_Tr_1
from FCT_Ar_1      import      FCT_Ar_1
from FCT_Bias_1    import      FCT_Bias_1
from FCT_Br_1      import      FCT_Br_1
from FCT_Cmf_1     import      FCT_Cmf_1
from Tr            import      Tr

from Amihud import Amihud
from Turnover import Turnover
# Bid_Ask_Spread：买卖差价因子，缺少 bid1 和 ask1 列数据
# Order_Book_Length : 由于缺少 bid_size 和 ask_size 而暂时无法计算

from FCT_Donchian_Vol_Dfive import FCT_Donchian_Vol_Dfive
from FCT_Dmi_Adxr import FCT_Dmi_Adxr
from FCT_Dmi_Adx import FCT_Dmi_Adx
from FCT_Demark_Vol_Dfive import FCT_Demark_Vol_Dfive
from FCT_Demark_Ref_1 import FCT_Demark_Ref_1
from FCT_Demark_Atr_Dfive import FCT_Demark_Atr_Dfive
from FCT_Dbcd import FCT_Dbcd
from FCT_Cr_Vol_Dfive import FCT_Cr_Vol_Dfive
from FCT_Cr_Ref_1 import FCT_Cr_Ref_1
from FCT_Cr_Atr_Dfive import FCT_Cr_Atr_Dfive
from FCT_Cr_1 import FCT_Cr_1
from FCT_Close_0_1 import FCT_Close_0_1
from FCT_Close_1_1 import FCT_Close_1_1
from FCT_Close_1_1_1 import FCT_Close_1_1_1
from FCT_Cci import FCT_Cci
# FCT_Camarilla_Vol_Dfive 没有查到如何计算这一因子
# FCT_BuySell_T 的计算似乎需要 buy_volume 和 sell_volume 两个字段

#sys.path.append('../')
from config import *
# 设置工作目录为当前脚本所在的目录
#os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
future=pd.read_csv('mindiff.csv')

class factor_calculator:
    def __init__(self, instruments, k_line_type, lengths):
        """
        初始化因子计算器
        :param instruments: 期货品种列表
        :param k_line_type: K线类型
        :param lengths:     滑动平均长度列表
        """
        self.instruments = instruments
        self.k_line_type = k_line_type
        self.lengths = lengths

        '''
        初始化所有因子计算器
        以字典的形式，将每个计算器与其名称进行对应，便于在程序中调用
        '''
        self.factors_dict = {
            "Tr":           Tr(),
            "FCT_Ac_Tr_1":  FCT_Ac_Tr_1(),
            "FCT_Ar_1":     FCT_Ar_1(),
            "FCT_Bias_1":   FCT_Bias_1(),
            "FCT_Br_1":     FCT_Br_1(),
            "FCT_Cmf_1":    FCT_Cmf_1(),  
            "Amihud": Amihud(),
            "Turnover": Turnover(),
            "FCT_Donchian_Vol_Dfive": FCT_Donchian_Vol_Dfive(),
            "FCT_Dmi_Adxr": FCT_Dmi_Adxr(),
            "FCT_Dmi_Adx": FCT_Dmi_Adx(),
            "FCT_Demark_Vol_Dfive": FCT_Demark_Vol_Dfive(),
            "FCT_Demark_Ref_1" : FCT_Demark_Ref_1(),
            "FCT_Demark_Atr_Dfive" : FCT_Demark_Atr_Dfive(),
            "FCT_Dbcd": FCT_Dbcd(),
            "FCT_Cr_Vol_Dfive": FCT_Cr_Vol_Dfive(),
            "FCT_Cr_Ref_1": FCT_Cr_Ref_1(),
            "FCT_Cr_Atr_Dfive": FCT_Cr_Atr_Dfive(),
            "FCT_Cr_1": FCT_Cr_1(),
            "FCT_Close_0_1": FCT_Close_0_1(),
            "FCT_Close_1_1": FCT_Close_1_1(),
            "FCT_Close_1_1_1": FCT_Close_1_1_1(),
            "FCT_Cci": FCT_Cci(),
        }

        self.require_length_factors = [
            "FCT_Ac_Tr_1", "FCT_Ar_1", "FCT_Bias_1", "FCT_Br_1", "FCT_Cmf_1", 
            "Amihud", "FCT_Dmi_Adxr", "FCT_Dmi_Adx", "FCT_Demark_Ref_1", 
            "FCT_Cci"
        ]

    def factors_cal(self):
        # 调用所有计算器，计算相应因子并保存到文件夹中
        # 首先遍历所有的期货种类
        for instrument in self.instruments:
            # 构建数据路径data_path
            data_path = f'./data/{self.k_line_type}/{instrument}/{instrument}.csv'
            if not os.path.exists(data_path):
                print(f"数据不存在:{data_path}")
                continue

            # 读取数据，并设置传入参数param
            mindiff = future[future['instrument']==instrument]['mindiff'].item()
            df = pd.read_csv(data_path)

            # 遍历因子字典，逐个计算因子
            for factor_name, calculator in self.factors_dict.items():
                try:
                    # 如果因子需要滑动长度，还需要遍历相应的长度列表
                    if factor_name in self.require_length_factors:
                        if os.path.exists(f'./data/{self.k_line_type}/{instrument}/Tr.csv'):
                            tr = pd.read_csv(f'./data/{self.k_line_type}/{instrument}/Tr.csv')
                            tr = tr['Tr']

                        for length in self.lengths:
                            param = {'df': df, 'mindiff': mindiff, 'length': length, 'tr': tr}

                            # 设置保存路径，保存数据并命名为{factor_name}@{length}.csv
                            save_path = f'./data/{self.k_line_type}/{instrument}/{factor_name}@{length}.csv'

                            # 计算每一个因子，调用calculator.formula并传入参数进行计算
                            result = calculator.formula(param)

                            # 利用os.makedirs设置一个路径，并利用to_csv保存结果
                            os.makedirs(os.path.dirname(save_path), exist_ok=True)
                            result.to_csv(save_path, index=False)

                            # 保存成功信息汇报
                            print(f"instrument:{instrument} factor:{factor_name}    length:{length} success:{save_path}")
                    else:
                        # Tr 因子不需要滑动长度，因此单独处理
                        # 设置保存路径，保存数据并命名为{factor_name}.csv
                        save_path = f"./data/{self.k_line_type}/{instrument}/{factor_name}.csv"

                        # 计算每一个因子
                        param = {'df': df}
                        result = calculator.formula(param)

                        # 利用os.makedirs设置一个路径，并利用to_csv保存结果
                        os.makedirs(os.path.dirname(save_path), exist_ok=True)
                        result.to_csv(save_path, index=False)

                        # 保存成功信息汇报
                        print(f"instrument:{instrument} factor:{factor_name}    success:{save_path}")
                except Exception as e:
                    # 当因子计算出错时报错
                    print(f"计算{factor_name}因子时出错：{e}")


# 主程序入口
if __name__ == "__main__":
    '''
    数据的初始化，在main.py里面也有相同的部分，便于使用者调整数据处理的范围
    instruments:    期货品种
    k_line_type:    k线类型
    lengths:        滑动平均长度
    '''
    instruments = instruments
    k_line_type = '5m'
    lengths = [5, 10, 20, 40, 80, 120, 180]

    # 创建因子计算器实例，以调用内部的函数
    calculator = factor_calculator(instruments, k_line_type, lengths)

    # 计算所有因子
    calculator.factors_cal()