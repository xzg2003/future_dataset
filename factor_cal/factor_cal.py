import os       # 与路径操作相关的包，用于管理文件
import pandas
from .FCT_Ac_Tr_1   import      FCT_Ac_Tr_1
from .FCT_Ar_1      import      FCT_Ar_1
from .FCT_Bias_1    import      FCT_Bias_1
from .FCT_Br_1      import      FCT_Br_1
from .FCT_Cmf_1     import      FCT_Cmf_1
from .Tr            import      Tr

# 设置工作目录为当前脚本所在的目录
os.chdir(os.path.dirname(os.path.abspath(__file__)))

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
            "FCT_Ac_Tr_1":  FCT_Ac_Tr_1(),
            "FCT_Ar_1":     FCT_Ar_1(),
            "FCT_Bias_1":   FCT_Bias_1(),
            "FCT_Br_1":     FCT_Br_1(),
            "FCT_Cmf_1":    FCT_Cmf_1(),
            "Tr":           Tr(),
        }


    def factors_cal(self):
        # 调用所有计算器，计算相应因子并保存到文件夹中
        # 首先遍历所有的期货种类
        for instrument in self.instruments:
            # 构建数据路径data_path
            data_path = f'../data/{self.k_line_type}/{instrument}/{instrument}.csv'
            if not os.path.exists(data_path):
                print(f"数据不存在:{data_path}")
                continue

            # 读取数据，并设置传入参数param
            df = pandas.read_csv(data_path)
            param = {'df': df}

            # 遍历因子字典，逐个计算因子
            for factor_name, calculator in self.factors_dict.items():
                try:
                    # 如果因子需要滑动长度，还需要遍历相应的长度列表
                    if factor_name != "Tr":
                        for length in self.lengths:
                            # 设置保存路径，保存数据并命名为{factor_name}@{length}.csv
                            save_path = f'../data/{self.k_line_type}/{instrument}/{factor_name}@{length}.csv'

                            # 计算每一个因子，调用calculator.formula并传入参数进行计算
                            result = calculator.formula(param, length)

                            # 利用os.makedirs设置一个路径，并利用to_csv保存结果
                            os.makedirs(os.path.dirname(save_path), exist_ok=True)
                            result.to_csv(save_path, index=False)

                            # 保存成功信息汇报
                            print(f"instrument:{instrument} factor:{factor_name}    length:{length} success:{save_path}")
                    else:
                        # Tr 因子不需要滑动长度，因此单独处理
                        # 设置保存路径，保存数据并命名为{factor_name}.csv
                        save_path = f"../data/{self.k_line_type}/{instrument}/{factor_name}.csv"

                        # 计算每一个因子
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
    instruments = ['A']
    k_line_type = '5m'
    lengths = [10, 20, 40, 80, 120, 180]

    # 创建因子计算器实例，以调用内部的函数
    calculator = factor_calculator(instruments, k_line_type, lengths)

    # 计算所有因子
    calculator.factors_cal()