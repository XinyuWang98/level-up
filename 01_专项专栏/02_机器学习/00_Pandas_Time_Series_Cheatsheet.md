# Pandas Time Series Cheatsheet

## 1. 差分 (Differencing) - `.diff()`

`.diff(periods=n)` 用于计算当前行与前 `n` 行的差值。

**公式**: $Y_t' = Y_t - Y_{t-n}$

**常用场景**: 
- 将非平稳序列（Non-Stationary）转化为平稳序列（Stationary），用于 ARIMA/XGBoost 等模型。
- 计算“日环比增量”、“周同比增量”。

**示例**:
```python
import pandas as pd

df = pd.DataFrame({'price': [100, 110, 105, 120]})

# 计算一阶差分 (今天 - 昨天)
df['diff_1'] = df['price'].diff(1) 
# [NaN, 10.0, -5.0, 15.0]

# 替代手动 Lag 相减
# 以前你可能这样做: df['price'] - df['price'].shift(1)
# 现在直接用 .diff(1) 更简洁、更高效
```

## 2. 滞后 (Lagging) - `.shift()`

`.shift(periods=n)` 将数据向下移动 `n` 行。

**常用场景**:
- 构造特征（Feature Engineering）：用昨天的数据预测今天。
- 防止数据泄露（Data Leakage）：计算 Rolling Mean 时先 shift。

**示例**:
```python
# 获取昨天的价格
df['lag_1'] = df['price'].shift(1)
# [NaN, 100.0, 110.0, 105.0]
```

## 3. 滚动统计 (Rolling Windows) - `.rolling()`

`.rolling(window=n)` 创建一个 n 行的滑动窗口，通常配合 `.mean()`, `.std()`, `.sum()` 使用。

**防泄露关键点**:
在预测 `t` 时刻时，必须使用 `t-1` 时刻的数据来计算 Rolling。
**正确写法**:
```python
# 先 shift(1) 拿到“昨天及以前的数据”，再 roll
df['roll_mean_7'] = df['price'].shift(1).rolling(window=7).mean()
```

**错误写法 (Data Leakage)**:
```python
# 这样会把“今天”包含进均值里，导致模型作弊
df['roll_mean_7'] = df['price'].rolling(window=7).mean()
```

## 4. 模型评估与可视化 (Evaluation & Visualization)

### 4.1 预测值 vs 真实值 (Predictions vs Actuals)
最为直观的评估方式，检查模型是否捕捉到了趋势和周期。

```python
import matplotlib.pyplot as plt

# 假设 test_df 包含 'date', 'quantity' (真实值), 'pred' (预测值)
plt.figure(figsize=(15, 6))
plt.plot(test_df['date'], test_df['quantity'], label='Actual', color='blue', alpha=0.6)
plt.plot(test_df['date'], test_df['pred'], label='Prediction', color='red', alpha=0.6, linestyle='--')
plt.title('Sales Forecast vs Actuals')
plt.legend()
plt.show()
```

### 4.2 特征重要度 (Feature Importance)
检查模型最依赖哪些特征，用于筛选特征或解释模型。

```python
import xgboost as xgb

# xgb_model 是训练好的 XGBoost 模型
fig, ax = plt.subplots(figsize=(10, 8))
xgb.plot_importance(xgb_model, ax=ax, height=0.5, max_num_features=20)
plt.title('XGBoost Feature Importance')
plt.show()
```

### 4.3 误差分析 (Error Analysis by Time)
检查模型在特定时间段（如周几、月份）的表现，找出"盲点"。

```python
import seaborn as sns

# 计算误差
test_df['error'] = test_df['pred'] - test_df['quantity']

fig, axes = plt.subplots(1, 2, figsize=(18, 5))

# DayOfWeek 误差分布
sns.boxplot(data=test_df, x='dayofweek', y='error', ax=axes[0])
axes[0].set_title('Error by Day of Week')
axes[0].axhline(0, color='r', linestyle='--')

# Month 误差分布
sns.boxplot(data=test_df, x='month', y='error', ax=axes[1])
axes[1].set_title('Error by Month')
axes[1].axhline(0, color='r', linestyle='--')

plt.show()
```
