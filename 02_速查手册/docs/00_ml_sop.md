# 🧭 机器学习标准流程 (ML SOP)

> **⭐ 核心原则**: 80% 的时间在洗数据 (Step 1-5)，20% 的时间在建模 (Step 6-9)。
> "Garbage In, Garbage Out" 是唯一的真理。

## Phase 0: 破题 (Definition) 🎯

**动手写代码前，先回答这 3 个问题：**

1.  **任务类型**:
    *   **回归 (Regression)**: 预测连续值 (销量/房价/时长)。关注 `MSE`, `MAPE`, `R2`。
    *   **分类 (Classification)**: 预测类别 (流失/欺诈/点击)。关注 `AUC`, `F1`, `Recall`。

2.  **数据分布**:
    *   Target 是否长尾分布 (Long-tail)? → 考虑 `log` 变换 (如房价/销量)。
    *   类别是否极度不平衡 (Imbalanced)? → 考虑 `Class Weight` 或 `SMOTE`。

3.  **基准线**:
    *   怎么才算"好"? (比随机猜准多少? 比去年的策略提升多少?)

---

## Phase 1: 数据准备 (Preparation) 🛠️

| 步骤 (Step)                      | 关键动作 (Action)                                                             | 核心函数/注意点 (Checkpoint) 🛑                                                                                        |
| :------------------------------- | :---------------------------------------------------------------------------- | :-------------------------------------------------------------------------------------------------------------------- |
| **1. Exploratory (EDA)**         | **"特征灵感来源"** <br> 检查分布、相关性、季节性。                            | `sns.heatmap`, `seasonal_decompose` <br> *观察: 周五卖得少? 去年这周卖得多? → 都是特征！*                            |
| **2. Cleaning**                  | 填补缺失值，处理异常值。                                                      | `df.fillna()`, `df.dropna()` <br> *Tree 模型对缺失值不敏感，但 Linear 模型必须填。*                                   |
| **3. Feature Eng (Structural)**  | **结构化特征** (不依赖统计量)。<br> 构造 Lag, Date, Text Length, Interaction. | `shift()`, `dt.dayofweek`, `a/b` <br> *EDA 发现的规律在这里变成代码。*                                                |
| **4. Split (切分)**              | **严格切分！** (防穿越)                                                       | `train_test_split(random_state=42)` <br> *必须在统计特征(编码/缩放)之前！*                                            |
| **5. Feature Eng (Statistical)** | **统计类特征** (依赖分布)。<br> Encoding, Scaling, Imputation (Mean).         | `TargetEncoder`, `StandardScaler` <br> **必须只用 X_train fit, 然后 transform X_test！**                              |
| **6. Collinearity (共线性)**     | 检查多重共线性。                                                              | `VIF` <br> *Tree (XGB/RF): 能够容忍共线性 (自动选最好的)。* <br> *Linear (LR/Lasso): 必须消除共线性 (否则权重失效)。* |

### 1.1 EDA 核心套路 (Copy-Paste Ready) 🧰

**1. 时间拆解 (Time Slicing)**
*挖掘周期性 (Seasonality) 的第一步。*

```python
# 基础拆解
df['year'] = df['date'].dt.year
df['month'] = df['date'].dt.month
df['dayofweek'] = df['date'].dt.dayofweek # 周几 (0=Mon, 6=Sun)

# 进阶业务逻辑 (发工资日? 月底业绩冲刺?)
df['is_weekend'] = df['dayofweek'].isin([5, 6]).astype(int)
df['is_month_start'] = df['date'].dt.is_month_start.astype(int) 
df['is_month_end'] = df['date'].dt.is_month_end.astype(int)
```

**2. 维度拆解 (Categorical Analysis)**
*看不同店铺/部门的 Target 分布 (Boxplot 是神器)。*

```python
# 看看哪些店卖得好，哪些店波动大 (方差大)？
plt.figure(figsize=(15, 6))
sns.boxplot(x='store', y='weekly_sales', data=df)
plt.title('Sales Distribution by Store')
# 结论: Store 14 简直是疯子 (离群点多)，Store 33 是死水 (低且平)。
```

**3. 标签观测 (Feature vs Label)**
*验证假设：节假日真的卖得好吗？*

```python
# 节假日 vs 非节假日 (均值可能差不多，但上限极高！)
sns.boxplot(x='holiday_flag', y='weekly_sales', data=df)
```

**4. 异常检测 (Outlier Detection - IQR)**
*找出那些"离谱"的日子。这些不仅仅是异常值，通常是**超级大促** (如黑色星期五) 的线索！*

```python
Q1 = df['weekly_sales'].quantile(0.25)
Q3 = df['weekly_sales'].quantile(0.75)
IQR = Q3 - Q1

# 定义异常边界 (通常是 1.5 倍 IQR，激进点可以用 3 倍)
lower_bound = Q1 - 1.5 * IQR
upper_bound = Q3 + 1.5 * IQR

# 谁是异常值？(打印出来看看日期，是不是超级碗/圣诞节？)
outliers = df[(df['weekly_sales'] < lower_bound) | (df['weekly_sales'] > upper_bound)]
print(f"异常值数量: {len(outliers)}")
print(outliers[['date', 'weekly_sales', 'holiday_flag']].sort_values('weekly_sales', ascending=False).head())
```

---

## Phase 2: 建模与评估 (Modeling) 🤖

| 步骤 (Step)       | 关键动作 (Action) | 核心函数/注意点 (Checkpoint) 🛑                                                               |
| :---------------- | :---------------- | :------------------------------------------------------------------------------------------- |
| **7. Baseline**   | 建立基准线。      | `RandomForest` (简单/抗造) <br> *先跑通流程，确立下限。*                                     |
| **8. Challenger** | 引入强模型。      | `XGBoost`, `LightGBM` <br> *尝试提升精度 (Bias)。*                                           |
| **9. Evaluation** | 科学评估。        | `cv_results`, `classification_report` <br> *别只看 Accuracy！看业务关注的指标 (如 Recall)。* |
| **10. Interpret** | 解释模型。        | `SHAP` <br> *告诉业务方："为什么预测他会流失？" (因为他在投诉)*                              |

---

## Phase 3: 业务闭环 (Action) 💼

*   **输出**: 不只是模型文件 (`.pkl`)，而是 **Actionable Insights**。
    *   "高潜名单" (Leads List)
    *   "高危预警" (Churn Alert)
    *   "策略建议" (Top Drivers)
*   **监控**: 上线后监控 PSI (Population Stability Index)，防止模型衰退。

---

## 各章节直达 🚀
*   🔧 **特征工程**: [Step 3 & 5 - 06_feature_engineering](06_feature_engineering.md)
*   ✂️ **数据集切分**: [Step 4 - 06b_data_splitting](06b_data_splitting.md)
*   🤖 **建模实战**: [Step 7 & 8 - 07_ml_models](07_ml_models.md)
*   📏 **评估指标**: [Step 9 - 08_evaluation](08_evaluation.md)
