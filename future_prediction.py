import os
import pandas as pd
import torch
import torch.nn as nn
from torch.utils.data import Dataset, DataLoader
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_squared_error
import numpy as np
from datetime import datetime

# 加载配置
from AI_config import factor_list, future_name

# 数据集类
class FuturesDataset(Dataset):
    def __init__(self, data, factor_list, target_col, sequence_length=100):
        self.data = data
        self.factor_list = factor_list
        self.target_col = target_col
        self.sequence_length = sequence_length

    def __len__(self):
        return len(self.data) - self.sequence_length

    def __getitem__(self, idx):
        # 获取因子和价格的近 100 天数据
        factors_and_prices = self.data.iloc[idx:idx + self.sequence_length][self.factor_list + [self.target_col]].values.T
        # 获取目标值（当天的 diff）
        y = self.data.iloc[idx + self.sequence_length][self.target_col]
        return torch.tensor(factors_and_prices, dtype=torch.float32), torch.tensor(y, dtype=torch.float32)

# 简单的深度学习模型
class FuturesModel(nn.Module):
    def __init__(self, input_channels, sequence_length):
        super(FuturesModel, self).__init__()
        input_dim = input_channels * sequence_length  # 输入维度为因子数量 * 序列长度
        self.net = nn.Sequential(
            nn.Linear(input_dim, 128),
            nn.ReLU(),
            nn.Linear(128, 64),
            nn.ReLU(),
            nn.Linear(64, 1)
        )

    def forward(self, x):
        # MLP 输入需要展平成 (batch_size, input_dim)
        x = x.view(x.size(0), -1)  # 展平输入
        return self.net(x)

# 加载数据
def load_data():
    # 加载期货价格数据
    price_path = f'./data/1d/{future_name}/{future_name}.csv'
    price_data = pd.read_csv(price_path, usecols=['date', 'close'])
    price_data['date'] = pd.to_datetime(price_data['date'])

    # 计算 diff 列（当日收盘价减去上一日收盘价）
    price_data['diff'] = price_data['close'].diff()
    price_data = price_data.dropna()  # 删除 NaN 行（首行没有上一日数据）

    # 加载因子数据
    factor_data = []
    for factor in factor_list:
        factor_path = f'./data/1d/{future_name}/{factor}.csv'
        factor_df = pd.read_csv(factor_path, usecols=['date', factor])
        factor_df['date'] = pd.to_datetime(factor_df['date'])
        factor_data.append(factor_df)

    # 合并因子数据和价格数据
    data = price_data
    for factor_df in factor_data:
        data = pd.merge(data, factor_df, on='date', how='inner')

    return data

# 数据预处理
def preprocess_data(data):
    # 检查数据是否存在 NaN 或 Inf，并进行处理
    data = data.replace([np.inf, -np.inf], np.nan).dropna()

    # 划分训练集和测试集
    train_data = data[(data['date'] >= '2014-01-01') & (data['date'] <= '2022-12-31')].drop(columns=['date'])
    test_data = data[(data['date'] >= '2023-01-01') & (data['date'] <= '2024-12-31')].drop(columns=['date'])

    # 标准化因子数据（不包括目标列 diff）
    # scaler = StandardScaler()
    # factor_columns = data.columns.difference(['date', 'close', 'diff'])  # 排除日期、收盘价和目标列
    # train_data[factor_columns] = scaler.fit_transform(train_data[factor_columns])
    # test_data[factor_columns] = scaler.transform(test_data[factor_columns])

    return train_data, test_data

# 训练模型
def train_model(model, train_loader, test_loader, criterion, optimizer, epochs=50):
    model.train()
    for epoch in range(epochs):
        train_loss = 0
        for features, target in train_loader:
            optimizer.zero_grad()

            # 检查输入是否存在 NaN 或 Inf
            if torch.isnan(features).any() or torch.isinf(features).any():
                print("发现无效输入值，跳过该批次")
                continue

            output = model(features)
            loss = criterion(output.squeeze(-1), target)  # 确保输出与目标值维度一致

            # 检查损失是否为 NaN
            if torch.isnan(loss) or torch.isinf(loss):
                print("发现无效损失值，跳过该批次")
                continue

            loss.backward()
            optimizer.step()
            train_loss += loss.item()

        # 计算测试集损失
        test_loss = evaluate_loss(model, test_loader, criterion)

        print(f"Epoch {epoch + 1}/{epochs}, Train Loss: {train_loss / len(train_loader):.4f}, Test Loss: {test_loss:.4f}")

# 计算测试集损失
def evaluate_loss(model, test_loader, criterion):
    model.eval()
    test_loss = 0
    with torch.no_grad():
        for features, target in test_loader:
            output = model(features)
            loss = criterion(output.squeeze(-1), target)
            test_loss += loss.item()
    return test_loss / len(test_loader)

# 测试模型
def test_model(model, test_loader):
    model.eval()
    predictions, targets = [], []
    with torch.no_grad():
        for features, target in test_loader:
            output = model(features)
            predictions.extend(output.squeeze(-1).tolist())  # 确保输出与目标值维度一致
            targets.extend(target.tolist())
    mse = mean_squared_error(targets, predictions)
    print(f"Test MSE: {mse:.4f}")
    return predictions, targets

def save_results(data, predictions, targets, sequence_length):
    # 获取测试集对应的日期
    test_dates = data[(data['date'] >= '2023-01-01') & (data['date'] <= '2024-12-31')]['date'].iloc[sequence_length:].reset_index(drop=True)
    
    # 创建结果 DataFrame
    results = pd.DataFrame({
        'date': test_dates,
        'predictions': predictions,
        'targets': targets
    })
    
    # 保存到 result.csv
    results.to_csv('./result.csv', index=False)
    print("结果已保存到 result.csv")

def main():
    # 加载数据
    data = load_data()

    # 数据预处理
    train_data, test_data = preprocess_data(data)

    # 创建数据集和数据加载器
    sequence_length = 100
    train_dataset = FuturesDataset(train_data, factor_list, target_col='diff', sequence_length=sequence_length)
    test_dataset = FuturesDataset(test_data, factor_list, target_col='diff', sequence_length=sequence_length)
    train_loader = DataLoader(train_dataset, batch_size=32, shuffle=True)
    test_loader = DataLoader(test_dataset, batch_size=32, shuffle=False)

    # 输出 train_dataset 的前 10 个 data 的内容
    for i in range(10):
        print(f"Train dataset item {i}:", train_dataset[i])


    # 初始化模型
    input_channels = len(factor_list) + 1  # 因子数量 + 价格
    model = FuturesModel(input_channels, sequence_length)
    criterion = nn.MSELoss()
    optimizer = torch.optim.Adam(model.parameters(), lr=0.001)

    # 检查模型参数是否初始化正确
    for name, param in model.named_parameters():
        if torch.isnan(param).any() or torch.isinf(param).any():
            print(f"模型参数 {name} 初始化无效")
            return

    # 训练模型
    train_model(model, train_loader, test_loader, criterion, optimizer, epochs=50)

    # 测试模型
    predictions, targets = test_model(model, test_loader)

    # 保存结果
    save_results(data, predictions, targets, sequence_length)

if __name__ == "__main__":
    main()
