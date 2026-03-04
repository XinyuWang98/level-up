# 🐼 Pandas (数据分析师的瑞士军刀)
*你 80% 的工作都在这里。*

## I/O & 偷窥数据 (Input/Output & Inspection)

| 方法 (Method)   | 作用 (Action)   | 备注 (Note)                          |
| :-------------- | :-------------- | :----------------------------------- |
| `pd.read_csv()` | **读取**        | `pd.read_excel()` 同理               |
| `df.to_csv()`   | **保存**        | `index=False` (别把索引存进去!)      |
| `df.head()`     | **看前N行**     | 默认5行                              |
| `df.info()`     | **查类型/空值** | 检查 Object vs Float                 |
| `df.describe()` | **宏观统计**    | `include='all'` (看 Unique/Top/Freq) |
| `df.columns`    | **列名列表**    | 方便复制粘贴列名                     |

## 显示设置 (Display Options) 📺

| 问题 (Issue)            | 解决方案 (Solution) | 代码 (Code)                                              |
| :---------------------- | :------------------ | :------------------------------------------------------- |
| **列被折叠** (`...`)    | 全局设置显示所有列  | `pd.set_option('display.max_columns', None)`             |
| **行被折叠**            | 全局设置显示 N 行   | `pd.set_option('display.max_rows', 100)`                 |
| **数字太长** (科学计数) | 设置浮点数格式      | `pd.set_option('display.float_format', '{:.2f}'.format)` |

!!! tip "Jupyter/Notebook 不仅是打印机 (Rich Output)"
    **不要用 `print()`** 打印 DataFrame！
    
    *   **Bad**: `print(df.describe())` → 纯文本，歪歪扭扭，会被 VS Code 截断。
    *   **Good**: `display(df)` 或直接把变量名放在 Cell 最后一行 → **HTML 表格**，支持横向滚动，格式美观。
    *   **Pro**: `df.describe().T` → **转置显示**，专治列太多的情况。

!!! tip "全能数据概览 (The Ultimate Data Profile)"
    **别再分别跑 `df.info()` 和 `df.describe()` 了！**

    用这个函数把它们合体，还能顺便看缺失率 (`missing_ratio`) 和唯一值 (`unique`)。

    ??? example "🐍 get_data_summary() 完整代码"

        ```python
        def get_data_summary(df):
            # 1. 获取 Describe 的转置 (基础统计量)
            # include='all' 确保同时包含数值型和类别型特征
            summary = df.describe(include='all').T
            
            # 2. 手动提取 Info 里的关键信息 (数据类型, 缺失率, 唯一值数量)
            summary['dtype'] = df.dtypes
            summary['missing_ratio'] = df.isnull().mean() # 缺失比例 (比单纯看 count 更有用)
            summary['unique_count'] = df.nunique()      # 唯一值数量
            
            # 3. 调整列的顺序 (把最重要的 Status 放在最前面)
            # 剩下的列 (mean, std, min, max...) 放在后面
            first_cols = ['dtype', 'missing_ratio', 'unique_count', 'count']
            rest_cols = [c for c in summary.columns if c not in first_cols]
            
            # 4. 直接返回 DataFrame 并按 dtype 排序
            return summary[first_cols + rest_cols].sort_values(by='dtype', ascending=False)
        
        # ✅ 使用
        summary_df = get_data_summary(df)
        # 如果需要美化展示，可以在 DataFrame 上调用 style
        summary_df.style.background_gradient(subset=['missing_ratio'], cmap='Reds')
        ```

## 文本型数据专项处理 (Text Processing & Sets) ✂️

在处理各种文本、NLP、或是爬取的脏数据时，熟练掌握文本操作是基本功。

### 1. Python 原生集合运算 (Sets)
**场景**: 标签去重、找出共同标签、找出差异特征。
**核心**: Set 本身就是去重的，而且提供了极快的数学集合运算，远比写 `for loop` 和 `if in` 优雅。

| 需求                | 方法                 | 运算符 | 示例             | SQL 类比     |
| :------------------ | :------------------- | :----- | :--------------- | :----------- |
| **合并去重** (并集) | `set.union()`        | `\|`   | `set_a \| set_b` | `UNION`      |
| **共同元素** (交集) | `set.intersection()` | `&`    | `set_a & set_b`  | `INNER JOIN` |
| **差异元素** (差集) | `set.difference()`   | `-`    | `set_a - set_b`  | 左连接取独有 |

### 2. Pandas 字符串处理 (String Manipulation)
> **记住**: 都要加 `.str` 访问器！

| 方法 (Method)                            | 作用 (Action)  | 示例 (Code)                                     | 坑点 (Gotcha)                                 |
| :--------------------------------------- | :------------- | :---------------------------------------------- | :-------------------------------------------- |
| `.str.lower()` / `.upper()` / `.title()` | **大小写**     | `df['col'].str.title()`                         | 首字母大写用 `.title()`，不是 `.capitalize()` |
| `.str.strip()`                           | **去首尾空格** | `df['col'].str.strip()`                         | 注意中间的空格去不掉                          |
| `.str.contains()`                        | **包含**       | `df['col'].str.contains('keyword', case=False)` | 记得 `na=False` 防止空值报错                  |
| `.str.replace()`                         | **替换**       | `df['col'].str.replace('old', 'new')`           | 默认支持正则，关掉用 `regex=False`            |
| `.str.slice()`                           | **截取**       | `df['col'].str.slice(0, 5)` 或 `.str[:5]`       | **别用 `.len(20)`！** `.len()` 只算长度       |
| `.str.extract()`                         | **正则提取**   | `df['col'].str.extract(r'(\d+)')`               | **必须加括号** `()` 包裹提取内容              |
| `.str.split()`                           | **拆分**       | `df['col'].str.split('_', expand=True)`         | `expand=True` 直接展开为 DataFrame            |
| `.str.cat()`                             | **连接**       | `df['a'].str.cat(df['b'], sep='-')`             | 类似于 Excel 的 `A1 & "-" & B1`               |

### 3. 正则表达式去噪 (Regex Basics)
**场景**: 文本中混杂了标点符号、特殊字符，或是需要提取金额/电话号码。
**核心组合**: `import re` + `re.sub(pattern, replacement, string)`

!!! tip "常用清洗一行流"

    *   **只留中文/英文/数字 (去标点)**: `re.sub(r'[^a-zA-Z0-9\u4e00-\u9fa5]', ' ', text)`
    *   **提取连续数字**: `re.findall(r'\d+', text)`
    *   **搭配 Pandas 用法**: `df['clean'] = df['text'].apply(lambda x: re.sub(r'[^a-zA-Z]', ' ', str(x)))`
    *   **处理两列拼接有 NaN 的问题**: 优雅拼接两列文本，如果其中一列是空值，不用变成全空。 `df['full'] = df[['title', 'body']].apply(lambda x: " ".join(x.dropna().astype(str)), axis=1)`

## 清洗 & 缺失值 (Duplicates & Nulls) 🧼

| 方法                 | 作用 (Action)         | 示例 (Example)                              |
| :------------------- | :-------------------- | :------------------------------------------ |
| `.duplicated()`      | **查重** (返回布尔值) | `df[df.duplicated('uid')]` (查看重复的行)   |
| `.drop_duplicates()` | **去重** (保留一行)   | `df.drop_duplicates('uid', keep='first')`   |
| `.dropna()`          | **扔掉空值**          | `df.dropna(subset=['uid'])`                 |
| `.fillna()`          | **填补空值**          | `df.fillna(0)` 或 `df.fillna(df.mean())`    |
| `.astype()`          | **强制类型转换**      | `df['id'].astype(str)`                      |
| `pd.to_datetime()`   | **转时间**            | `pd.to_datetime(df['date'])`                |
| `pd.to_numeric()`    | **转数字** (容错)     | `pd.to_numeric(df['col'], errors='coerce')` |

!!! tip "缺失值填充的一行流 (One-Liner Imputation)"

    别再分两步写 `mean = ...` 然后 `fillna` 了！
    
    *   **Code**: `df['col'] = df['col'].fillna(df['col'].mean())`
    *   **Logic**: Pandas 会先算括号里的均值，再填进去。清晰、优雅、常用。

!!! tip "全面体检 (Missing Value Audit)"

    *   **看数量**: `df.isnull().sum()` (基础)
    *   **看比例**: `df.isnull().mean()` (Senior 必看! 决定是删行还是删列)
    *   **可视化**: `sns.heatmap(df.isnull(), cbar=False)` (最直观)

!!! warning "日期格式必须精确匹配 (Date Format Gotcha)"
    `pd.to_datetime()` 对格式非常敏感！符号必须一一对应。
    
    *   **数据**: `'31/12/2023'` (斜杠，4位年)
    *   ❌ **%d%m%y**: 找纯数字（`311223`），失败。
    *   ❌ **%d/%m/%y**: 找2位年 (`/23`)，但数据是4位 (`/2023`)，失败。
    *   ✅ **%d/%m/%Y**: `%Y` 匹配 4 位年，`/` 匹配斜杠。完美。
    
    **常用符号**: `%Y`(2024), `%y`(24), `%m`(01-12), `%d`(01-31), `%H:%M:%S`

## 筛选 & 过滤 (Selection) 🔍

!!! warning "选列 vs 算数参数：select_dtypes 还是 numeric_only? 🤯"
    **症状**: 想把所有数值列提取出来，写了 `df.columns(select_dtypes=number)`，或者在切片时用了 `numeric_only=True`，全错！
    
    *   **✅ 场景 1：我要过滤/提取 DataFrame 的列 (基于类型)**
        *   **代码**: `df_num = df.select_dtypes(include='number')`
        *   **只拿列名**: `df.select_dtypes(include='number').columns`
        *   **原理**: `select_dtypes()` 是 DataFrame 的**核心方法**，返回一个新的 DataFrame 子集。
    
    *   **✅ 场景 2：我在算均值/求和，不想让文本列报错**
        *   **代码**: `df.mean(numeric_only=True)`
        *   **原理**: `numeric_only=True` 只是数学聚合函数（如 `mean`, `sum`, `corr`）里的一个**参数**，意思是“遇到非数字列请跳过”，它**不能**用来单独选列！

| 方法       | 全称                 | 语法示例                                | 适用场景                                         |
| :--------- | :------------------- | :-------------------------------------- | :----------------------------------------------- |
| `.loc[]`   | **Loc**ation (Label) | `df.loc[df['age']>18, 'name']`          | **最常用**：按条件筛选 + 按列名取值              |
| `.iloc[]`  | **I**nteger **Loc**  | `df.iloc[:5, 0:2]`                      | **切片**：虽然不知道列名，但我想要前 5 行前 2 列 |
| `.query()` | Query String         | `df.query('age > 18 and city == "NY"')` | **SQL 风格**：代码极度整洁，适合复杂多条件       |
| `.isin()`  | Is In List           | `df[df['id'].isin(target_list)]`        | **名单筛选**：相当于 SQL 的 `WHERE id IN (...)`  |

!!! warning "赋值陷阱: 别把 '问句' 当 '陈述句' (The Boolean Trap)"
    **错误写法**: `df['age'] = df.loc[df['age']>90] == 90` ❌
    
    *   **后果**: `== 90` 返回的是 `True/False`！你把整列 `age` 都变成了布尔值。
    *   **正确写法**: `df.loc[df['age']>90, 'age'] = 90` ✅ (定位到这些行 → 修改为 90)
    *   **或者**: `df['age'] = df['age'].clip(upper=90)` (数值截断，更语义化)

!!! warning "多条件筛选的括号地狱 (Boolean Algebra)"
    **错误写法**: `df[[条件1] & [条件2]]` ❌ (`TypeError`)
    
    *   **原因**: Python 中 `&` 优先级比 `>` 高，且不能对 list 做且运算。
    *   **正确口诀**: **"每个条件包括号，中间用 & 连接"**。
    *   **Code**: `mask = (df['age'] > 30) & (df['age'] < 40) & (df['rating'] == 5)`

!!! tip "Query 魔法: 像写 SQL 一样筛选 (String Magic)"
    如果你讨厌写很多 `df[...]` 和括号，可以用 `query()`！
    
    *   **语法**: 纯字符串，支持 `and`/`or`/`not` (比 `&` `|` `~` 更符合直觉)。
    *   **引用变量**: 使用 `@变量名`。
    
    ```python
    # Bad (括号地狱):
    df[(df['age'] > 30) & (df['dept'] == 'Sales')]
    
    # Good (Query):
    min_age = 30
    df.query("age > @min_age and dept == 'Sales'") 
    ```
    
    **注意**: `query()` 里必须写 **字符串**，不能传 `df['col'] > 0` 这种 Series 进去！

!!! warning "索引对齐陷阱: .loc 取出来是 Series，不是数字 (Scalar Extraction)"
    **症状**: 两个 `.loc[]` 过滤结果相减，得到 `NaN`。

    **原因**: `.loc[]` 返回的是 **Series**（带 index 的包裹 📦），两个 Series 做减法时 Pandas 会**按 index 对齐**。index 不同就对不上 → `NaN`。

    ```python
    # ❌ 错误：两个 Series 的 index 不同，相减得 NaN
    post_val = df.loc[df['Period'] == 'Post', 'effect']   # index=0
    pre_val  = df.loc[df['Period'] == 'Pre', 'effect']    # index=1
    result   = post_val - pre_val  # → NaN (0 对不上 1)

    # ✅ 正确：取出标量值后再运算
    result = post_val.item() - pre_val.item()  # → 纯数字相减
    ```

    **口诀**: 「`.loc` 出来的是 Series，要数字就拆包裹」

    从 Series 中提取单个标量值的 4 种方法：

    | 方法         | 返回类型                    | 安全性         | 适用场景                  |
    | :----------- | :-------------------------- | :------------- | :------------------------ |
    | `.item()`    | Python 原生 (`int`/`float`) | ✅ 多元素时报错 | **推荐**：确定只有 1 个值 |
    | `.values[0]` | NumPy 类型 (`np.int64`)     | ⚠️ 静默取第一个 | 知道可能多行但只要第一个  |
    | `.squeeze()` | Python 原生                 | ✅ 多元素时报错 | 同 `.item()`，语义略不同  |
    | `.iat[0]`    | Python 原生                 | ⚠️ 按位置取     | 性能优先场景              |

    ```python
    s = pd.Series([42])

    s.item()       # → 42 (Python int)
    s.values[0]    # → 42 (numpy.int64)

    # 多元素时的差异：
    s2 = pd.Series([1, 2, 3])
    s2.item()      # ❌ ValueError: can only convert an array of size 1
    s2.values[0]   # → 1 (静默返回第一个，不报错)
    ```

## 变形 & 组合 (Transformation)

| 方法 (Method)      | 作用 (Action) | 核心场景 (Scenario)                    |
| :----------------- | :------------ | :------------------------------------- |
| `df.apply()`       | **万能接口**  | 对每一行/列应用函数 (慢，优先用向量化) |
| `df.replace()`     | **值替换**    | `df.replace({-1: np.nan})`             |
| `df.rename()`      | **列重命名**  | `columns={'old': 'new'}`               |
| `df.sort_values()` | **排序**      | `by='date', ascending=False`           |
| `pd.concat()`      | **堆叠**      | 上下拼接 (Union All)                   |
| `pd.merge()`       | **关联**      | SQL Join (Left/Inner)                  |
| `df.unstack()`     | **长变宽**    | 把索引甩到列名上 (透视)                |
| `df.melt()`        | **宽变长**    | 把多列合并成一列 (逆透视)              |
| `df.explode()`     | **炸裂**      | 把 List 拆成多行 (`[1,2]` → `1`,`2`)   |



## 分段与分桶 (Binning) 🪣

当你需要把连续数值（如消费金额、年龄）变成类别（如高/中/低、老/中/青）时，**千万不要写一堆 `if-else` 或 `apply`**，直接用分桶函数！

| 方法 (Method) | 核心逻辑           | 适用场景                                        |
| :------------ | :----------------- | :---------------------------------------------- |
| `pd.cut()`    | **按绝对数值**切分 | "0-30元，30-70元..." (每组的人数可能差异巨大)   |
| `pd.qcut()`   | **按分位数**切分   | "前25%的人，后25%的人" (每组的**人数必定相等**) |

??? example "🪣 cut & qcut 经典生产力切法"

    ```python
    # 1. pd.cut (业务自定义边界)
    # 比如：把月消费划分成 Low, Medium, High
    bins = [0, 30, 70, 150] # 定义边界 (默认左开右闭: 0 < x <= 30)
    labels = ['Low', 'Medium', 'High']
    df['Charge_Level'] = pd.cut(df['MonthlyCharges'], bins=bins, labels=labels)

    # 2. pd.qcut (等分人群)
    # 比如：把用户按在网时长均分为 4 个群体 (这就是建模/RFM常说的"四分位数分箱")
    df['Tenure_Quartile'] = pd.qcut(df['tenure'], q=4, labels=['Q1', 'Q2', 'Q3', 'Q4'])
    ```

!!! warning "pd.cut 必踩陷阱: 边界值为 NaN ⚠️"
    `pd.cut` 默认区间是**左开右闭** (e.g., `(0, 30]`)。如果你的数据里刚好包含 `0`，而你定义的 `bins=[0, 30...]`，那么 `0` 不在开区间内，它会被偷偷变成 `NaN` 而不报错！
    
    **解法**: 
    1. 给下边界留点安全余量：写成 `bins=[-0.01, 30, 70...]`
    2. 或强行包含左侧极限：代码加上 `include_lowest=True`


## 聚合 & 分组 (Aggregation)

| 方法 (Method)       | 作用 (Action) | 示例 (Code)                                     |
| :------------------ | :------------ | :---------------------------------------------- |
| `df.groupby()`      | **分组核心**  | `df.groupby(['city', 'gender'])`                |
| `.agg()`            | **花式聚合**  | `.agg({'sales': 'sum', 'users': 'nunique'})`    |
| `.transform()`      | **组内变换**  | 返回与原 DataFrame **等长**的 Series (索引对齐) |
| `df.pivot_table()`  | **透视表**    | Excel Pivot Table 的 Python 版                  |
| `df.value_counts()` | **频次统计**  | **最常用！** 相当于 `Select count(*) Group by`  |

!!! tip "GroupBy 高阶聚合 (Named Aggregation)"
    不要只会写 `mean()`！当你需要同时算均值、总和，还得给列改名时：
    
    ```python
    # ❌ 错误写法 (Old School)
    # df.groupby('dept')['age'].agg({'age': 'mean'})
    
    # ✅ 正确写法 (Modern Pandas)
    df.groupby('dept').agg(
        avg_age=('age', 'mean'),
        max_rating=('rating', 'max'),
        user_count=('id', 'nunique')
    )
    ```

### 🛡️ GroupBy Filter (The Security Gate)
`filter` 是 Pandas 中最被低估的函数。它就是一个**"按组安检"**的机制。

*   **输入**: 一个完整的组 (DataFrame)。
*   **逻辑**: 对这**一整组**进行体检 (算平均值、求和、看行数)。
*   **输出**: `True` (整组放行) 或 `False` (整组拦截)。

**场景举例**:
> "找出那些 **(平均分及格)** 的 **(班级)** 的 **(所有学生)**"

```python
# x 代表一个个 "班级" (DataFrame)
# x['score'].mean() >= 60 返回 True/False
df.groupby('class').filter(lambda x: x['score'].mean() >= 60)
```

!!! danger "Filter 的两大禁区"
    1.  **不能插在 df 上**: `df.filter()` 是用来**选列名**的 (正则选列)，跟数据过滤没关系！
    2.  **Lambda 不能返回 Series**: 
        *   ❌ `lambda x: x['score'] > 60` (这是筛选行，应该用 `.loc`)
        *   ✅ `lambda x: x['score'].mean() > 60` (这是筛选组，返回一个 True/False)

### 🔄 GroupBy Transform (The Shape Keeper)
`transform` 是 `groupby` 三大件中最容易被忽视的，但在**特征工程**中几乎必用。

#### agg vs transform vs filter 一图秒懂

| 方法          | 输入               | 输出形状              | 核心用途               |
| :------------ | :----------------- | :-------------------- | :--------------------- |
| **agg**       | 一组 → 一个值      | **缩短** (每组一行)   | 汇总报表 (总和/均值)   |
| **transform** | 一组 → 等长 Series | **不变** (与原表等长) | 组内计算后**写回原表** |
| **filter**    | 一组 → True/False  | **不变或缩短**        | 按组条件筛选           |

#### 🐍 常见用法

??? example "🐍 GroupBy Transform 常见用法"

    ```python
    # 1. 组内占比 (最经典: 每个员工的销售额 / 部门总销售额)
    df['dept_ratio'] = df.groupby('dept')['sales'].transform(
        lambda x: x / x.sum()
    )

    # 2. 组内标准化 (Z-Score: 每个学生在班级内的排名信号)
    df['score_zscore'] = df.groupby('class')['score'].transform(
        lambda x: (x - x.mean()) / x.std()
    )

    # 3. 组内排名 (每个门店内按销量排名)
    df['rank_in_store'] = df.groupby('store')['sales'].transform('rank')

    # 4. 广播组均值 (把组均值写回每一行, 用于对比)
    df['dept_avg'] = df.groupby('dept')['sales'].transform('mean')
    ```

#### 🕐 时序特征工程 (Per-Group Lag/Rolling)

多门店/多分组数据做 Lag/Rolling 时，**必须用 `transform`**，否则 `shift/rolling` 会跨组污染：

```python
# ❌ 跨店污染: shift 后 rolling 丢失了分组边界
df.groupby('store')['sales'].shift(1).rolling(4).mean()

# ✅ Per-Store: transform 保持每个 store 独立计算
df['roll4_mean'] = df.groupby('store')['sales'].transform(
    lambda x: x.shift(1).rolling(4).mean()
)
```

!!! tip "transform 的核心特性: 索引对齐"

    `transform` 返回的 Series **与原 DataFrame 索引完全一致**，所以可以直接赋值为新列，不会出现 NaN 对齐问题。

    这就是它和 `agg` 的本质区别:

    - `agg`: 5000 行 → 10 行 (每组一行)，赋值回去需要 `merge`
    - `transform`: 5000 行 → 5000 行 (每行都有值)，直接 `df['new'] = ...` 即可

## 透视表 (Pivot Table) 🎲
> **降维打击**: 当你还在痛苦地 `groupby` + `unstack` 时，别人已经用 `pivot_table` 下班了。

| 参数 (Arg)   | 含义 (Meaning)    | 示例 (Example)                  |
| :----------- | :---------------- | :------------------------------ |
| `index`      | **行索引** (Left) | `index='Region'`                |
| `columns`    | **列索引** (Top)  | `columns='Category'`            |
| `values`     | **数值** (Center) | `values='Sales'`                |
| `aggfunc`    | **算法**          | `aggfunc='sum'` (默认mean)      |
| `margins`    | **总计**          | `margins=True` (添加 All 行/列) |
| `fill_value` | **填空**          | `fill_value=0` (把 NaN 变成 0)  |

??? example "⚡️ Pivot Table 标准写法"

    ```python
    df.pivot_table(
        index='Region', 
        columns='Category', 
        values='Sales', 
        aggfunc='sum',
        fill_value=0
    )
    ```

!!! tip "多层索引打平 (Flattening MultiIndex)"
    `pivot_table` 产生的结果往往是多层索引 (MultiIndex)，例如 `('sales', 'East')`。这很难看。
    
    **一键打平神技**:
    ```python
    # 1. 列表推导式重命名列 (仅当 columns 是 MultiIndex 时)
    df.columns = [f'{col[0]}_{col[1]}' for col in df.columns]
    
    # 2. 把索引变成列
    df = df.reset_index()
    ```
    
    结果: `region`, `sales_Clothing`, `sales_Electronics`... 清爽！

## Lambda 函数与 Apply (The Power of Any) 🦸‍♂️
当 Pandas 自带函数 (`mean`, `sum`) 不够用时，`apply(lambda x: ...)` 登场。

*   **场景**: "如果评分>3显示Positive，否则Negative"
*   **语法**: `lambda x: <返回值>`
*   **代码**:
    ```python
    df['label'] = df['rating'].apply(lambda x: 'Positive' if x > 3 else 'Negative')
    ```
*   **注意**: 能向量化 (Vectorization) 就别用 apply (for loop)，apply 是最后的手段。

## Pandas 赋值对齐坑 (The Alignment Trap) 🕳️
**症状**: `df['new_col'] = series` 后，发现全变成了 `NaN`。

**原因**: 左边 DataFrame 的 Index 是 `0, 1, 2`，右边 Series 的 Index 是 `'A', 'B', 'C'`。Pandas 找不到对应关系，就填空了。

**✅ 解决方案 (逻辑完美版)**:
```python
# 1. 临时设为索引 (让两边 Index 都是 group 名)
df = df.set_index('group')
# 2. 赋值 (这时 Pandas 就能自动通过 group 名对齐了)
df['new_col'] = group_series
# 3. 恢复索引 (变回 0, 1, 2)
df = df.reset_index()
```

## Pandas 列名重命名 (Renaming Columns) 🏷️
**Method 1: 字典映射 (推荐 - 安全)**
```python
df = df.rename(columns={'old_name': 'new_name', 'sum_revenue': 'revenue'})
```
**Method 2: 暴力覆盖 (快捷)**
```python
df.columns = ['group', 'date', 'revenue', 'users']
```
!!! tip "如何处理长尾数据?"

    *   `np.log1p(x)`: 对数变换，把长尾拉回来 (用于金额/次数)。
    *   `pd.qcut(x, q=10)`: 分箱，把连续值变成类别值 (用于年龄/评分)。
    *   `np.log1p(x)`: 对数变换，把长尾拉回来 (用于金额/次数)。

## 日期时间运算 (Datetime Operations) 📅
> **如果你会 SQL 的 `DATE_ADD` / `DATEDIFF` / `EXTRACT`，那 Pandas 只是换了个写法。**

### SQL ↔ Pandas 速查对照表

| SQL                                | Pandas                           | 示例                |
| :--------------------------------- | :------------------------------- | :------------------ |
| `DATE_ADD(date, INTERVAL 7 DAY)`   | `date + pd.Timedelta(days=7)`    | 往后推 7 天         |
| `DATE_SUB(date, INTERVAL 1 MONTH)` | `date - pd.DateOffset(months=1)` | 往前推 1 个月       |
| `DATEDIFF(date1, date2)`           | `(date1 - date2).dt.days`        | 两个日期差几天      |
| `EXTRACT(YEAR FROM date)`          | `date.dt.year`                   | 提取年份            |
| `EXTRACT(MONTH FROM date)`         | `date.dt.month`                  | 提取月份            |
| `EXTRACT(DOW FROM date)`           | `date.dt.dayofweek`              | 提取星期几 (0=周一) |
| `DATE_TRUNC('month', date)`        | `date.dt.to_period('M')`         | 截断到月            |

### 🔧 pd.Timedelta (时间差 = SQL 的 INTERVAL)

```python
import pandas as pd

# 创建时间差 (3 种等价写法)
delta_7d = pd.Timedelta(days=7)       # 最直观
delta_7d = pd.Timedelta('7 days')     # 字符串写法
delta_7d = pd.Timedelta(weeks=1)      # 用 weeks 也行

# 日期加减 (= SQL DATE_ADD / DATE_SUB)
df['next_week'] = df['date'] + pd.Timedelta(days=7)    # 下周
df['last_week'] = df['date'] - pd.Timedelta(days=7)    # 上周
df['next_month'] = df['date'] + pd.DateOffset(months=1) # 下月 (自动处理月末)

# 两个日期相减 (= SQL DATEDIFF)
df['tenure_days'] = (df['end_date'] - df['start_date']).dt.days  # 差几天
```

!!! important "Timedelta vs DateOffset"

    - `pd.Timedelta(days=30)`: 固定 30 天，不管月份大小
    - `pd.DateOffset(months=1)`: 智能跨月，1月31日 + 1月 = 2月28日

    **经验法则**：天/小时/分钟用 `Timedelta`，月/年用 `DateOffset`。

### 📆 dt 访问器速查 (= SQL EXTRACT)

```python
# 确保是 datetime 类型
df['date'] = pd.to_datetime(df['date'])

# 提取组件 (全都通过 .dt 访问器)
df['year']       = df['date'].dt.year          # 2024
df['month']      = df['date'].dt.month         # 1-12
df['day']        = df['date'].dt.day           # 1-31
df['dayofweek']  = df['date'].dt.dayofweek     # 0=周一, 6=周日
df['dayofyear']  = df['date'].dt.dayofyear     # 1-366
df['weekofyear'] = df['date'].dt.isocalendar().week.astype(int)  # 1-53
df['quarter']    = df['date'].dt.quarter       # 1-4
df['hour']       = df['date'].dt.hour          # 0-23 (有时间才有用)
```

### ✅ 布尔日期属性 (Boolean Date Properties)

```python
# 直接返回 True/False
df['date'].dt.is_month_start   # 是否 1 号
df['date'].dt.is_month_end     # 是否月底
df['date'].dt.is_quarter_start # 是否季度首日
df['date'].dt.is_year_start    # 是否元旦
```

!!! warning "布尔属性对周数据无效"

    `is_month_start` 只检查 "这个日期是不是 1 号"。如果数据都是周五，1 号几乎不会恰好是周五 → 全是 False。

    **周数据的替代写法**：

    ```python
    # 月初周: 日期 <= 7 (即该月第一个周五)
    df['is_month_start_week'] = (df['date'].dt.day <= 7).astype(int)

    # 月末周: 下个周五已跨月
    df['is_month_end_week'] = (
        df['date'].dt.month != (df['date'] + pd.Timedelta(days=7)).dt.month
    ).astype(int)
    ```

## 时间序列三剑客 (Time Series Trio) ⏳
| 方法 (Method)        | 作用 (Action) | 核心场景 (Scenario)                  |
| :------------------- | :------------ | :----------------------------------- |
| `.diff(periods=1)`   | **一阶差分**  | 计算“今日增量” (Day T - Day T-1)     |
| `.shift(periods=1)`  | **滞后一期**  | 获取“昨天的数据” (Lag Feature)       |
| `.rolling(window=7)` | **滚动窗口**  | 计算“过去7天均值” (需配合 `.mean()`) |

!!! tip "告别手动相减 (The .diff() Advantage)"
    **场景**: 计算每日销量变化。
    
    *   **Old School (手动Lag)**: 
        ```python
        df['sales_lag1'] = df['sales'].shift(1)
        df['diff'] = df['sales'] - df['sales_lag1']
        ```
    *   **Modern Pandas (.diff)**: 
        ```python
        df['diff'] = df['sales'].diff(1)
        ```
        **优势**: 代码更短，底层 C 语言优化，速度更快。

!!! warning "防泄露金律 (Anti-Leakage Rule)"
    做预测模型 (Forecasting) 时，计算 Rolling 特征**必须先 Shift**！
    
    *   ❌ `df['sales'].rolling(7).mean()` → 包含了“今天”，**作弊**！
    *   ✅ `df['sales'].shift(1).rolling(7).mean()` → 只看“昨天及以前”，**安全**。
