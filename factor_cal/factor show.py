import FCT_Br_1, FCT_Ar_1, FCT_Ac_Tr_1, FCT_Bias_1, FCT_Tr_1, FCT_Cmf_1
import pandas as pd
import os

def factors_cal():
    instrument_list = ['A', 'AG', 'AL', 'AP', 'AU', 'BU', 'C', 'CF', 'CJ', 'CS', 'CU', 'EB', 'EG', 'FG', 'FU', 'HC', 
                       'I', 'IC', 'IF', 'IH', 'J', 'JD', 'JM', 'L', 'LU', 'LH', 'M', 'MA', 'NI', 'OI', 'P', 'PB', 'PF', 
                       'PG', 'PK', 'PP', 'RB', 'RM', 'RU', 'SA', 'SF', 'SM', 'SN', 'SP', 'SR', 'SC', 'SS', 'TA', 'T', 
                       'TF', 'UR', 'V', 'Y', 'ZN']  

    k_line = "5m"
    lengths = [10, 20, 40, 80, 120, 180]

    # 读取 mindiff.csv（你上传的文件）
    mindiff_df = pd.read_csv(".quantative/mindiff.csv")
    mindiff_dict = dict(zip(mindiff_df['instrument'], mindiff_df['mindiff']))

    # 启用的因子
    factor_list = {
        #"FCT_Cmf_1": FCT_Cmf_1.FCT_Cmf_1(),
        #"FCT_Br_1": FCT_Br_1.FCT_Br_1(),
        #"FCT_Ar_1": FCT_Ar_1.FCT_Ar_1(),
        #"FCT_Ac_Tr_1": FCT_Ac_Tr_1.FCT_Ac_Tr_1(),
        "FCT_Bias_1": FCT_Bias_1.FCT_Bias_1(),
        #"FCT_Tr_1": FCT_Tr_1.FCT_Tr_1()
    }

    for instrument in instrument_list:
        data_path = f".quantative/data/{k_line}/{instrument}/{instrument}.csv"

        if not os.path.exists(data_path):
            print(f"Warning: Data file for {instrument} not found at {data_path}")
            continue

        if instrument not in mindiff_dict:
            print(f"Warning: mindiff not found for {instrument} in mindiff file.")
            continue

        try:
            df = pd.read_csv(data_path)
            df.rename(columns={'volume': 'vol', 'datetime': 'date'}, inplace=True)

            if 'vol' not in df.columns or 'date' not in df.columns:
                print(f"Error: Required columns missing in {data_path}")
                continue
            
            df["date"] = pd.to_datetime(df["date"])
            mindiff_value = float(mindiff_dict[instrument])

            for length in lengths:
                for factor_name, factor_class in factor_list.items():
                    param = {
                        "df": df,
                        "k_line": k_line,
                        "instrument": instrument,
                        "length": length,
                        "mindiff": mindiff_value
                    }
                    factor_class.formula(param)

        except Exception as e:
            print(f"Error processing {instrument}: {e}")

if __name__ == "__main__":
    factors_cal()

