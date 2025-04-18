import rqdatac
import pandas
import datetime
rqdatac.init('18720946768','20060402lyf')
# ricequant信息的初始化，保证后续能调用api接口

rqdatac.info()
# 显示用户信息

'''
# 以下是测试代码，用于查询某一个时间点的期货合约数据
date_0 = datetime.date(2015, 1, 1)
instruments_search = rqdatac.all_instruments(type='Future', market='cn', date=date_0)
print(instruments_search)

instruments_search.to_csv('instruments_classification.csv', index=False, encoding='utf-8')
print("数据成功保存")
'''

def factors_cal():
    instruments=['A'] #期货类型
    k_line_type = '5m'  # k线类型
    lengths = [10, 20, 40, 80, 120, 180] # 滑动平均长度

    tr_calculator = Tr()

    # 由于只有Tr的计算不包含length，这里进行单独处理
    for instrument in instruments:
        # 构建数据路径
        data_path = f'../data/{k_line_type}/{instrument}/{instrument}.csv'
        if not os.path.exists(data_path):
            print(f"数据文件不存在：{data_path}")
            continue

        # 读取数据
        df = pandas.read_csv(data_path)

        # 准备参数字典
        param = {'df': df}

        # 调用因子计算方法
        try:
            result = tr_calculator.formula(param)
        except Exception as e:
            print(f"计算因子时出错：{e}")
            continue

        # 构建保存路径
        save_path = f'../data/{k_line_type}/{instrument}/FCT_Tr.csv'
        os.makedirs(os.path.dirname(save_path), exist_ok=True)

        # 保存结果
        result.to_csv(save_path, index=False)
        print(f"因子计算结果已保存：{save_path}")



    # 一下是需要length的因子的计算
    for instrument in instruments:
        for length in lengths:
            # 构建数据路径
            data_path = f'../data/{k_line_type}/{instrument}/{instrument}.csv'
            if not os.path.exists(data_path):
                print(f"数据文件不存在：{data_path}")
                continue

            # 读取数据
            df = pandas.read_csv(data_path)

            # 准备参数字典
            param = {'df': df}

            # 调用因子计算方法
            try:
                result = tr_calculator.calculate_tr(param)
            except Exception as e:
                print(f"计算因子时出错：{e}")
                continue

            # 构建保存路径
            save_path = f'../data/{k_line_type}/{instrument}/FCT_Tr.csv'
            os.makedirs(os.path.dirname(save_path), exist_ok=True)

            # 保存结果
            result.to_csv(save_path, index=False)
            print(f"因子计算结果已保存：{save_path}")


if __name__ == "__main__":
    factors_cal()