import nbformat as nbf
import json

nb = nbf.v4.new_notebook()
cells = []

# Title
cells.append(nbf.v4.new_markdown_cell("# 🧪 模块: P7 笔试模拟 02 — Pandas 高危陷阱与避坑专项\n\n本练习专为查漏补缺设计，题目全部源自你的《03_pandas速查手册》里的 `Warning` 和 `Tip` ⚠️。\n这是一份“故意挖坑”的卷子，看看能不能闭眼避开这些底层机制陷阱！"))

# Workflow: Module 0
cells.append(nbf.v4.new_markdown_cell("""## 模块 0: 函数加油站 (Function Cheat Sheet)
这些是你知识库里明确标记过容易踩坑的方法：
- **`select_dtypes` vs `numeric_only`**: 前者选列，后者聚合计。
- **`.item()`**: 从单元素 Series 中安全提取标量，防止对齐出现 NaN。
- **`.clip()` vs 布尔赋值**: 安全截断极值。
- **`include_lowest=True`**: `pd.cut` 时左开闭区间的保命符。
- **`pd.DateOffset` vs `pd.Timedelta`**: 跨月用 Offset，跨天用 Timedelta。
"""))

# Workflow: Module 1
cells.append(nbf.v4.new_markdown_cell("## 模块 1: 概念映射\nPandas 表面上是表格计算，底层全是向量与索引对齐（Index Alignment）。大部分 NaN 报错都源于左右表/Series 的索引不一致。"))

# Workflow: Module 2
cells.append(nbf.v4.new_markdown_cell("## 模块 2: 数据准备\n*(本节针对语法陷阱验证，使用针对性构造的脏数据集)*"))

# Workflow: Module 3
cells.append(nbf.v4.new_markdown_cell("## 模块 3: 查漏补缺挑战 (10 个必踩陷阱)"))

questions = [
    {
        "q": "### Q1: 选列陷阱 (select_dtypes vs numeric_only)\n你想提取表里的所有数值列，写 `df_num = df(numeric_only=True)` 报错了。请用最标准的方法提取只包含数字的子数据框。",
        "code": "df = pd.DataFrame({'age': [25, 30], 'name': ['Alice', 'Bob'], 'salary': [10000.0, 20000.0]})\n# 你的代码\ndf_num = \n",
        "ans": "# ✅ 参考答案\n# 💡 numeric_only 只能用在 .mean() 这类数学聚合算子内部作为参数，不能用来选列！\ndf_num = df.select_dtypes(include='number')\ndisplay(df_num)"
    },
    {
        "q": "### Q2: 字符串正则包含陷阱 (.str.contains)\n找出所有包含 'apple' 的行。注意这里混入了一个 NaN，如果不处理会报错 `ValueError`。",
        "code": "df = pd.DataFrame({'desc': ['green apple', 'banana', np.nan, 'red Apple']})\n# 你的代码\n",
        "ans": "# ✅ 参考答案\n# 💡 字符串操作碰到空值极易报错，必须加 na=False，忽略大小写加 case=False\ndf_apple = df[df['desc'].str.contains('apple', case=False, na=False)]\ndisplay(df_apple)"
    },
    {
        "q": "### Q3: 布尔赋值陷阱 (The Boolean Trap)\n你想把所有 `age > 90` 的人都强制变成 90 岁。\n新手写了: `df['age'] = df.loc[df['age'] > 90] == 90`。结果整列毁了。\n请写出正确的原地修改代码（或者用更优雅的 clip 函数）。",
        "code": "df = pd.DataFrame({'name': ['A', 'B'], 'age': [20, 100]})\n# 你的代码\n",
        "ans": "# ✅ 参考答案\n# 💡 直接赋值会导致整列变成 True/False\n# 写法1: df.loc[df['age'] > 90, 'age'] = 90\n# 写法2 (更优雅):\ndf['age'] = df['age'].clip(upper=90)\ndisplay(df)"
    },
    {
        "q": "### Q4: 索引对齐导致 NaN 的惨案 (Scalar Extraction)\n你分别筛选出了男生的平均分和女生的平均分，得到了两个单行 Series。\n你想算他们之间的纯数字差值，直接 `post_val - pre_val` 得到了 NaN（因为 index 不一样）。如何提取纯数字？",
        "code": "post_val = pd.Series([85], index=['M'])  # 模拟筛选结果\npre_val  = pd.Series([80], index=['F'])   # 模拟筛选结果\n\n# 你的代码\ndiff = \nprint(diff)",
        "ans": "# ✅ 参考答案\n# 💡 如果用 Pandas Series 直接相减，会按照 Index = 'M' 和 'F' 对齐，对不上就是 NaN。\n# 必须用 .item() 拆开包裹！\ndiff = post_val.item() - pre_val.item()\nprint(diff)"
    },
    {
        "q": "### Q5: 时序特征跨组污染防范 (groupby + shift)\n计算每个用户相对于自己上一单的购买间隔。\n新手写了: `df['date_diff'] = df['date'] - df['date'].shift(1)`。\n但这会把用户 B 的第一单减去用户 A 的最后一单！请修复它。",
        "code": "df = pd.DataFrame({\n    'uid': ['A', 'A', 'B', 'B'],\n    'date': pd.to_datetime(['2023-01-01', '2023-01-05', '2023-01-02', '2023-01-10'])\n})\n# 你的代码\n",
        "ans": "# ✅ 参考答案\n# 💡 遇到多分组时序特征，必须用 groupby + transform 避免跨组污染\ndf['date_diff'] = df['date'] - df.groupby('uid')['date'].transform(lambda x: x.shift(1))\ndisplay(df)"
    },
    {
        "q": "### Q6: 日期格式化地狱 (Datetime format)\n解析英式日期 `'31/12/2023'` (日/月/4位年)。如果只用 `pd.to_datetime()` 可能会搞错月和日。\n请用明确的 `format=` 参数来解析。",
        "code": "df = pd.DataFrame({'date_str': ['31/12/2023', '15/01/2023']})\n# 你的代码\n",
        "ans": "# ✅ 参考答案\n# 💡 %Y 是4位年，%y是2位年；%m是月，%d是天。\ndf['date'] = pd.to_datetime(df['date_str'], format='%d/%m/%Y')\ndisplay(df)"
    },
    {
        "q": "### Q7: GroupBy Filter 的安检机制\n找出那些 **“平均年龄大于 30 岁”的部门** 的 **所有员工记录**。\n注意：不是保留 30岁以上的员工，而是“如果部门均龄>30，整个部门保留”。",
        "code": "df = pd.DataFrame({\n    'dept': ['Tech', 'Tech', 'HR', 'HR'],\n    'name': ['A', 'B', 'C', 'D'],\n    'age': [35, 29, 22, 25] \n})\n# Info: Tech 组均值 32, HR 组均值 23.5\n# 你的代码\n",
        "ans": "# ✅ 参考答案\n# 💡 filter 方法是对“整个组”进行评估并决定是否放行全组行\nres = df.groupby('dept').filter(lambda x: x['age'].mean() > 30)\ndisplay(res)"
    },
    {
        "q": "### Q8: pd.cut 分箱的左侧致命缺失值\n把分数分成 0-60, 60-100。\n新手: `pd.cut(df['score'], bins=[0, 60, 100])`。\n结果得了 0 分的同学（刚好在 0 边界上）被变成了 NaN！如何修复？",
        "code": "df = pd.DataFrame({'score': [0, 50, 60, 100]})\n# 你的代码\n",
        "ans": "# ✅ 参考答案\n# 💡 pd.cut 默认左开右闭 (0, 60]，所以不包含 0。加上 include_lowest=True 保命！\ndf['grade'] = pd.cut(df['score'], bins=[0, 60, 100], include_lowest=True, labels=['Fail', 'Pass'])\ndisplay(df)"
    },
    {
        "q": "### Q9: 月份和天的加法 (DateOffset vs Timedelta)\n给当前日期加上 1 个月，再减去 7 天。\n如果是 1月31日加一个月，必须智能跳到 2月底，不能报错。",
        "code": "df = pd.DataFrame({'date': pd.to_datetime(['2023-01-31'])})\n# 你的代码\n",
        "ans": "# ✅ 参考答案\n# 💡 月/年用 DateOffset(智能跨月)，天用 Timedelta。\ndf['next_date'] = df['date'] + pd.DateOffset(months=1) - pd.Timedelta(days=7)\ndisplay(df)"
    },
    {
        "q": "### Q10: Query 的变量魔法 (String Magic)\n用 `.query()` 找出年龄大于用户输入变量 `min_age` 且 城市在 `target_cities` 列表里的行。",
        "code": "df = pd.DataFrame({'age': [25, 30, 35], 'city': ['BJ', 'SH', 'GZ']})\nmin_age = 28\ntarget_cities = ['BJ', 'SH']\n# 请只使用 .query() 一行代码\n",
        "ans": "# ✅ 参考答案\n# 💡 使用 @ 符号在 query 字符串中引用外部环境变量，代码极度清爽\nres = df.query(\"age > @min_age and city in @target_cities\")\ndisplay(res)"
    }
]

for item in questions:
    cells.append(nbf.v4.new_markdown_cell(item['q']))
    cells.append(nbf.v4.new_code_cell("import pandas as pd\nimport numpy as np\n" + item['code']))
    ans_cell = nbf.v4.new_code_cell(item['ans'])
    ans_cell.metadata = {"jupyter": {"source_hidden": True}}
    cells.append(ans_cell)

# Workflow: Module 4
cells.append(nbf.v4.new_markdown_cell("## 模块 4: 参考答案与复盘\n*以上的每道题都在你的 `03_pandas.md` 知识库有原型，如果错了请随时查阅！*"))

nb['cells'] = cells

with open('P7笔试模拟_02_Pandas底层机制与高阶避坑.ipynb', 'w') as f:
    nbf.write(nb, f)
print("Notebook rebuilt successfully!")
