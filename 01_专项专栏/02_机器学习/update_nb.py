import nbformat
import os

nb_path = './01_专项专栏/02_机器学习/09_Project2B_Retail_Sales_Forecasting.ipynb'

# Read the notebook
if not os.path.exists(nb_path):
    print(f"Error: Notebook not found at {nb_path}")
    exit(1)

with open(nb_path, 'r', encoding='utf-8') as f:
    nb = nbformat.read(f, as_version=4)

# Define new cells to append
cells_to_add = []

# Cell 1: Feature Engineering (Anti-Leakage)
source_1 = r"""
# ==========================================
# 5. XGBoost 建模: Diff 预测 + 递归预测 (Recursive Forecasting)
# ==========================================
import xgboost as xgb
from sklearn.metrics import mean_squared_error, mean_absolute_error
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# 5.1 特征工程 (防泄露重构)
# 为了确保没有数据穿越，我们重新计算用于模型的 Rolling/Lag 特征
# 核心原则：预测 Day T 时，只能看到 Day T-1 及以前的数据

print("正在构建 XGBoost 专属特征集...")
df_xgb = day_summary.copy()

# 基础时间特征
df_xgb['month'] = df_xgb['date'].dt.month
df_xgb['year'] = df_xgb['date'].dt.year
# df_xgb['week'] 已经在前面计算过

# 目标变量: Diff (一阶差分)
df_xgb['target_diff'] = df_xgb['quantity'].diff(1)

# === 关键：构造 Shift 后的特征 ===
# Shift(1) 代表“昨天”的数据。所有的 Rolling 必须基于 Shift(1) 进行，否则就会包含“今天”的销量（即泄露）

# 1. 简单滞后
df_xgb['qty_lag1'] = df_xgb['quantity'].shift(1)
df_xgb['qty_lag7'] = df_xgb['quantity'].shift(7) # 这里的 shift(7) 其实是 shift(1) 再 lag 6，或者直接取7天前

# 2. 滚动特征 (基于昨天及以前的数据)
# Close_Shift1 代表昨天及以前的序列
qty_shift1 = df_xgb['quantity'].shift(1)

df_xgb['qty_roll7_mean'] = qty_shift1.rolling(window=7).mean()
df_xgb['qty_roll7_std']  = qty_shift1.rolling(window=7).std()
df_xgb['qty_roll30_mean'] = qty_shift1.rolling(window=30).mean()

# 3. 辅助变量 (为了简单起见，这里主要用 Quantity 特征，如果需要 GMV/Order 也可以同理构造)

# 清洗数据 (去除因 Lag/Diff 产生的 NaN)
df_model = df_xgb.dropna().reset_index(drop=True)

# 特征列表
feature_cols = [
    'dayofweek', 'month', 'year',
    'qty_lag1', 'qty_lag7',
    'qty_roll7_mean', 'qty_roll7_std', 'qty_roll30_mean'
]
target_col = 'target_diff'

print(f"特征工程完成。有效样本数: {len(df_model)}")
print(f"使用特征: {feature_cols}")
"""

# Cell 2: Train/Test Split & Training
source_2 = r"""
# 5.2 数据切分与模型训练
# 时间序列切分：最后 30 天作为测试集 (Out-of-Time Validation)

test_days = 30
train_df = df_model.iloc[:-test_days].copy()
test_df = df_model.iloc[-test_days:].copy()

X_train = train_df[feature_cols]
y_train = train_df[target_col]
X_test = test_df[feature_cols]
y_test = test_df[target_col]

print(f"Train Set: {X_train.shape}, Test Set: {X_test.shape}")

# 训练 XGBoost
model_xgb = xgb.XGBRegressor(
    n_estimators=1000,
    learning_rate=0.05,
    max_depth=5,
    subsample=0.8,
    colsample_bytree=0.8,
    objective='reg:squarederror',
    n_jobs=-1,
    random_state=42
)

model_xgb.fit(
    X_train, y_train,
    eval_set=[(X_train, y_train), (X_test, y_test)],
    early_stopping_rounds=50,
    verbose=100
)

# 特征重要性
xgb.plot_importance(model_xgb, max_num_features=10)
plt.title("XGBoost Feature Importance")
plt.show()
"""

# Cell 3: Recursive Forecast Logic
source_3 = r"""
# 5.3 递归预测 (Recursive Forecasting)实现
# 这里的难点是：每预测出一天，都要把它作为“历史”来重新计算下一天的特征

def recursive_forecast(model, train_data_tail, steps=30):
    '''
    model: 训练好的 XGBoost 模型
    train_data_tail: 训练集最后一段数据 (用于初始化 Lag/Roll 特征)
    steps: 预测步数
    '''
    # 初始化：我们需要保留足够长的历史数据来计算 rolling(30)
    # 所以我们取训练集最后 40 天的数据作为 buffer
    history_df = train_data_tail.iloc[-60:].copy().reset_index(drop=True)
    
    forecast_results = []
    
    last_known_date = history_df['date'].iloc[-1]
    last_known_abs_qty = history_df['quantity'].iloc[-1] # 昨天的真实销量
    
    current_abs_qty = last_known_abs_qty # 用于累加 Diff
    
    print(f"开始递归预测 {steps} 天...")
    
    for i in range(steps):
        # 1. 确定当前预测的日期
        curr_date = last_known_date + pd.Timedelta(days=i+1)
        
        # 2. 构造当前日期的特征 (Feature Calculation)
        # 注意：这里必须严格按照 5.1 的逻辑复现特征
        
        # 构造一个临时行，用于计算 features
        # 关键：Lag 和 Roll 都是基于 history_df 的数据
        
        qty_series = history_df['quantity'] # 包含 真实历史 + 已预测的值
        
        # 计算特征 (仅针对当前这一天)
        feat_dict = {}
        feat_dict['dayofweek'] = curr_date.dayofweek
        feat_dict['month'] = curr_date.month
        feat_dict['year'] = curr_date.year
        
        # Lag 1: 昨天的销量 (也就是 history_df 的最后一个值)
        feat_dict['qty_lag1'] = qty_series.iloc[-1]
        
        # Lag 7: 7天前的销量
        feat_dict['qty_lag7'] = qty_series.iloc[-7] 
        
        # Roll 7 Mean: 过去7天(包含昨天)的均值
        feat_dict['qty_roll7_mean'] = qty_series.iloc[-7:].mean()
        
        # Roll 7 Std
        feat_dict['qty_roll7_std'] = qty_series.iloc[-7:].std()
        
        # Roll 30 Mean
        feat_dict['qty_roll30_mean'] = qty_series.iloc[-30:].mean()
        
        # 3. 转换为 DataFrame 输入模型
        X_curr = pd.DataFrame([feat_dict])[feature_cols]
        
        # 4. 预测 Diff
        pred_diff = model.predict(X_curr)[0]
        
        # 5. 还原 Absolute Quantity
        # 新的销量 = 昨天销量 + 预测的变化量
        pred_abs = feat_dict['qty_lag1'] + pred_diff 
        
        # 业务逻辑修正：销量不能为负
        if pred_abs < 0: 
            pred_abs = 0
            
        # 6. 将新预测结果 Append 到 history_df，用于下一次迭代
        new_row = {'date': curr_date, 'quantity': pred_abs}
        # 仅由于我们需要 quantity 来算 lag，其他列为了保持格式可以填 NaN
        history_df = pd.concat([history_df, pd.DataFrame([new_row])], ignore_index=True)
        
        # 7. 记录结果
        forecast_results.append({
            'date': curr_date,
            'pred_diff': pred_diff,
            'pred_quantity': pred_abs
        })
        
    return pd.DataFrame(forecast_results)

# 执行预测
forecast_df = recursive_forecast(model_xgb, train_df, steps=test_days)
print("递归预测完成。前5天结果：")
print(forecast_df.head())
"""

# Cell 4: Evaluation & Visualization
source_4 = r"""
# 5.4 结果评估与对比
# 将预测结果与 Test 集真实值对比

# 合并对比
comparison_df = pd.merge(test_df[['date', 'quantity']], forecast_df[['date', 'pred_quantity']], on='date', how='inner')
comparison_df.rename(columns={'quantity': 'Actual', 'pred_quantity': 'Forecast'}, inplace=True)

# 计算 Metrics
mae = mean_absolute_error(comparison_df['Actual'], comparison_df['Forecast'])
rmse = np.sqrt(mean_squared_error(comparison_df['Actual'], comparison_df['Forecast']))
mape = np.mean(np.abs((comparison_df['Actual'] - comparison_df['Forecast']) / comparison_df['Actual'])) * 100

print(f"XGBoost Recursive Forecast Loop Metrics:")
print(f"MAE: {mae:.2f}")
print(f"RMSE: {rmse:.2f}")
print(f"MAPE: {mape:.2f}%")

# 可视化
plt.figure(figsize=(18, 6))

# 画出部分训练集历史 (连接处)
history_plot = train_df.iloc[-60:]
plt.plot(history_plot['date'], history_plot['quantity'], label='Training Data (Last 60 days)', color='gray', alpha=0.5)

# 画出真实值
plt.plot(comparison_df['date'], comparison_df['Actual'], label='Actual Sales', color='green', linewidth=2)

# 画出预测值
plt.plot(comparison_df['date'], comparison_df['Forecast'], label='XGBoost Recursive Forecast', color='red', linestyle='--', marker='o')

plt.title(f'XGBoost Recursive Forecasting (Diff Strategy)\nMAE: {mae:.2f}, RMSE: {rmse:.2f}')
plt.xlabel('Date')
plt.ylabel('Quantity')
plt.legend()
plt.grid(True, alpha=0.3)
plt.show()
"""

# Add cells
cells_to_add.append(nbformat.v4.new_code_cell(source_1))
cells_to_add.append(nbformat.v4.new_code_cell(source_2))
cells_to_add.append(nbformat.v4.new_code_cell(source_3))
cells_to_add.append(nbformat.v4.new_code_cell(source_4))

nb.cells.extend(cells_to_add)

# Save
with open(nb_path, 'w', encoding='utf-8') as f:
    nbformat.write(nb, f)

print(f"Successfully appended {len(cells_to_add)} cells to {nb_path}")
