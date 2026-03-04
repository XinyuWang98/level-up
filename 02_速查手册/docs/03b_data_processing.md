# 🔧 数据处理 & 宽表构建 (Data Processing & Wide Tables)
*从"明细表"到"用户特征宽表"，你需要的所有花式操作都在这里。*

## 宽表终极选择：Groupby 命名聚合 vs Pivot_Table ⚔️

在做 **A/B 测试的 EDA** 或 **特征工程**（例如：把明细宽表转化为"每个用户一行"的特征表）时，经常需要在 `groupby` 和 `pivot_table` 之间犹豫。

| 场景                                             | 推荐方案                     | 原因                         |
| :----------------------------------------------- | :--------------------------- | :--------------------------- |
| 单一指标，把分类值变成列名                       | `pivot_table`                | 一句话搞定，最简单           |
| 多维度重度聚合（次数 + 金额 + 去重数）           | `groupby().agg()` + 命名聚合 | 扁平输出，无 MultiIndex 困扰 |
| 把具体分类值铺开成列名（如品牌 × 行为 = 几千列） | `pivot_table` 循环 + `join`  | 生成高维稀疏特征矩阵         |

### 🔥 写法一：打平多维指标 (Named Aggregation)

先通过 `np.where` 为不同类型生成独立列（便于后续分别求和等），然后一次性 `agg`：

```python
import numpy as np

# 1. 前置准备：为不同的指标拆分出单独的列
df['view_price'] = np.where(df['event_type'] == 'view', df['price'], 0)
df['cart_price'] = np.where(df['event_type'] == 'cart', df['price'], 0)
df['purchase_price'] = np.where(df['event_type'] == 'purchase', df['price'], 0)

df['is_view'] = (df['event_type'] == 'view').astype(int)
df['is_cart'] = (df['event_type'] == 'cart').astype(int)
df['is_purchase'] = (df['event_type'] == 'purchase').astype(int)

# 2. 一次性重度聚合 (Named Aggregation)
user_features = df.groupby('user_id').agg(
    # --- 行为次数统计 ---
    total_views=('is_view', 'sum'),
    total_carts=('is_cart', 'sum'),
    total_purchases=('is_purchase', 'sum'),
    # --- 金额总计 ---
    sum_view_price=('view_price', 'sum'),
    sum_cart_price=('cart_price', 'sum'),
    sum_purchase_price=('purchase_price', 'sum'),
    # --- 多样性统计 ---
    unique_products=('product_id', 'nunique'),
    unique_categories=('category_code', 'nunique'),
    unique_brands=('brand', 'nunique')
).reset_index()
# 结果 user_features 出生即是完美扁平单层列宽表！
```

!!! tip "批量构造聚合字典 (字典解包法)"
    如果你有大量的列需要分别设置不同的聚合函数，可以用字典推导式动态构造 `agg_dict`，完全替代 `for` 循环：
    
    ```python
    target_nunique = ['category_lv1', 'brand', 'product_id', 'user_session']
    target_sum = ['price']
    
    agg_dict = {col: 'nunique' for col in target_nunique}
    agg_dict.update({col: 'sum' for col in target_sum})
    # agg_dict = {'category_lv1': 'nunique', 'brand': 'nunique', ..., 'price': 'sum'}
    
    df_grouped = df.groupby(['user_id', 'event_type']).agg(agg_dict)
    ```

### 🌌 写法二：高维稀疏特征展开 (High-Dimensional Cross Features)

当你需要把具体的**分类值本身变成列名**时（例如，基于品牌列表 `brand = ['apple', 'samsung', ...]`，想统计出 `brand_apple_view_cnt`, `brand_samsung_purchase_cnt`），就需要借助 `pivot_table` 的循环透视大法！

**这是推荐系统/增益模型生成极度稀疏特征矩阵（User Profile）的标准写法：**

```python
# ==========================================
# 需求：把分类值铺开，与事件类型交叉计算次数
# ==========================================
df['action_count'] = 1 # 用来做最基础的计数 (count)

# ============== 动作 1：透视分类特征 ==============
expanded_dfs = []
# ⚠️ 强烈预警：不要放 unique 超过 1 万的底层 ID 字段，会 OOM 撑爆内存
target_cols = ['category_lv1', 'brand']

for col in target_cols:
    pivot_df = df.pivot_table(
        index='user_id', 
        columns=[col, 'event_type'], # 生成多层列名
        values='action_count', 
        aggfunc='sum', 
        fill_value=0
    )
    
    # 将多层列名打平: ('apple', 'view') -> brand_apple_view_cnt
    pivot_df.columns = [f"{col}_{str(c[0])}_{c[1]}_cnt" for c in pivot_df.columns]
    expanded_dfs.append(pivot_df)

# ============== 动作 2：常规特征聚合 ==============
base_df = df.pivot_table(
    index='user_id',
    columns='event_type', 
    values=['price', 'user_session'], 
    aggfunc={'price': 'sum', 'user_session': 'nunique'}, 
    fill_value=0
)
# 这里也会产生多重索引，需打平
base_df.columns = [f"{c[0]}_{c[1]}" for c in base_df.columns]

# ============== 动作 3：超级大合并 ==============
# 将 base_df 挨个儿横向 join 上所有的稀疏特征矩阵
user_df = base_df.join(expanded_dfs).reset_index()

# 最终会得到一张动辄几千上万列的高度稀疏矩阵！(非常正常)
```

!!! warning "高维展开的内存红线"
    | 字段类型       | Unique 数量 | 展开后列数 (× 3 event_type) | 是否安全 |
    | :------------- | :---------- | :-------------------------- | :------- |
    | `category_lv1` | ~14         | ~42                         | ✅ 安全   |
    | `brand`        | ~2,000      | ~6,000                      | ⚠️ 可行   |
    | `product_id`   | ~60,000     | ~180,000                    | ❌ OOM！  |
    
    **经验法则**: Unique > 10,000 的底层 ID 类字段，应该用 `scipy.sparse` 稀疏矩阵或 Embedding 代替。

---

## 一列变多列：str.split() 的优雅赋值法则 ✂️

当使用 `str.split(expand=True)` 时，Pandas 会生成一个全新的 DataFrame，列名变成了 `0, 1, 2...`。如何塞回原表？

### 🌟 方案 1: 精准提取法 (最高效、最不易报错、生产首选)
不要把整个列表展开，而是精确提取想要的层级。即使某一行的内容包含超多分隔符，也不会产生多余的垃圾列。
```python
# 取拆分后的第一段 (索引 0)
df['main_category'] = df['category_code'].str.split('.').str[0]

# 取拆分后的第二段 (索引 1)
df['sub_category']  = df['category_code'].str.split('.').str[1]
```

### 🧩 方案 2: 拼图合并法 (无需数有多少列)
如果不确定拆出多少列，但想全部保留：先独立展开 -> 批量改列名 -> 拼回原表。
```python
# 1. 生成独立展开结果表 (expand=True)
split_cols = df['category_code'].str.split('.', expand=True)

# 2. 批量改名 (自动生成 category_level_0, category_level_1...)
split_cols = split_cols.add_prefix('category_level_')

# 3. 横向合并回原表
df = df.join(split_cols)
```

---

## MultiIndex 列名打平大全

当 `pivot_table` 或 `groupby` 产生多层列名 (MultiIndex) 时，后续操作极其痛苦。以下是 3 种打平方法：

```python
# 方法 1: 列表推导式 (最常用)
df.columns = [f'{col[0]}_{col[1]}' for col in df.columns]

# 方法 2: add_prefix (适用于单层新表)
split_cols = split_cols.add_prefix('category_level_')

# 方法 3: droplevel (只想保留一层)
df.columns = df.columns.droplevel(0)  # 丢弃第一层
```

最后别忘了 `df = df.reset_index()` 把行索引也释放回来！
