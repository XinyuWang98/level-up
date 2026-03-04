# 🧼 数据清洗 (Data Cleaning)
*拿到数据后的第一步：确保数据"干净"。*

## 标准清洗 SOP 流程

```python
# 1. 快速体检 (一分钟看完整体状况)
df.info()                     # 类型 + 非空数
df.isnull().mean()            # 缺失比例
df.describe(include='all').T  # 统计概览 (转置更清爽)

# 2. 去重
df = df.drop_duplicates(subset=['uid'], keep='first')

# 3. 缺失值处理 (三选一)
df = df.dropna(subset=['critical_col'])              # 关键列有空就扔
df['col'] = df['col'].fillna(df['col'].median())     # 数值列填中位数
df['col'] = df['col'].fillna('unknown')              # 类别列填占位符

# 4. 类型转换 (最容易被忽略的一步)
df['date'] = pd.to_datetime(df['date'])
df['id']   = df['id'].astype(str)
df['amt']  = pd.to_numeric(df['amt'], errors='coerce')
```

## 缺失值处理策略

| 缺失比例 | 推荐策略                              | 口诀                           |
| :------- | :------------------------------------ | :----------------------------- |
| < 5%     | 直接删行 `dropna()`                   | "少量缺失，大胆删"             |
| 5% ~ 30% | 填充 (均值/中位数/众数/`'unknown'`)   | "中等缺失，智慧填"             |
| > 30%    | 考虑删列，或作为特征 (`is_null` 标志) | "大量缺失，列见鬼（或变特征）" |

!!! tip "缺失值填充的一行流 (One-Liner Imputation)"
    别再分两步写 `mean = ...` 然后 `fillna` 了！
    
    *   **Code**: `df['col'] = df['col'].fillna(df['col'].mean())`
    *   **Logic**: Pandas 会先算括号里的均值，再填进去。清晰、优雅、常用。

!!! tip "全面体检 (Missing Value Audit)"

    *   **看数量**: `df.isnull().sum()` (基础)
    *   **看比例**: `df.isnull().mean()` (Senior 必看! 决定是删行还是删列)
    *   **可视化**: `sns.heatmap(df.isnull(), cbar=False)` (最直观)

## 异常值检测

### 1. 百分位数极值处理 (Quantile 分位数法) - ⭐️ 业务最常用
这是互联网公司处理长尾金额、极端播放量最常用的手段：去掉（或截断）最顶部 1%或 5% 的数据。

```python
# 1. 计算 99% 分位数 (返回一个具体的数字)
p99 = df['amount'].quantile(0.99)
p01 = df['amount'].quantile(0.01)

# ✅ 做法 A: 直接删除最顶部的 1% (布尔过滤)
df_clean = df[df['amount'] <= p99]

# ✅ 做法 B: 盖帽法/截断 (Clip) - 推荐！
# 把大于 p99 的值强行变成 p99，小于 p01 的强行变成 p01，不删行。
df['amount_capped'] = df['amount'].clip(lower=p01, upper=p99)
```

### 2. IQR 法 (箱线图原理)
```python
Q1 = df['col'].quantile(0.25)
Q3 = df['col'].quantile(0.75)
IQR = Q3 - Q1

# 定义异常边界
LOWER_BOUND = Q1 - 1.5 * IQR
UPPER_BOUND = Q3 + 1.5 * IQR

# 筛出异常值
outliers = df[(df['col'] < LOWER_BOUND) | (df['col'] > UPPER_BOUND)]
print(f"异常值数量: {len(outliers)}, 占比: {len(outliers)/len(df):.2%}")
```

### Z-Score 法 (标准正态分布)
```python
from scipy import stats

# |Z| > 3 视为异常 (距离均值超过 3 个标准差)
z_scores = stats.zscore(df['col'].dropna())
outlier_mask = (z_scores.abs() > 3)
print(f"Z-Score 异常值数量: {outlier_mask.sum()}")
```

!!! warning "异常值处理的黄金法则"
    **先看分布图** → **再看业务含义** → **最后决定处理方式**
    
    *   **截断 (Clip)**: 保留记录，只压到边界值（推荐用于建模 / 聚合统计）
    *   **删除 (Drop)**: 直接扔掉（减少时仅在异常值确实是脏数据 / 录入错误时使用）
    *   **标记 (Flag)**: 新增 `is_outlier` 列（保留原始数据，最安全）

## 日期格式处理

!!! warning "日期格式必须精确匹配 (Date Format Gotcha)"
    `pd.to_datetime()` 对格式非常敏感！符号必须一一对应。
    
    *   **数据**: `'31/12/2023'` (斜杠，4位年)
    *   ❌ **%d%m%y**: 找纯数字（`311223`），失败。
    *   ❌ **%d/%m/%y**: 找2位年 (`/23`)，但数据是4位 (`/2023`)，失败。
    *   ✅ **%d/%m/%Y**: `%Y` 匹配 4 位年，`/` 匹配斜杠。完美。
    
    **常用符号**: `%Y`(2024), `%y`(24), `%m`(01-12), `%d`(01-31), `%H:%M:%S`
