# 📊 SQL vs Pandas 数据类型对照表

> **给 SQL 玩家的速查指南**：
> Pandas 的底层是 **NumPy**，所以它的类型系统其实是“C语言风格”的计算器类型，和数据库的存储类型略有不同。

## 1. 核心对照表 (最常用)

| SQL 类型            | Pandas 类型 (`df.info()`) | Python 原生 | 📝 人话解释                                                                        |
| :------------------ | :------------------------ | :---------- | :-------------------------------------------------------------------------------- |
| **VARCHAR / TEXT**  | **`object`** (最常见)     | `str`       | **文本**。Pandas 里凡是字符串、或者乱七八糟混在一起的东西，都叫 `object` (对象)。 |
| **INT / BIGINT**    | **`int64`**               | `int`       | **整数**。`64` 代表它能存很大的数 (64位)。                                        |
| **FLOAT / DECIMAL** | **`float64`**             | `float`     | **小数**。注意：Pandas 里没有 DECIMAL 这种高精度类型，统一用 float。              |
| **BOOLEAN**         | **`bool`**                | `bool`      | **真假**。(`True` / `False`)                                                      |
| **DATETIME**        | **`datetime64[ns]`**      | `datetime`  | **时间**。精确到纳秒 (ns)。                                                       |
| **NULL**            | `NaN` (通常显式为 float)  | `None`      | **空值**。注意下面的“空值坑”。                                                    |

---

## 2. 三个必须知道的“坑” 🕳️

### 🚩 坑 1: `object` 是个垃圾桶
*   **SQL**: `VARCHAR` 只能存字符串。
*   **Pandas**: `object` 是一个“万能指针”。
    *   如果一列全是字符串 -> `object`
    *   如果一列有数字、有字符串、还有列表 -> 也是 `object`
    *   **警惕**：当你看到一列本该是数字的列变成了 `object`，说明里面混进了脏东西（比如字符串 "NULL" 或 "Unknown"）。

### 🚩 坑 2: `int` 变 `float` (空值传染)
*   **SQL**: `INT` 列可以有 `NULL`。
*   **Pandas (旧版)**: `NaN` (空值) 在底层本质上是一个 **小数 (float)**。
    *   后果：如果一列整数 (`[1, 2, 3]`) 里混进了一个空值 (`NaN`)，整列会被强制“降级”变成 **浮点数** (`[1.0, 2.0, 3.0, NaN]`)。
    *   *注：最新的 Pandas 已经推出了 `Int64` (大写I) 类型来解决这个问题，但默认行为通常还是转 float。*

### 🚩 坑 3: `category` (枚举)
*   **SQL**: `ENUM`
*   **Pandas**: `category`
*   **作用**：如果有列数据是重复的（比如 'Male', 'Female' 重复 100万次），转成 `category` 能极大地节省内存。`tips` 数据集里之所以有 `category`，就是为了演示这个优化。

---

## 3. 如何类型转换？(Type Casting)

在 SQL 里你写 `CAST(col AS INT)`，在 Pandas 里这样写：

```python
# 转整数
df['col'] = df['col'].astype(int)

# 转小数
df['col'] = df['col'].astype(float)

# 转时间 (最常用！因为读进来往往是字符串)
df['date'] = pd.to_datetime(df['date'])

# 转文本
df['col'] = df['col'].astype(str)
```
