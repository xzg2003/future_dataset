import pandas as pd
import csv
import os
import shutil
from bs4 import BeautifulSoup
from factor_judge.mutal_IC import mutal_IC
from factor_judge.layer_yield import layer_yield
from factor_judge.statistic import statistic

class run_factor_judge():
    def __init__(self, factor, method, k_line):
        self.statistic = statistic(factor, method, k_line)
        self.layer_yield = layer_yield(factor, k_line)
        self.factor = factor
        self.k_line = k_line
        pass
    
    # 输出完整报告
    def get_report(self):
        for k,v in (self.statistic.get_result()).items():
            self.statistic.results.setdefault(k, []).append(v)
  
        self.statistic.save_month_result()
        self.layer_yield.get_result()

    def to_html(self):
        # 设置图片文件夹路径
        folder_path = f'./result/{self.k_line}/{self.factor}'  
        html_output = f'./result/{self.k_line}/{self.factor}/{self.factor}_report.html'  # 生成的HTML文件名
        
        # 生成HTML内容
        html_content = """
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>PNG Image Gallery</title>
            <style>
                body {
                    font-family: Arial, sans-serif;
                    text-align: center;
                }
                .image-gallery {
                    display: flex;
                    flex-wrap: wrap;
                    justify-content: center;
                }
                .image-gallery img {
                    margin: 1%;
                    width: 80%;  /* 增大图片宽度 */
                    height: 80%; /* 增大图片高度 */
                    object-fit: contain;  /* 保持图片比例 */
                }
                .column2 {
                width:300px;
                }
            </style>
        </head>
        <body>"""
        html_content += f' <h1>{self.factor}因子报告</h1>\n'

        html_content += f' <h2>分层收益</h2>\n'
        html_content += f' <div class="image-gallery">\n'
        html_content += f'        <img src="{self.factor}_layer_yield.png" alt="分层收益">\n'
        html_content += f' </div>\n'

        df = pd.read_csv(f'{folder_path}/{self.factor}_layer_yield.csv',encoding='utf-8')
        # 将 DataFrame 转换为 HTML 表格
        html_table = df.to_html(index=False,justify='center')  # index=False 用来避免在表格中显示行索引
        html_content += f' <h2>分层收益表</h2>\n'
        html_content += html_table

        html_content += f' <h2>因子分布图</h2>\n'
        html_content += f' <div class="image-gallery" align=center>\n'
        html_content += f'        <img src="{self.factor}.png" alt="因子分布图">\n'
        html_content += f' </div>\n'

        df = pd.read_csv(f'{folder_path}/{self.factor}.csv',encoding='gbk')
        # 将 DataFrame 转换为 HTML 表格
        html_table = df.to_html(index=False,justify='center')  # index=False 用来避免在表格中显示行索引
        html_content += """
        <h2>因子统计数据报告</h2>"""
        html_content += html_table+'\n'
        html_content += """"
        </body>
        </html>
        """
        
        # 将生成的HTML内容写入到文件
        with open(html_output, 'w', encoding='utf-8') as f:
            f.write(html_content)

        with open(html_output, 'r', encoding='utf-8') as file:
            html_content = file.read()
        
        soup = BeautifulSoup(html_content, 'html.parser')

        tabel = soup.find('table')
        tabel['style'] = "table-layout: fixed;"
        tabel['width'] = '120%'

        tds = soup.find_all('td')
        for td in tds:
            test = td.get_text()
            td['style'] = "white-space:nowrap;overflow:hidden;text-overflow: ellipsis;"
            td['title'] = test
       
        with open(html_output, 'w', encoding='utf-8') as file:
            file.write(str(soup))
        
        print(f"\nHTML文件已生成：{html_output}")

if __name__=='__main__':
    factors = pd.read_csv('factor_name.csv',encoding='utf-8')

    
    for i in factors:

        a = run_factor_judge(i,'M','1d')
        a.get_report()
        a.to_html()
        print(f'{i} finished！')
    
    mutal_IC('1d').cal_mutal_IC()