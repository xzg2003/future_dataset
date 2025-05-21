from factor_judge.factor_judge import factor_judge
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import os
import pandas as pd
import numpy as np
from config import *
class layer_yield(factor_judge):
    def __init__(self, factor, k_line):
        super().__init__(factor, k_line)
    
    def quantile(self, df):
        split_percents = [0, 0.01, 0.03, 0.08, 0.15, 0.3, 0.5, 0.7, 0.85, 0.92, 0.97, 0.99, 1]
        factor_values = df[self.name].fillna(0).values
        factor_quantiles = np.unique(np.percentile(factor_values, [p * 100 for p in split_percents]))
        #print(f"分位数边界值: {factor_quantiles}")
        if len(factor_quantiles) <= 1:
            raise ValueError("分位数的边界值不足，无法进行分组。请检查输入数据。")

        df['quantile_layer'] = pd.cut(
            factor_values,
            bins=factor_quantiles,
            labels=range(len(factor_quantiles) - 1),
            include_lowest=True
        )

        df_list = []
        quantile_summary = []

        group_df = df.groupby(['quantile_layer'])
        for id, group in group_df:
            _df = group.sort_values('date').reset_index(drop=True)
            _df['cumulative_return'] = _df['rate'].cumsum()
            df_list.append(_df)

            total_profit = group['rate'].sum() * 10000  # 调整系数
            trade_count = group['rate'].count()
            avg_profit = total_profit / trade_count

            quantile_summary.append({
                'quantile_layer': id[0],
                'min': group[self.name].min(),
                'max': group[self.name].max(),
                'count': group[self.name].count(),
                'avg_profit': avg_profit
            })
            #print(_df)

        group_by_layer = pd.concat(df_list)
        summary_df = pd.DataFrame(quantile_summary)
        return group_by_layer, summary_df

    def draw_factor_backtest(self, factor_data, summary_df):
        fig, ax = plt.subplots(figsize=(16, 8))
        #plt.title(f"{factor_name} Backtest", fontproperties=zh_font)
        custom_colors = ['#FF9966', '#FFCCCC', '#CCCCFF', '#99CCCC', '#FF00FF', '#CCCCCC', 
                    '#FF6666', '#6699CC', '#FF6666', '#CC6600', '#99CCFF', '#99CC99']
        colors = {i: custom_colors[i] for i in range(12)}

        for idx, row in summary_df.iterrows():
            layer = row['quantile_layer'][0] if isinstance(row['quantile_layer'], tuple) else row['quantile_layer']
            layer_data = factor_data[factor_data['quantile_layer'] == layer]

            if not layer_data.empty:
                layer_data['date'] = pd.to_datetime(layer_data['date'])
                layer_label = (
                    f"Layer {layer} | "
                    f"Range: [{row['min']:.6f}, {row['max']:.6f}] | "
                    f"Count: {int(row['count'])} | "
                    f"Avg Profit(‱): {row['avg_profit']:.6f}"
                )
                ax.plot(
                    layer_data['date'],
                    layer_data['cumulative_return'],
                    label=layer_label,
                    color=colors[int(layer)]
                )
                plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
                plt.gca().xaxis.set_major_locator(mdates.MonthLocator(interval=10)) 
                plt.gcf().autofmt_xdate()

        ax.set_xlabel("Datetime")
        ax.set_ylabel("Cumulative Profit (%)")

        ax.grid(True)
        ax.legend(loc="upper left", fontsize=6)

        plt.tight_layout()
        plt.savefig(f'./result/{self.k_line}/{self.name}/{self.name}_layer_yield.png', dpi=300)
        plt.close()

    def get_result(self):
        df_combined=[]
        for i in instruments:
            if i in self.df.keys():
                df = self.df[i].copy()
                df['rate'] = df['yield'] - df['yield'].mean()
            else:
                continue
            df_combined.append(df)
        df_combined=pd.concat(df_combined,axis=0,ignore_index=True)
            
        group_by_layer, summary_df = self.quantile(df_combined)
        summary_df.to_csv(f'./result/{self.k_line}/{self.name}/{self.name}_layer_yield.csv', encoding="utf-8-sig",index=False)
        self.draw_factor_backtest(group_by_layer, summary_df)

#layer_yield('FCT_Ar_1@5', '1d').get_result()