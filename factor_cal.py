from factor_cal zhy import FCT_cmf_1, FCT_Br1, FCT_Ar_1, FCT_Ac_Tr_1, FCT_Bias_1, FCT_Tr_1
import pandas as pd
def factors_cal():
    instrument_list = ["RB2405.SHF", "I2405.DCE"]  
    k_line = "5m" 
    lengths = [10, 20, 40, 80, 120, 180] 

    factor_list = {
        "FCT_cmf_1": FCT_cmf_1(),
        "FCT_Br1": FCT_Br1(),
        "FCT_Ar_1": FCT_Ar_1(),
        "FCT_Ac_Tr_1": FCT_Ac_Tr_1(),
        "FCT_Bias_1": FCT_Bias_1(),
        "FCT_Tr_1": FCT_Tr_1()
    }

    for instrument in instrument_list:
        data_path = f"./data/{k_line}/{instrument}/{instrument}.csv"
        df = pd.read_csv(data_path)
        df["date"] = pd.to_datetime(df["date"])  

        for length in lengths:
            for factor_name, factor_class in factor_list.items():
                param = {
                    "df": df,
                    "k_line": k_line,
                    "instrument": instrument,
                    "length": length,
                }
                factor_class.formula(param)

if __name__ == "__main__":
    factors_cal()