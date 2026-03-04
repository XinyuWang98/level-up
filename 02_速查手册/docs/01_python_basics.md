# 🐍 Python 基础 & 核心心法

## -1. 起手式 (The Boilerplate) 🏗️
*每次开局先贴这一段，省去 50% 的 debug 时间。*

```python
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
import platform

# 1. 忽略烦人的警告
warnings.filterwarnings('ignore')

# 2. Pandas 显示设置 (破解行列显示限制)
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', 100)
pd.set_option('display.width', 1000)
pd.set_option('display.float_format', lambda x: '%.3f' % x) # 避免科学计数法

# 2. 绘图设置 (高清 + 样式)
%matplotlib inline
sns.set(style='whitegrid', palette='muted', font_scale=1.5)

# 3. 解决中文乱码 (Mac/Windows 自适应) 🇨🇳
if platform.system() == 'Darwin':
    plt.rcParams['font.sans-serif'] = ['Arial Unicode MS'] # Mac专用
else:
    plt.rcParams['font.sans-serif'] = ['SimHei'] # Windows专用

plt.rcParams['axes.unicode_minus'] = False # 解决负号显示问题
```

!!! tip "怎么测速? (Benchmarking)"

    想知道代码跑得快不快？用这个"秒表"：

    ```python
    import time
    start = time.time()  # 掐表
    # ...(你的代码)...
    end = time.time()    # 停表
    print(f"耗时: {end - start:.2f} 秒")
    ```

## 0. 黄金流程 (The Golden SOP) 🌟 & 核心心法
**在你写下第一行 groupby 之前，必须走完这 5 步！**

| 步骤 (Step) | 动作 (Action)     | 核心代码 (Code)              | 目的 (Why)                                   |
| :---------- | :---------------- | :--------------------------- | :------------------------------------------- |
| **Step 1**  | **偷窥** (Peep)   | `df.head()`, `df.info()`     | 检查列名、数据类型 (Object vs Float)         |
| **Step 2**  | **清洗** (Clean)  | `df['id'].astype(str)`       | **修复错误类型** (这是 Describe 生效的前提!) |
| **Step 3**  | **体检** (Scan)   | `df.describe(include='all')` | **检查逻辑** (Unique 数是否合理? Min/Max?)   |
| **Step 4**  | **去重** (De-dup) | `df.duplicated().sum()`      | 确保没算重 (Count vs Unique)                 |
| **Step 5**  | **分析** (Start)  | `groupby`, `pivot_table`     | 开始干正事                                   |

### 核心心法 (Muscle Memory) 🏋️
*这些是我亲自踩坑练出来的，必须刻在 DNA 里。*

1.  **赋值! 赋值! 赋值!**
    *   ❌ `df['col'].astype(float)` (做了个寂寞)
    *   ✅ `df['col'] = df['col'].astype(float)` (存回去!)

2.  **GPS 定位修改**
    *   ❌ `df[df['age']>100]['age'] = np.nan` (SettingWithCopyWarning)
    *   ✅ `df.loc[df['age']>100, 'age'] = np.nan` (精准手术)

3.  **取单个值 (Scalar Trap) - 核心混淆点** 💣
    *   **场景**: 即便只剩一行，索引不一定是 0。此时用 `df.loc[0]` 必死。

    | 方法         | `[0]` 含义 (Meaning)   | 比喻 (Analogy)                | 推荐指数                |
    | :----------- | :--------------------- | :---------------------------- | :---------------------- |
    | `df.loc[0]`  | **名为 0 的标签**      | **呼喊人名** ("叫张三的出列") | ❌ (容易报错)            |
    | `df.iloc[0]` | **第 0 行** (绝对位置) | **点名排队** ("排第一的出列") | ✅ (取整行数据)          |
    | `.values[0]` | **第 0 个数值**        | **拆快递** (扔掉包装只拿货)   | 👑 **最推荐** (取纯数值) |

4.  **左右不分 (Merge Trap) - 左手定律** 🖐️
    *   **场景**: 关联数据后行数变少了，导致分母缩小，转化率虚高。
    *   ❌ `df_logs.merge(df_users, how='left')` (只保留了活跃用户)
    *   ✅ **左手定则**: 左手拿 **"花名册" (全量表)**，右手拿 **"记分牌" (行为表)**。

    | 左表 (Left)        | 右表 (Right)       | 结果 (Rows)                 | 缺失值 (NaN)                               |
    | :----------------- | :----------------- | :-------------------------- | :----------------------------------------- |
    | **全量表** (Users) | **行为表** (Logs)  | **行数不变** (等于左表)     | **没行为的用户补 NaN** (我们要的就是这个!) |
    | **行为表** (Logs)  | **全量表** (Users) | **行数减少** (只剩活跃用户) | **没行为的用户直接丢了** (留存陷阱来源 💣)  |

### 向量化替代方案 (拒接 Apply) 🚀
| 场景 (Scenario) | ❌ 慢速写法 (The Slow Way)                    | ✅ 向量化写法 (The Fast Way)         | 核心优势                                 |
| :-------------- | :------------------------------------------- | :---------------------------------- | :--------------------------------------- |
| **逻辑判断**    | `df.apply(lambda x: 'A' if x>1 else 'B')`    | `np.where(df['sales']>1, 'A', 'B')` | **100x Faster** (底层 C 语言优化)        |
| **转 0/1 标记** | `df.apply(lambda x: 1 if x>7 else 0)`        | `(df['days']>7).astype(int)`        | **更简洁** (True=1, False=0)             |
| **文本拆分**    | `df['col'].apply(lambda x: x.split(',')[0])` | `df['col'].str.split(',').str[0]`   | 代码更简洁，易读性强                     |
| **时间提取**    | `df['date'].apply(lambda x: x.year)`         | `df['date'].dt.year`                | 专门针对时间序列优化                     |
| **天数差**      | `df.apply(lambda x: (x.end - x.start).days)` | `(df['end'] - df['start']).dt.days` | **直接减** (返回 Int)，类似 SQL datediff |

### Pandas vs SQL 窗口函数速查 (Window Functions) 🪟
*面试高频考题：如何用 Python 实现 SQL 的窗口函数？*

| SQL (Window Function)                       | Pandas (Method)                   | 含义 (Meaning)                                     |
| :------------------------------------------ | :-------------------------------- | :------------------------------------------------- |
| `LAG(col, 1)`                               | `df['col'].shift(1)`              | **错位**：昨天的数平移到今天 (生成 feature 时必用) |
| `LEAD(col, 1)`                              | `df['col'].shift(-1)`             | **反向错位**：明天的数平移到今天 (造 label 时常用) |
| `AVG(col) OVER (ROWS 6 PRECEDING)`          | `df['col'].rolling(7).mean()`     | **滑动平均**：过去7天的均值 (趋势)                 |
| `SUM(col) OVER (PARTITION BY u ORDER BY d)` | `df.groupby('u')['col'].cumsum()` | **累计求和**：以此类推 (cummax, cummin)            |
| `RANK()`                                    | `df['col'].rank()`                | **排名**                                           |
| `DATEDIFF(d2, d1)`                          | `(d2 - d1).dt.days`               | **日期差**                                         |

!!! tip "Pro Tip: Shift(7) vs Rolling(7) 的区别 (面试必问)"

    *   **Shift(7)**: **"7天前的那一天"** (Snapshot)。
        *   *场景*: "上周五的销量"。
        *   *作用*: 捕获 **"周期性" (Seasonality)** (比如周末比周一高)。
    *   **Rolling(7).mean()**: **"过去7天的总平均"** (Summary)。
        *   *场景*: "最近一周的平均热度"。
        *   *作用*: 捕获 **"趋势" (Trend)** (平滑掉噪点，看整体走势)。

---

## 1. Python 原生 (基石)
*掌控了这些，你就掌控了一切。*

### 🗺️ 数据类型全景图 (Data Type Overview)

先搞清楚 Python 里最常见的几种容器的核心区别，后面遇到才不会混淆：

| 类型       | 写法          | 允许重复     | 有序       | 可改     | 查找速度   | 典型用途             |
| :--------- | :------------ | :----------- | :--------- | :------- | :--------- | :------------------- |
| **List**   | `[1, 2, 3]`   | ✅            | ✅          | ✅        | 🐢 逐个找   | 存一组数据、循环遍历 |
| **Set**    | `{1, 2, 3}`   | ❌ 自动去重   | ❌ 无序     | ✅        | 🚀 哈希极快 | 去重、交并差运算     |
| **Dict**   | `{'k': 'v'}`  | Key 不可重复 | ✅ (3.7+)   | ✅        | 🚀 哈希极快 | 键值映射             |
| **Tuple**  | `(1, 2, 3)`   | ✅            | ✅          | ❌ 不可改 | 🐢          | 函数返回多个值       |
| **Series** | `pd.Series()` | ✅            | ✅ (带索引) | ✅        | 🐢          | DataFrame 的一列     |

!!! tip "常见转换链路"

    ```python
    # List → Set (去重)
    set(my_list)

    # List → Series (进入 Pandas 世界)
    pd.Series(my_list)

    # Series → List (离开 Pandas 世界)
    my_series.tolist()

    # DataFrame 取一列 → 自动就是 Series
    df['rating']  # 这就是一个 Series
    ```

### 字符串方法 (String) 🧵

| 方法                 | 作用 (Action) | 示例 (Example)                   | 备注 (Note)                  |
| :------------------- | :------------ | :------------------------------- | :--------------------------- |
| `.strip()`           | 去除首尾空格  | `"  hi  ".strip()` → `"hi"`      | 清洗脏数据最常用             |
| `.split(sep)`        | 拆分字符串    | `"a,b".split(",")` → `['a','b']` | 返回的是列表 List            |
| `.replace(old, new)` | 简单替换      | `"$10".replace("$", "")`         | 不支持正则 (正则用 `re.sub`) |
| `.startswith(x)`     | 检查前缀      | `"https://".startswith("http")`  | 返回布尔值 True/False        |
| `f"{var}"`           | 格式化输出    | `f"Item: {price}"`               | Python 3.6+ 必会神技         |

### 列表方法 (List) 📋

| 方法           | 作用 (Action)     | 区别 (Difference)                     |
| :------------- | :---------------- | :------------------------------------ |
| `.append(x)`   | 追加 **一个元素** | `[1].append([2])` → `[1, [2]]` (嵌套) |
| `.extend(x)`   | 追加 **一堆元素** | `[1].extend([2])` → `[1, 2]` (合并)   |
| `.pop(idx)`    | 弹出并返回        | 默认弹出最后一个，可指定 index        |
| `.sort()`      | **原地排序**      | 修改原列表，返回 None                 |
| `sorted(list)` | **返回新列表**    | 原列表不变，返回排序后的新列表        |

> **List Comprehensions (列表推导式)**: `[x for x in list]` (高级写法，必会)。

### 集合方法 (Set) 🧮
**核心价值**: 去重 + 集合运算（交并差）。在 NLP 分词合并、标签对比时极其常用。

| 需求                | 方法                         | 运算符 | 示例             | SQL 类比                 |
| :------------------ | :--------------------------- | :----- | :--------------- | :----------------------- |
| **合并去重** (并集) | `set.union()`                | `\|`   | `set_a \| set_b` | `UNION`                  |
| **共同元素** (交集) | `set.intersection()`         | `&`    | `set_a & set_b`  | `INNER JOIN`             |
| **差异元素** (差集) | `set.difference()`           | `-`    | `set_a - set_b`  | 左连接取独有             |
| **对称差**          | `set.symmetric_difference()` | `^`    | `set_a ^ set_b`  | `FULL OUTER JOIN` 取独有 |

!!! warning "Set 的两大注意事项"

    1. **无序**：`set` 不保证元素顺序，每次打印可能不一样。不要依赖 `set` 的输出顺序。
    2. **只能装不可变类型**：`set` 里能放 `int`, `str`, `tuple`，但**不能放 `list` 或 `dict`**（因为它们是可变的，无法哈希）。

### 字典方法 (Dictionary)

| 方法 (Method)           | 作用 (Action)       | 示例 (Example)                     |
| :---------------------- | :------------------ | :--------------------------------- |
| `.get(k, default)`      | **安全取值**        | 取不到不报错，返回 None 或默认值   |
| `.items()`              | **遍历键值对**      | `for k, v in d.items():`           |
| `.keys()` / `.values()` | **只看键 / 只看值** | 返回 dict_keys / dict_values 对象  |
| `.update(d2)`           | **合并字典**        | 把 d2 里的东西塞进 d1 (重复键覆盖) |

### Series 速查 (Python → Pandas 的桥梁) 🌉
**Series 本质上就是带索引的 List**，是你从 Python 进入 Pandas 世界后接触到的第一个数据结构。

| 操作       | List 写法           | Series 写法                  | 区别                               |
| :--------- | :------------------ | :--------------------------- | :--------------------------------- |
| 取第一个值 | `lst[0]`            | `s.iloc[0]` 或 `s.values[0]` | Series 有索引，`s[0]` 可能按标签找 |
| 求平均值   | `sum(lst)/len(lst)` | `s.mean()`                   | Series 内置统计方法                |
| 文本操作   | `lst[0].lower()`    | `s.str.lower()`              | Series 用 `.str` 访问器做向量化    |
| 去重       | `list(set(lst))`    | `s.unique()`                 | Series 返回 ndarray                |
| 频次统计   | `Counter(lst)`      | `s.value_counts()`           | Series 直接出排序后的结果          |

!!! tip "什么时候用 List，什么时候用 Series？"

    - **纯 Python 逻辑**（循环、条件判断、拼接字符串）→ 用 **List**
    - **数据分析**（求均值、分组、筛选、画图）→ 用 **Series / DataFrame**
    - **经验法则**：只要你在 Pandas 环境里，就尽量别转回 List，直接用 Series 操作更快更优雅。

### 流程控制 & 内置函数

| 函数 (Func)         | 作用 (Action)      | 核心场景 (Scenario)                     |
| :------------------ | :----------------- | :-------------------------------------- |
| `enumerate(list)`   | **同时拿索引和值** | `for i, val in enumerate(list):`        |
| `zip(list1, list2)` | **拉链遍历**       | `for a, b in zip(names, scores):`       |
| `len()`             | **查长度**         | 查一切 (List, Dict, Str, DF)            |
| `type()`            | **查类型**         | Debug 神器                              |
| `isinstance()`      | **检查类型**       | `if isinstance(x, str):` (比 type 稳健) |
| `any()` / `all()`   | **逻辑聚合**       | 只要有一个True / 全都是True             |
