# 🔧 特征工程标准流程 (Feature Engineering SOP)

> **💡 核心原则**: 特征工程不是"盲目堆砌"，而是"验证假设"。所有的特征都应该来源于 **EDA (Exploratory Data Analysis)** 的洞察。

## Phase 1: 业务驱动 (Business Logic & Explainability) 💡

**最优先做！** 这些特征通常可解释性最强，能直接回答"为什么"。

1.  **EDA 转化**:
    *   *EDA 发现*: "周末卖得好" → **Action**: `df['is_weekend'] = df['dayofweek'].isin([5,6])`
    *   *EDA 发现*: "节假日后销量暴跌" → **Action**: `df['days_since_holiday']`
2.  **交互特征 (Interaction)**:
    *   **业务公式**: `Sales = Price * Qty`
    *   **比率**: `Promotion_Ratio = Discount / Original_Price`
    *   **差异**: `Price_Diff = My_Price - Competitor_Price`

---

## Phase 2: 数据预处理 (Preprocessing) 🧹

**清洗数据的标准动作。**

1.  **日期拆解 (Date Decomposition)**:
    *   **基础**: Year, Month, Day, DayOfWeek, WeekOfYear.
    *   **周期**: `sin(2*pi*month/12)`, `cos(2*pi*month/12)` (保留周期性，如 12月和1月挨着)。
2.  **缺失值策略 (Missing Value Strategy)**:
    *   **Data 量极大 (>1M)**: 直接丢弃 (`dropna`)。
    *   **策略分流**:
        *   **Tree 模型 (XGB/LGB/CatBoost)**: 🟢 **通常不需要填补！**
            *   模型会自动学习缺失值的最佳分裂方向 (Default Direction)。
            *   *例外*: 如果业务上 `NaN` 代表 0 (如没销量)，必须 `fillna(0)`。
        *   **Linear/NN 模型 (LR/DeepLearning)**: 🔴 **必须填补！**
            *   无法处理 NaN，报错。必须用 `Mean/Median/Zero` 填充。
    *   **特殊技巧**: 增加 `is_missing` 指示列 (有时候"缺失"本身就是一种信息，比如"用户没填性别"可能意味着隐私意识强)。
3.  **编码与变换**:
    *   **Target Encoding**: 高维类别 (如 UserID) → 转化为 "该用户历史点击率"。**必须在 Split 之后做！**
    *   **Log Transform**: Target 长尾分布时必须做 (`np.log1p`)。

---

## Phase 3: 批量构建 (Batch Construction - The "Magic") 🪄

**时序/序列数据的核心武器。** (参数 `window` 的选择必须基于 EDA 的 ACF/PACF 图)

| 特征类型         | 含义 (Meaning) | 代码逻辑 (Pandas)                                | 适用场景                                                     |
| :--------------- | :------------- | :----------------------------------------------- | :----------------------------------------------------------- |
| **Lag (滞后)**   | 过去的值       | `df.groupby('id')['val'].shift(lag)`             | **最强特征**。昨天卖了多少？上周今天卖了多少？(Lag 1, 7, 52) |
| **Diff (增量)**  | 变化量         | `df.groupby('id')['val'].diff(lag)`              | 增长趋势。今天比昨天多卖多少？                               |
| **Rolling Mean** | 周期水平       | `df.groupby('id')['val'].rolling(window).mean()` | 剔除波动看水平。最近 7 天平均卖多少？                        |
| **Rolling Std**  | 波动幅度       | `df.groupby('id')['val'].rolling(window).std()`  | **风险特征**。最近销量稳不稳定？                             |

**💻 自动化构建代码 (Snippet):**

```python
# 基于 EDA 发现的周期 (7天=周, 28天=月)
lags = [1, 7, 14, 28]
rollings = [7, 28]

for lag in lags:
    df[f'sales_lag_{lag}'] = df.groupby('store')['sales'].shift(lag)

for window in rollings:
    df[f'sales_roll_mean_{window}'] = df.groupby('store')['sales'].transform(
        lambda x: x.rolling(window=window).mean())
    df[f'sales_roll_std_{window}'] = df.groupby('store')['sales'].transform(
        lambda x: x.rolling(window=window).std())
```

---

## Phase 4: 筛选与瘦身 (Selection & Screening) ⚖️

**给模型减负，防止过拟合。**

1.  **方差过滤 (Variance Threshold)**:
    *   删掉所有值都一样的列 (Variance=0)。
2.  **共线性检查 (Multicollinearity)**:
    *   **线性模型 (LR/Lasso/Ridge)**: **🔥 必须做！**

        ```python
        from statsmodels.stats.outliers_influence import variance_inflation_factor
        
        # 1. 计算 VIF，通常 VIF > 10 建议删除
        vif_data = pd.DataFrame()
        vif_data["feature"] = X.columns
        vif_data["VIF"] = [variance_inflation_factor(X.values, i) for i in range(X.shape[1])]
        
        print(vif_data.sort_values('VIF', ascending=False))
        ```
    *   **树模型 (XGB/LGB/RF)**: **通常不需要** (模型 robust，能自动选最好的切分点)。
3.  **特征重要性 (Feature Importance)**:
    *   先跑一个 RF/LGBM Baseline。
    *   `plot_importance` 算出排名。
    *   删掉 Importance=0 的尾部特征。

---

## Data Leakage 终极防线 🚨

*   **穿越 (Leakage)**: 用了"未来"的数据预测"现在"。
*   **检查清单**:
    *   [ ] `shift` 的方向对吗？(只能 `shift(正数)`，不能 `shift(-1)`！)
    *   [ ] `Target Encoding` 是不是只用了 Train set？
    *   [ ] `StandardScaler` 是不是只 `fit(X_train)`？
    *   [ ] 预测"明天销量"时，是不是用了"明天的天气"？(如果是预报天气可以，如果是实测天气就不行！)
