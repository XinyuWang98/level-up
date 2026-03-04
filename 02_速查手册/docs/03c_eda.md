# 🔍 EDA 探索性数据分析 (Exploratory Data Analysis)
*在动手建模之前，先和数据"混个脸熟"。*

## EDA 标准 SOP（4 步法）

```mermaid
graph LR
    A[1. 数据概览] --> B[2. 单变量分析]
    B --> C[3. 双变量/多变量分析]
    C --> D[4. 异常 & 结论]
```

### Step 1: 数据概览 (The Big Picture)
```python
# 基础三件套
df.shape                      # 多少行 × 多少列
df.info()                     # 每列类型 + 非空数
df.describe(include='all').T  # 统计量概览 (转置看更清爽)

# 进阶: 缺失率 + 唯一值 一键报告
df.isnull().mean().sort_values(ascending=False)  # 缺失率从高到低
df.nunique().sort_values()                        # 唯一值从少到多
```

### Step 2: 单变量分析 (Univariate)

| 数据类型 | 常用图表          | Seaborn 代码                                           |
| :------- | :---------------- | :----------------------------------------------------- |
| 数值型   | 直方图 + KDE      | `sns.histplot(df['col'], kde=True)`                    |
| 数值型   | 箱线图 (看异常值) | `sns.boxplot(x=df['col'])`                             |
| 类别型   | 柱状图 (频次)     | `sns.countplot(x='col', data=df)`                      |
| 类别型   | 饼图 (占比)       | `df['col'].value_counts().plot.pie(autopct='%1.1f%%')` |

!!! tip "长尾分布处理"
    *   `np.log1p(x)`: 对数变换，把长尾拉回来（用于金额/次数）
    *   `pd.qcut(x, q=10)`: 分箱，把连续值变成类别值（用于年龄/评分）
    *   **先画直方图看分布，再决定是否需要变换！**

### Step 3: 双变量/多变量分析 (Bivariate / Multivariate)

```python
# 1. 数值 vs 数值: 相关性热力图
corr_matrix = df.select_dtypes(include='number').corr()
sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', center=0)

# 2. 数值 vs 类别: 分组箱线图
sns.boxplot(x='category', y='price', data=df)

# 3. 类别 vs 类别: 交叉表 + 卡方检验
ct = pd.crosstab(df['gender'], df['purchased'])
from scipy.stats import chi2_contingency
chi2, p_val, dof, expected = chi2_contingency(ct)
print(f"卡方统计量: {chi2:.2f}, p 值: {p_val:.4f}")

# 4. 散点图矩阵 (一次性看所有数值变量之间的关系)
sns.pairplot(df[['age', 'income', 'spending']], diag_kind='kde')
```

### Step 4: 异常 & 结论 (Findings)

完成 EDA 后，**必须总结以下要点** (面试时经常被问到)：

- [ ] 数据量级？多少行多少列？
- [ ] 有哪些缺失？缺失比例多大？怎么处理的？
- [ ] 目标变量 (y) 的分布？是否存在类别不平衡？
- [ ] 哪些特征和目标变量强相关？
- [ ] 是否存在明显的异常值？怎么处理的？
- [ ] 有没有发现 surprising 的 pattern？

---

## 电商数据 EDA 经典指标

在处理电商行为数据（如 view/cart/purchase 事件流）时，以下指标几乎是必算的：

| 指标             | 公式                             | 含义                   |
| :--------------- | :------------------------------- | :--------------------- |
| **CVR (转化率)** | `purchase_users / view_users`    | 看了之后买了的比例     |
| **加购率**       | `cart_users / view_users`        | 看了之后加购的比例     |
| **加购转化率**   | `purchase_users / cart_users`    | 加了购物车后买的比例   |
| **客单价 (AOV)** | `total_revenue / purchase_users` | 平均每个买家花多少钱   |
| **ARPU**         | `total_revenue / total_users`    | 平均每个用户贡献的收入 |
| **用户活跃天数** | `date.nunique() per user`        | 用户在多少天里有行为   |

```python
# 快速计算核心指标
total_users = df['user_id'].nunique()
view_users = df.loc[df['event_type'] == 'view', 'user_id'].nunique()
cart_users = df.loc[df['event_type'] == 'cart', 'user_id'].nunique()
purchase_users = df.loc[df['event_type'] == 'purchase', 'user_id'].nunique()
total_revenue = df.loc[df['event_type'] == 'purchase', 'price'].sum()

CVR = purchase_users / view_users
AOV = total_revenue / purchase_users
ARPU = total_revenue / total_users

print(f"总用户数: {total_users:,}")
print(f"CVR: {CVR:.2%}")
print(f"AOV (客单价): {AOV:.2f}")
print(f"ARPU: {ARPU:.2f}")
```
