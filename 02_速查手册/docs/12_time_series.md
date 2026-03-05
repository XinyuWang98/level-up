# 📈 时序预测 (Time Series)
*预测未来：从横截面 (Cross-sectional) 跨越到 时间序列 (Time Series)。*

## 选型指南 (Model Selection)

| 模型 (Model)  | 适用场景       | 核心特点                                                             |
| :------------ | :------------- | :------------------------------------------------------------------- |
| **ARIMA**     | 学术/金融      | **白盒**。纯数学 (自回归+移动平均)，极其依赖数据平稳性。             |
| **Prophet** 👑 | **商业/销量**  | **灰盒**。Facebook开源，傻瓜式处理节假日/突变点，适合 90% 业务场景。 |
| **LSTM**      | 极其复杂的波动 | **黑盒**。深度学习 (RNN)，需要海量数据。                             |
| **XGBoost** 🚀 | **定制化业务** | **白盒**。通过构造特征把时序问题变成监督学习。适合强业务逻辑！       |

## 基础知识备忘 (Basics Cheat Sheet)

### 📅 Pandas Day of Week Mapping
在 `dt.dayofweek` 中，整数与星期的对应关系如下：

| 整数 (Integer) | 星期 (Day)             |
| :------------- | :--------------------- |
| **0**          | **Monday (星期一)**    |
| **1**          | **Tuesday (星期二)**   |
| **2**          | **Wednesday (星期三)** |
| **3**          | **Thursday (星期四)**  |
| **4**          | **Friday (星期五)**    |
| **5**          | **Saturday (星期六)**  |
| **6**          | **Sunday (星期日)**    |

!!! tip "避免魔法数字"

    在代码开头定义常量：

    ```python
    DAY_MON = 0
    DAY_FRI = 4
    DAY_SUN = 6
    ```

---

## 🔮 通用预测 SOP (Forecasting Pipeline)
> *从 0 到 1 构建预测模型的核心 6 步。下方每个步骤都有对应的「代码锦囊」。*

| 步骤       | 名称               | 核心动作                            | 代码锦囊    |
| :--------- | :----------------- | :---------------------------------- | :---------- |
| **Step 1** | 🎯 明确目标         | Target / Granularity / Horizon      | —           |
| **Step 2** | 📊 EDA & 平稳性检验 | 画图 → ADF → 季节性分解             | §2.1 ~ §2.3 |
| **Step 3** | 🔧 差分决策         | period vs order → 差分策略选择      | §3.1 ~ §3.3 |
| **Step 4** | 🛠️ 特征工程         | Lag / Rolling / Date Attributes     | §4.1 ~ §4.2 |
| **Step 5** | ✂️ 数据集拆分       | Time Series Split (绝不能 Shuffle!) | §5.1        |
| **Step 6** | 🤖 建模             | Prophet Baseline → XGBoost Champion | §6.1 ~ §6.2 |
| **Step 7** | 📉 评估与回测       | 分层评估 → 可视化 → 误差分析        | §7.1 ~ §7.5 |

---

## Step 1: 🎯 明确预测目标 (Goal Definition)

*   **Target**: 预测什么？(Quantity / GMV / Traffic)
*   **Granularity**: 粒度？(By Day / By Week)
*   **Horizon**: 预测多久？(未来 7 天 / 30 天)

---

## Step 2: 📊 EDA & 平稳性检验

### 2.1 ADF 平稳性检验 (Stationarity Test)

> **Why?** 差分不是拍脑袋决定的。必须先用 ADF 检验科学判断序列是否平稳，再决定是否差分。

??? example "ADF 平稳性检验代码模板"

    ```python
    from statsmodels.tsa.stattools import adfuller

    def adf_test(series, name=''):
        """​ADF 平稳性检验 - 科学判断是否需要差分"""
        result = adfuller(series.dropna(), autolag='AIC')
        p_value = result[1]

        print(f'=== ADF 检验: {name} ===')
        print(f'  ADF Statistic : {result[0]:.4f}')
        print(f'  p-value       : {p_value:.4f}')
        print(f'  临界值 (5%)   : {result[4]["5%"]:.4f}')
        print(f'  结论: {"✅ 平稳" if p_value < 0.05 else "❌ 非平稳 (需差分)"}')
        return p_value

    # 使用: 逐步检验，从原始序列开始
    p0 = adf_test(df['quantity'], '原始序列')
    if p0 >= 0.05:
        p1 = adf_test(df['quantity'].diff(1), 'diff(period=1)')
    ```

### 2.2 季节性分解 (Seasonal Decompose) SOP 🍂

> **Why?** 用统计学方法验证 EDA 观察到的周期性，避免被整体趋势误导。验证 "周三低谷" 是否是真实的周期信号。

#### ✅ 核心决策表 (Decision Matrix)

| 场景                        | 模型选择 (`model`)        | 频率设置 (`freq`)  | 周期 (`period`) |
| :-------------------------- | :------------------------ | :----------------- | :-------------- |
| **波动稳定** (如 Walmart)   | `'additive'` (加法)       | `W-FRI` (周五数据) | `52` (年周期)   |
| **波动随趋势放大** (如 GDP) | `'multiplicative'` (乘法) | `M` (月数据)       | `12` (年周期)   |
| **日数据查周规律**          | `'additive'`              | `D` (日数据)       | `7` (周周期)    |

!!! warning "频率陷阱 (Frequency Trap)"

    **千万别用 `asfreq('D')` 处理周数据！**
    
    - ❌ `asfreq('D')`: 会产生 6/7 的 `NaN` 或 `0`，严重干扰分解。
    - ✅ `asfreq('W-FRI')`: 保持每周一个点，无空值。

#### 🐍 实战代码模板

??? example "🐍 季节性分解代码模板"

    ```python
    from statsmodels.tsa.seasonal import seasonal_decompose
    import matplotlib.pyplot as plt

    # 1. 准备数据 (这是最容易错的一步!)
    # 确保索引是 DatetimeIndex，且设置正确的频率
    # ❌ df.asfreq('D') → 会产生大量空值
    # ✅ df.asfreq('W-FRI') → 保持周频 (Walmart 示例)
    ts_data = df.set_index('date')['weekly_sales'].asfreq('W-FRI').fillna(0)

    # 2. 执行分解
    # model='additive': 波动幅度不随趋势变化 (y = Trend + Seasonality + Residual)
    # period=52: 周数据看年周期 (1年=52周)
    decomposition = seasonal_decompose(ts_data, model='additive', period=52)

    # 3. 可视化
    fig = decomposition.plot()
    fig.set_size_inches(14, 8) 
    plt.show()

    # 4. 提取分量 (用于后续特征工程)
    trend = decomposition.trend
    seasonal = decomposition.seasonal
    residual = decomposition.resid
    ```

### 2.3 动态旺季定义 (Dynamic Seasonality)

> **Why?** 硬编码 (如 `[9, 10, 11, 12]` 是旺季) 容易过时。用数据驱动的方法自动识别旺季，适应性更强。

```python
# 1. 计算每个月的平均销量（防止泄露，最好只用训练集）
monthly_sales = train_df.groupby(train_df['order_date'].dt.month)['sales'].mean()

# 2. 动态定义门槛 (Threshold): 取 75% 分位数
threshold = monthly_sales.quantile(0.75)

# 3. 自动获取旺季月份
dynamic_peak_months = monthly_sales[monthly_sales > threshold].index.tolist()
print(f"📈 自动识别出的旺季月份: {dynamic_peak_months}")

# 4. 构造特征
df['is_peak_season'] = df['month'].isin(dynamic_peak_months).astype(int)
```

---

## Step 3: 🔧 差分决策 (Differencing)

### 3.1 period vs order 辨析

!!! important "这是最容易混淆的概念"

    `diff(period=7)` **不是** 7 阶差分！`period` 和 `order` 是两个完全不同的维度：

    | 参数              | 含义                       | 举例                               | 消除什么           |
    | ----------------- | -------------------------- | ---------------------------------- | ------------------ |
    | **period** (步长) | 差分的滞后间隔，和谁做减法 | `diff(period=7)` = $y_t - y_{t-7}$ | **季节性** (周/年) |
    | **order** (次数)  | 重复差分几次               | `diff(1).diff(1)` = 二阶差分       | **更强的趋势**     |

    **常见组合**：

    - `diff(1)` -- 去趋势 (最常用)
    - `diff(7)` -- 去周季节性 (日数据)
    - `diff(1).diff(7)` -- 先去趋势，再去周季节性 (组合差分)
    - `diff(12)` -- 去年季节性 (月数据)

### 3.2 差分科学决策框架

**核心原则：先诊断，再用药**。差分不是万能药，必须通过统计检验决策。

**决策流程**：

1. **ADF 检验**：判断序列是否平稳 → 不平稳才需要差分
2. **ACF 图分析**：确定 `period` 应该用多少
    - ACF 缓慢衰减 → 有趋势 → `diff(period=1)`
    - ACF 在 lag=7,14,21 有尖峰 → 周季节性 → `diff(period=7)`
3. **差分后再检验**：ADF 确认平稳
4. **方差监控**：差分后方差暴增 = 过度差分

!!! warning "过度差分的判断"

    以下信号表明你差分过头了：

    - 差分后方差比原序列还大 (variance_diff > variance_original)
    - ACF 图 lag=1 处出现大的负自相关（接近 -0.5）
    - 差分后序列剧烈震荡

    **经验法则**：一般不超过 2 阶差分，季节差分 1 次足够。

### 3.3 XGBoost 差分三策略对比

| 策略             | 做法                                   | 优点               | 缺点             | 推荐场景         |
| :--------------- | :------------------------------------- | :----------------- | :--------------- | :--------------- |
| **直接预测原值** | `y = quantity`                         | 简单，无需还原     | 不能外推，极值差 | 弱趋势/平稳序列  |
| **预测差分值**   | `y = diff(1)`，再还原                  | 解决外推           | 还原时误差累积   | 强趋势/单步预测  |
| **差分作为特征** | `X` 含 `diff_1/diff_7`，`y = quantity` | 两全其美，无需还原 | 需更多特征工程   | **推荐默认方案** |

!!! tip "差分作为特征 (推荐做法)"

    把 `diff` 值当成输入特征而非预测目标。模型仍然直接预测 `quantity`，但多了趋势方向信号：

    ```python
    # ⚠️ 必须先 shift(1) 再 diff，否则 diff(n) 包含当前 y_t → Data Leakage!
    # ❌ df['quantity'].diff(1) = y_t - y_{t-1} → 包含 y_t
    # ✅ df['quantity'].shift(1).diff(1) = y_{t-1} - y_{t-2} → 纯历史数据
    df['diff_1'] = df['quantity'].shift(1).diff(1).fillna(0)  # 趋势信号
    df['diff_7'] = df['quantity'].shift(1).diff(7).fillna(0)  # 周季节信号

    X = df[['lag_1', 'lag_7', 'roll_mean_7', 'dayofweek',
            'diff_1', 'diff_7']]  # diff 只是特征之一
    y = df['quantity']  # 目标还是原始值！无需还原
    ```

---

## Step 4: 🛠️ 特征工程 (Feature Engineering)

### 4.1 填补缺失日期 (Data Continuity)

> **Why?** 时序模型假设时间连续。如果中间断了一天，`shift(1)` 就会错位。零售数据经常有这种情况（如周日不开门）。

```python
# 方法1: Reindex (简洁)
full_range = pd.date_range(start='2020-01-01', end='2020-12-31', freq='D')
df = df.set_index('date').reindex(full_range, fill_value=0).reset_index()

# 方法2: Left Join (直观)
full_df = pd.DataFrame({'date': full_range})
df = pd.merge(full_df, df, on='date', how='left').fillna(0)
```

### 4.2 批量特征构造 (Scalable Feature Engineering)

> **Why?** 手动写 `lag_1`, `lag_2`... 太累且易错。用 **Loop + f-string** 自动生成。

```python
targets = ['quantity', 'gmv', 'order_cnt'] # 目标列

for col in targets:
    # Lag Features (滞后): 抓趋势
    df[f'{col}_lag1'] = df[col].shift(1).fillna(0)
    df[f'{col}_lag7'] = df[col].shift(7).fillna(0) # 周环比
    
    # Rolling Features (滑窗): 平滑噪音 (必须先 shift 再 rolling!)
    df[f'{col}_roll7'] = df[col].shift(1).rolling(7).mean().fillna(0)
    
    # Diff Features (增量): 必须先 shift(1) 再 diff，避免 Data Leakage!
    df[f'{col}_diff1'] = df[col].shift(1).diff(1).fillna(0)
    df[f'{col}_diff7'] = df[col].shift(1).diff(7).fillna(0)  # 周季节信号
```

### 4.3 进阶: Granger 特征筛选 (Granger Selection)

> **Why?** 传统Correlation只看"同期相关性" (今天下雨 vs 今天卖伞)，但预测模型需要"跨期相关性" (昨天下雨 vs 今天卖感冒药)。**Granger Causality 是筛选 Lag 特征的黄金标准。**

**SOP:**
1.  **确定最大滞后期**: 业务直觉 (如 `maxlag=7` 天)。
2.  **批量检验**: 对备选特征 X 做 Granger Test。
3.  **筛选 P < 0.05**:
    *   **P < 0.05**: 说明 X 的过去值对预测 Y 有帮助 → **保留该特征**。
    *   **P > 0.05**: 说明 X 对 Y 无预测能力 → **剔除** (降噪)。

```python
from statsmodels.tsa.stattools import grangercausalitytests

# 筛选: 只有 P<0.05 的特征才放入模型
def granger_select(data, target, feature, maxlag=3):
    test_result = grangercausalitytests(data[[target, feature]], maxlag=maxlag, verbose=False)
    p_values = [round(test_result[i+1][0]['ssr_ftest'][1], 4) for i in range(maxlag)]
    min_p_value = np.min(p_values)
    return min_p_value < 0.05  # 如果最小P值小于0.05，说明至少有一个Lag是显著的

# 实战: 循环筛选所有 Candidate Features
selected_features = []
for col in candidate_cols:
    if granger_select(df, 'sales', col):
        selected_features.append(col)
        print(f"✅ 保留特征: {col} (Granger Cause)")
    else:
        print(f"❌ 剔除特征: {col} (无预测力)")
```

!!! warning "diff() Data Leakage 陷阱"

    `diff(n)` 的计算公式是 `y_t - y_{t-n}`，**包含当前行 `y_t` 本身**！

    如果 `y_t` 就是你的预测目标 (target)，那 `diff(n)` 作为特征就是在「偷看答案」：

    ```python
    # ❌ Data Leakage: diff(1) = y_t - y_{t-1}，包含 y_t
    df[col].diff(1)
    # ❌ Data Leakage: diff(4) = y_t - y_{t-4}，同样包含 y_t
    df[col].diff(4)

    # ✅ 安全: 先退一步 shift(1)，再做 diff
    df[col].shift(1).diff(1)  # = y_{t-1} - y_{t-2}，纯历史数据
    df[col].shift(1).diff(4)  # = y_{t-1} - y_{t-5}，纯历史数据
    ```

!!! warning "Per-Store 特征构造: 必须用 transform"

    多门店/多分组数据做 Lag/Rolling 时，**必须用 `groupby + transform`**，否则会跨组污染：

    ```python
    # ❌ 跨店污染: groupby 后 shift/rolling 会丢失分组边界
    df.groupby('store')[col].shift(1).rolling(4).mean()

    # ✅ Per-Store: transform 保持每个 store 独立计算
    df.groupby('store')[col].transform(
        lambda x: x.shift(1).rolling(4).mean()
    )
    ```

!!! warning "XGBoost 不接受日期类型 (Datetime)"

    XGBoost / LightGBM 等树模型**只接受数值型特征**，不能直接使用 `datetime64` 列。

    **正确做法**：Feature Engineering 就是把日期"翻译"成数字。翻译完了，原列就不需要了：

    ```python
    # ✅ 日期信息已被拆解为数值特征
    # year, month, dayofweek, is_weekend, is_peak_month ...

    # 训练前丢掉原始日期列
    feature_cols = [c for c in X_train.columns if c != 'order_date']
    xgb_X_train = X_train[feature_cols]
    xgb_X_test  = X_test[feature_cols]
    ```

    **注意**：Prophet 恰恰相反，它**只需要**日期列 (`ds`) + 目标值 (`y`)，不需要手工特征。

---

## Step 5: ✂️ 数据集拆分 (Train-Test Split)

> **深度好文**: 关于 **[单条时序 vs 多条时序](06b_data_splitting.md)** 的详细拆分策略 (含交叉验证代码)，请移步 **[✂️ 06b_data_splitting](06b_data_splitting.md)**。

### 5.1 动态 Cutoff 切分 (最常用)

适用于 Walmart 这种 **多门店 × 多时间** 的数据。

```python
# ✅ 动态计算切分点: 取后 20% 的时间做测试集
TEST_RATIO = 0.2
unique_dates = sorted(df['date'].unique())
cutoff_date = unique_dates[int(len(unique_dates) * (1 - TEST_RATIO))]

# 按日期统一一刀切
train_mask = df['date'] <= cutoff_date
test_mask  = df['date'] > cutoff_date

X_train, X_test = X[train_mask], X[test_mask]
y_train, y_test = y[train_mask], y[test_mask]

print(f"切分点: {cutoff_date} | Train: {train_mask.sum()} | Test: {test_mask.sum()}")
```

!!! warning "严禁随机 Shuffle"
    时序数据必须保证 **训练集时间 < 测试集时间**，否则就是 Data Leakage。
    ❌ `train_test_split(random_state=42)` 是绝对禁止的。

---

## Step 6: 🤖 建模 (Modeling)

### 6.1 Prophet Baseline (傻瓜式起手)

??? example "Prophet Baseline 代码模板"

    ```python
    from prophet import Prophet

    # 1. 数据准备 (强迫症格式: ds=时间, y=数值)
    df = df.rename(columns={'Date': 'ds', 'Sales': 'y'})

    # 2. 实例化 & 训练
    model = Prophet(daily_seasonality=True, yearly_seasonality=True)
    model.add_country_holidays(country_name='CN') # 💡 神技: 自动把中国节假日加进去!
    model.fit(df)

    # 3. 造未来 (Make Future Dataframe)
    future = model.make_future_dataframe(periods=30) # 预测未来30天

    # 4. 预测 & 诊断
    forecast = model.predict(future)
    fig1 = model.plot_components(forecast) # 拆解：看周几生意最好？春节影响多大？
    ```

!!! tip "当 Prophet 失效了怎么办？(Custom Modeling)"

    **大招**：**回归 XGBoost+特征工程**。

    *   手动构造特征：`lag_1` (昨天销量), `lag_7` (上周销量), `is_promo_start` (是否促销第一天)。
    *   从 "时间轴思维" 切换回 "特征思维"，把时序问题变成经典回归问题。这才是 Senior DA 的终极解决方案。

### 6.2 XGBoost Champion (特征驱动)

> XGBoost 通用用法 (实例化 / 参数 / 两套 API) 详见 → [建模速查 (07_ml_models)](07_ml_models.md)

**时序场景的额外注意事项**：

```python
# 时序用 XGBoost 时，必须去掉日期列 (XGBoost 不接受 datetime)
feature_cols = [c for c in X_train.columns if c != 'order_date']
xgb_X_train = X_train[feature_cols]
xgb_X_test  = X_test[feature_cols]
```

---

## Step 7: 📉 评估与回测 (Evaluation)

### 7.1 分层评估 (Stratified Evaluation)

> **Why?** 只看整体 M[目标业务] 会掩盖极值点的真实表现。Senior 必须分层评估。

??? example "分层评估代码模板"

    ```python
    from sklearn.metrics import mean_absolute_error

    # 划分极值点 (Top 10%) 和普通点
    top_10pct_threshold = y_test.quantile(0.9)
    mask_extreme = y_test >= top_10pct_threshold

    mae_overall = mean_absolute_error(y_test, y_pred)
    mae_extreme = mean_absolute_error(y_test[mask_extreme], y_pred[mask_extreme])
    mae_normal  = mean_absolute_error(y_test[~mask_extreme], y_pred[~mask_extreme])

    print(f'Overall M[目标业务]:  {mae_overall:.2f}')
    print(f'Extreme M[目标业务]:  {mae_extreme:.2f}')  # 极值预测好不好？
    print(f'Normal M[目标业务]:   {mae_normal:.2f}')
    ```

### 7.2 预测值 vs 真实值 (Predictions vs Actuals)

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

### 7.3 误差分析 (Error Analysis by Time)

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

### 7.4 特征重要度 (Feature Importance)

检查模型最依赖哪些特征，用于筛选特征或解释模型。

??? example "Feature Importance 可视化"

    ```python
    import xgboost as xgb

    # xgb_model 是训练好的 XGBoost 模型
    fig, ax = plt.subplots(figsize=(10, 8))
    xgb.plot_importance(xgb_model, ax=ax, height=0.5, max_num_features=20)
    plt.title('XGBoost Feature Importance')
    plt.show()
    ```

### 7.5 可视化技巧：自适应箱线图 (Adaptive Boxplots)

> **Why?** 特征多了以后，图容易挤在一起。用 **自适应画布 (Adaptive Figure Size)** 动态调整长宽，确保每张图都清晰。

```python
# 1. 明确行和列
targets = ['quantity', 'gmv', 'order_cnt'] 
time_dims = ['dayofweek', 'month', 'year']

n_rows = len(targets)
n_cols = len(time_dims)

# 2. 自适应计算画布大小 (每张小图 6x4 inch)
fig_width = n_cols * 6
fig_height = n_rows * 4

fig, axes = plt.subplots(n_rows, n_cols, figsize=(fig_width, fig_height))

# 3. 循环绘图
for i, y_col in enumerate(targets):
    for j, x_col in enumerate(time_dims):
        # showfliers=False: 隐藏异常值，让长尾数据的分布更清晰
        sns.boxplot(data=df, x=x_col, y=y_col, ax=axes[i][j], showfliers=False)
        axes[i][j].set_title(f'{y_col} by {x_col}')

plt.tight_layout()
plt.show()
```

---

## 进阶策略

### 多步预测策略对比 (Multi-step Forecasting)

| 策略                 | 做法                         | 误差累积 | 模型数量 | 推荐场景         |
| :------------------- | :--------------------------- | :------- | :------- | :--------------- |
| **Recursive** (递归) | 用 t+1 预测值作为 t+2 的输入 | 严重     | 1 个     | 短期 (<5 步)     |
| **Direct** (直接)    | 每步训练独立模型             | 无       | N 个     | 中长期 (7-30 天) |
| **MIMO** (多输出)    | 一个模型同时输出多个未来值   | 无       | 1 个     | 推荐尝试         |

!!! warning "递归预测 (Recursive) 的误差累积"

    Recursive 策略每一步都用上一步的预测值作为输入，误差会像滚雪球一样越来越大。

    - **<5 步**: 可接受
    - **7-14 步**: 需要评估误差衰减
    - **30 步**: 风险很高，建议用 Direct 或 MIMO

### 时序高阶技巧速查表

| 技术点 (Technique)                   | 核心原理 (Concept)                          | 代码片段 (Code Snippet)               | 解决什么问题 (Why?)                                                |
| :----------------------------------- | :------------------------------------------ | :------------------------------------ | :----------------------------------------------------------------- |
| **Differencing**<br>(差分)           | 预测增量而不是总量<br>`y_t = x_t - x_{t-1}` | `df['diff'] = df['y'].diff()`         | **Tree Model 不能外推**。让数据变得平稳，消除长期趋势。            |
| **Reconstruction**<br>(还原)         | 把增量加回去<br>`pred = last_y + diff`      | `pred = df['y'].shift(1) + pred_diff` | 预测完差分后，必须**还原**成真实销量才能给业务看。                 |
| **Time Series CV**<br>(时序交叉验证) | 滑动窗口验证<br>不能随机 Split!             | `TimeSeriesSplit(n_splits=5)`         | **防穿越** (Data Leakage)。确保训练集永远在测试集的时间之前。      |
| **Robustness**<br>(敏感性检验)       | 加噪音测试                                  | `X_test['feat'] += noise`             | **防过拟合**。如果加了 5% 噪音预测结果就崩了，说明模型在死记硬背。 |
