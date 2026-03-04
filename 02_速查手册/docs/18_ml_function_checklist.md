# 🧰 ML高频实战函数参数详解 (The Parameter Master)

> **使用指南**: 核心参数都已用注释标注了**默认值**和**最佳实践**。复制这些代码块，根据你的数据微调即可。

---

## 🔥 核心：ML 黄金 Pipeline 傻瓜式代码流
*当你突然大脑空白，不知道下一步写什么时，直接 Copy-Paste 这套流程！*

### Step 1: 类别特征编码 (One-Hot)
```python
# 把 'gender', 'city' 等字符串列变成 0/1 列
df_encoded = pd.get_dummies(df, columns=['需要编码的列名1', '需要编码的列名2'], drop_first=True).astype(int)
# ⚠️ .astype(int) 是必须的！新版 Pandas 的 get_dummies 返回 bool，XGBoost 不认识 bool。
# 注意: 树模型 (XGB/LGBM) 有些可以直接处理 category 类型，但 get_dummies 是最万能的保底方案。
```

### Step 2: 拆分 X 和 y
```python
# 明确告诉模型：你要预测谁？谁是特征？
X = df_encoded.drop(columns=['你的目标列名(如churn)'])
y = df_encoded['你的目标列名(如churn)']
```

### Step 3: 切分训练集和测试集 (防穿越)
```python
from sklearn.model_selection import train_test_split

# test_size=0.2 表示留 20% 的数据用来考试
X_train, X_test, y_train, y_test = train_test_split(
    X, y, 
    test_size=0.2, 
    random_state=42, # 保证每次切分结果一样
    stratify=y       # 分类问题必加！保证训练集和测试集里正负样本比例一样
)
```

### Step 4: 特征缩放 (Scaling) - 仅限线性模型/距离模型
```python
from sklearn.preprocessing import StandardScaler

scaler = StandardScaler()
# 🔥 核心防穿越法则：只能对 Train fit，对 Test 只能 transform！
X_train_scaled = scaler.fit_transform(X_train) 
X_test_scaled = scaler.transform(X_test)
# (树模型 XGB/RF 不需要这一步！)
```

### Step 5: 训练与预测
```python
from xgboost import XGBClassifier # 或 sklearn.linear_model.LogisticRegression 等

model = XGBClassifier(random_state=42)
model.fit(X_train, y_train)

# 考卷答题
y_pred = model.predict(X_test)
y_pred_proba = model.predict_proba(X_test)[:, 1] # 算 AUC 时专用的概率值
```

---

## 1. 数据加载与基础处理 (Data Loading & Preprocessing)

### `pd.read_csv`

```python
df = pd.read_csv(
    filepath_or_buffer='data.csv',
    sep=',',             # 分隔符 (默认逗号，tsv是用'\t')
    header=0,            # 表头所在行 (默认第0行)
    parse_dates=['date'],# 自动解析时间列 (省去后续 to_datetime)
    usecols=['a', 'b'],  # 只读取指定列 (省内存神器)
    dtype={'id': str},   # 指定列类型 (防 id 被当成数字)
    nrows=1000           # 只读前1000行 (测试代码时用)
)
```

### `pd.to_datetime` (时间清洗最重要一步)

```python
df['date'] = pd.to_datetime(
    df['date'],
    format='%Y-%m-%d',   # 指定格式 (如 '2023-01-01')，提速极快
    errors='coerce'      # 遇到脏数据(如"unknown")设为 NaT，不报错
)
```

### `SimpleImputer` (缺失值填充)

```python
from sklearn.impute import SimpleImputer
imputer = SimpleImputer(
    strategy='mean',     # 填充策略: 'mean', 'median', 'most_frequent', 'constant'
    fill_value=0,        # 当 strategy='constant' 时，填充这个值
    missing_values=np.nan # 识别哪些值是缺失的
)
df['age'] = imputer.fit_transform(df[['age']]) # 注意: 输入必须是 2D array
```

## 2. 特征工程 (Feature Engineering)

### `pd.get_dummies` (One-Hot 编码)

```python
df = pd.get_dummies(
    df,
    columns=['city'],    # 指定要编码的分类列
    drop_first=True,     # 🔥 必选! 删除第一列 (防止多重共线性)
    dummy_na=False       # 是否为 NaN 专门生成一列 (一般False，先fillna再编码)
)
```

### `groupby().shift()` (Lag 特征 - 预测核心)

```python
# 构造"昨天"的销量
df['lag_1'] = df.groupby('store')['sales'].shift(
    periods=1,           # 滞后步数 (1=昨天，7=上周今天)
    fill_value=np.nan    # 移动后产生的空值填什么 (一般先留空，最后dropna)
)
```

### `groupby().rolling()` (滑窗统计)

```python
# 构造"过去7天"的平均销量
df['rolling_mean_7d'] = df.groupby('store')['sales'].rolling(
    window=7,            # 窗口大小 (7天)
    min_periods=1,       # 窗口期数据不足时也计算 (防NaN)
    closed='left'        # 🔥 关键! 只用"过去"的数据 (防未来数据泄露)
).mean().reset_index(0, drop=True)
```

## 3. 数据切分 (Data Splitting)

### `train_test_split` (分类/非时序问题)

```python
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(
    X, y,
    test_size=0.2,       # 测试集比例 (一般 0.2 或 0.3)
    random_state=42,     # 随机种子 (复现结果必备)
    stratify=y,          # 🔥 关键! 保持分类比例一致 (如流失率都是20%)
    shuffle=True         # 是否打乱 (非时序数据必须 True)
)
```

### `TimeSeriesSplit` (回归/时序问题)

```python
from sklearn.model_selection import TimeSeriesSplit
tscv = TimeSeriesSplit(
    n_splits=5,          # 切成 5 份 (前向验证)
    test_size=None,      # 自动根据 n_splits 计算
    gap=0                # 训练集和测试集之间的间隔 (防止 Lag 特征泄露)
)
# 用法: for train_index, test_index in tscv.split(X): ...
```

## 4. 模型构建与训练 (Model Building & Training)

### `XGBRegressor` (回归任务 - 销量预测)

```python
model = XGBRegressor(
    n_estimators=1000,   # 树的数量 (给大一点，靠 early_stopping 停)
    learning_rate=0.05,  # 学习率 (越小越稳，但需要更多树)
    max_depth=6,         # 树深 (一般 3-10，太深过拟合)
    subsample=0.8,       # 每棵树只用 80% 样本 (行采样，防过拟合)
    colsample_bytree=0.8,# 每棵树只用 80% 特征 (列采样，防过拟合)
    n_jobs=-1,           # 并行核数 (-1 = 用满CPU)
    random_state=42
)
```

### `XGBClassifier` (分类任务 - 流失预测)

```python
model = XGBClassifier(
    scale_pos_weight=4,  # 🔥 关键! 负样本/正样本比例 (处理样本不平衡)
    eval_metric='auc',   # 评估指标 (二分类常用 AUC)
    objective='binary:logistic', # 目标函数 (二分类概率)
    # 其他参数同 Regressor (n_estimators, max_depth...)
)
```

### `model.fit()` (训练与早停)

```python
model.fit(
    X_train, y_train,
    eval_set=[(X_test, y_test)], # 验证集 (用于观察是否过拟合)
    early_stopping_rounds=50,    # 🔥 关键! 50轮 loss 不降就停止 (防过拟合+省时间)
    verbose=10                   # 每 10 轮打印一次日志
)
```

## 5. 预测与评估 (Prediction & Evaluation)

### `model.predict` vs `model.predict_proba`

```python
# 回归 / 分类(硬预测)
y_pred = model.predict(X_test) 
# 输出: [120, 130...] 或 [0, 1, 0...]

# 分类(概率预测) - 🔥 计算 AUC/KS 必须用这个!
y_prob = model.predict_proba(X_test)[:, 1] 
# 输出: [0.1, 0.8, 0.2...] (取第二列，即正样本概率)
```

### `classification_report` (分类体检单)

```python
print(classification_report(
    y_true=y_test,
    y_pred=y_pred,       # 注意: 这里要传入 label (0/1)，不是概率
    target_names=['No', 'Yes'], # 类别名称 (方便看)
    digits=4             # 保留小数位
))
```

### `mean_absolute_percentage_error` (回归常用)

```python
# 输出: 0.05 代表误差 5%
mape = mean_absolute_percentage_error(
    y_true=y_test,
    y_pred=y_pred
)
```

### `cross_val_score` (交叉验证得分)

```python
from sklearn.model_selection import cross_val_score
scores = cross_val_score(
    estimator=model,
    X=X, y=y,
    cv=5,                # 5 折交叉验证
    scoring='roc_auc',   # 评分标准 (回归用 'neg_mean_absolute_error')
    n_jobs=-1
)
print(f"Mean AUC: {scores.mean():.4f}")
```

## 6. 自动调参 (Auto-Tuning)

### `RandomizedSearchCV` (性价比调参)

```python
search = RandomizedSearchCV(
    estimator=model,
    param_distributions=param_dist, # 参数字典 {'depth': [3,5]}
    n_iter=50,           # 尝试次数 (50次运气只要不是太差都能找到好的)
    scoring='neg_mean_absolute_error', # 评分标准 (注意 sklearn 是越大越好，所以是负数)
    cv=3,                # 交叉验证折数
    n_jobs=-1,           # 全力跑
    verbose=1            # 输出进度
)
```
