# 🧹 Pandas 数据清洗速查表 (SQL 玩家版)

你完全猜对了！这些函数的设计逻辑和 SQL 非常像。这是给你的“作弊条”：

## 1. 删除无效行 (dropna)
> SQL: `DELETE FROM table WHERE col IS NULL`

```python
# 默认：只要有空值，整行删除
df.dropna()

# ✅ 常用：只看特定列 (相当于 WHERE col IS NOT NULL)
df.dropna(subset=['order_id', 'user_id'])

# 进阶：全空才删 (How)
df.dropna(how='all') 
```

## 2. 填充缺失值 (fillna)
> SQL: `COALESCE(col, 0)`

```python
# 全部填充
df.fillna(0)

# ✅ 常用：按列填充
df['amount'] = df['amount'].fillna(0)
df['desc'] = df['desc'].fillna('Unknown')
```

## 3. 删除重复值 (drop_duplicates)
> SQL: `DISTINCT` 或 `ROW_NUMBER() ... WHERE rn=1`

```python
# 默认：完全重复才删
df.drop_duplicates()

# ✅ 常用：按主键去重 (Subset)
df.drop_duplicates(subset=['order_id'])

# 进阶：保留哪一个？(Keep)
# keep='first' (默认，保留第一条) | 'last' (保留最后一条) | False (全删)
df.drop_duplicates(subset=['order_id'], keep='last')
```

## 4. 类型转换 (astype)
> SQL: `CAST(col AS TYPE)`

```python
# 转整数/浮点
df['id'] = df['id'].astype(int)
df['price'] = df['price'].astype(float)

# 转字符串
df['code'] = df['code'].astype(str)
```

## 5. 字符串清洗 (.str 访问器)
> SQL: `REPLACE()`, `SUBSTRING()`, `LOWER()`

```python
# 替换 (Replace)
df['price'] = df['price'].str.replace('$', '')

# 切分 (Split) -> 得到一个列表
df['name'].str.split(' ')

# 包含 (Contains) -> 相当于 SQL LIKE
df['email'].str.contains('@gmail.com')
```

## 6. 🔥 必杀技：强制转日期 (to_datetime)
> SQL: `TRY_CAST(val AS DATE)` (处理不了的变 NULL)

这是 Pandas 最强的地方，它可以处理“脏日期”（比如 '2023-02-30' 或 'invalid'）。

```python
# errors='coerce': 遇到读不懂的日期，强行变成 NaT (Not a Time)，而不是报错！
df['date'] = pd.to_datetime(df['date'], errors='coerce')
```
