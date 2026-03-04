import nbformat as nbf
import json

nb = nbf.v4.new_notebook()
cells = []

# Workflow Title
cells.append(nbf.v4.new_markdown_cell("# 🧪 模块: Python 数据清洗进阶 — 笔试/面试 20题精选版\n\n本练习遵循标准化教学工作流，专为 Senior DA 笔试/面试拔高设计。涵盖：复杂提取、高级分组、重塑、时序与多条件判别。"))

# Workflow: Module 0
cells.append(nbf.v4.new_markdown_cell("""## 模块 0: 函数加油站 (Function Cheat Sheet)
在我们开始前，先复习一下进阶清洗的核心招式：
- **`str.extract()`**: 正则提取 (需加括号分组)。SQL类比: `REGEXP_EXTRACT()`
- **`.transform()`**: 组内变换，返回与原表等长的数据。SQL类比: 窗口函数 `SUM() OVER(PARTITION BY)`
- **`np.select()`**: 多条件分支判断。SQL类比: `CASE WHEN ... THEN ... END`
- **`.clip()`**: 极值截断，替代繁琐的 if-else 盖帽法。SQL类比: `LEAST(GREATEST(x, min), max)`
- **`.melt()`**: 宽表变长表 (逆透视)。SQL类比: `UNPIVOT`
"""))

# Workflow: Module 1
cells.append(nbf.v4.new_markdown_cell("## 模块 1: 概念映射\n进阶数据处理不仅仅是写代码，更是对数据颗粒度（粒度）的变形。你需要像捏橡皮泥一样熟练地对 DataFrame 聚合 (`agg`)、打散 (`explode`)、拉长 (`melt`)。"))

# Workflow: Module 2
cells.append(nbf.v4.new_markdown_cell("## 模块 2: 数据准备\n*(注: 本节针对具体的高频小场景边界测试（Edge Cases），因此使用精心设计的验证集，以覆盖各种容易引发报错的脏数据格式。)*"))

# Workflow: Module 3
cells.append(nbf.v4.new_markdown_cell("## 模块 3: 分级挑战 (20 个魔鬼细节测试)"))

questions = [
    {
        "title": "### Part 1: 复杂字符串处理 (Advanced String Operations)",
        "q": "**Q1: 提取金额**\n提取文本中的数字并转为 float。注意有 `K` (千) 的情况。\n\n`text = ['Price: $1.2K', 'Just $500', 'Cost is $2.5K', 'Free']`\n\n要求输出: `[1200.0, 500.0, 2500.0, 0.0]`",
        "code": "df = pd.DataFrame({'text': ['Price: $1.2K', 'Just $500', 'Cost is $2.5K', 'Free']})\n# 你的代码\n",
        "ans": "import re\n\ndef parse_money(x):\n    if 'Free' in x:\n        return 0.0\n    num = float(re.search(r'[\\d\\.]+', x).group())\n    if 'K' in x:\n        num *= 1000\n    return num\n\ndf['amount'] = df['text'].apply(parse_money)\nprint(df['amount'].tolist())"
    },
    {
        "q": "**Q2: 提取邮箱后缀 (正则表达式提取)**\n提取所有邮箱的后缀 (例如 `@gmail.com` 提取 `gmail`)。\n\n`emails = ['user@gmail.com', 'admin@163.com', 'test@yahoo.com']`\n\n要求输出: `['gmail', '163', 'yahoo']`",
        "code": "import pandas as pd\ndf = pd.DataFrame({'email': ['user@gmail.com', 'admin@163.com', 'test@yahoo.com']})\n# 你的代码\n",
        "ans": "# 💡 .str.extract 需要配合正则表达式使用，并且必须要有 () 分组\ndf['domain'] = df['email'].str.extract(r'@(.*)\\.com')\nprint(df['domain'].tolist())"
    },
    {
        "q": "**Q3: 拆分姓名列**\n将 `name` 列拆分为 `first_name` 和 `last_name` 两列。\n\n`names = ['John Doe', 'Alice Smith', 'Bob']`\n\n要求: 新增两列，Bob 的 last_name 为 None",
        "code": "df = pd.DataFrame({'name': ['John Doe', 'Alice Smith', 'Bob']})\n# 你的代码\n",
        "ans": "# 💡 expand=True 可以直接把拆分结果变成多列 DataFrame\ndf[['first_name', 'last_name']] = df['name'].str.split(' ', n=1, expand=True)\nprint(df)"
    },
    {
        "title": "### Part 2: 神奇的 GroupBy (Advanced GroupBy)",
        "q": "**Q4: 分组填充空值 (Group-specific Imputation)**\n根据不同城市的平均分，来填充该城市的空值。\n\n要求: BJ 的 NaN 填 80，SH 的 NaN 填 90",
        "code": "import numpy as np\ndf = pd.DataFrame({'city': ['BJ', 'BJ', 'SH', 'SH'], 'score': [80, np.nan, 90, np.nan]})\n# 你的代码\n",
        "ans": "# 💡 transform 绝配！计算每组的均值，并且保持长度和原表一样，直接用 fillna 接收\ndf['score'] = df['score'].fillna(df.groupby('city')['score'].transform('mean'))\nprint(df)"
    },
    {
        "q": "**Q5: 组内占比计算**\n计算每个员工的销售额在所在部门的占比。",
        "code": "df = pd.DataFrame({'dept': ['A', 'A', 'B', 'B'], 'name': ['P1', 'P2', 'P3', 'P4'], 'sales': [100, 300, 200, 200]})\n# 你的代码\n",
        "ans": "# 💡 同样是 transform 广播组总和到每一行\ndf['ratio'] = df['sales'] / df.groupby('dept')['sales'].transform('sum')\nprint(df['ratio'].tolist())"
    },
    {
        "q": "**Q6: 分组过滤 (GroupBy Filter)**\n找出平均分及格 (>=60) 的全体班级成员！(注意是找出成员，不是找出班级)\n\n要求输出: 只保留 class 1 的两行记录",
        "code": "df = pd.DataFrame({'class': [1, 1, 2, 2], 'score': [70, 80, 30, 50]})\n# 你的代码\n",
        "ans": "# 💡 filter 是以组为单位返回 True/False，如果为 False 则扔掉该组所有行\ndf_filtered = df.groupby('class').filter(lambda x: x['score'].mean() >= 60)\nprint(df_filtered)"
    },
    {
        "q": "**Q7: 高阶聚合并重命名 (Named Aggregation)**\n按部门分组，不仅要算平均年龄，还要算最高工资，还要给这两列起好名字 (`avg_age`, `max_salary`)。\n\n要求: 一步写法",
        "code": "df = pd.DataFrame({'dept': ['A','A','B','B'], 'age': [25,35,40,50], 'salary': [5000, 7000, 8000, 10000]})\n# 你的代码\n",
        "ans": "# 💡 Pandas 原生的 Named Aggregation（无需 MultiIndex 打平）\nresult = df.groupby('dept').agg(\n    avg_age=('age', 'mean'),\n    max_salary=('salary', 'max')\n)\nprint(result)"
    },
    {
        "title": "### Part 3: 窗口与序列 (Lag & Rolling)",
        "q": "**Q8: 寻找状态突变**\n找出用户的VIP等级发生变化的行（即今天等级和昨天不一样）。\n\n要求输出: 只提取状态突变的行",
        "code": "df = pd.DataFrame({\n    'uid': [1, 1, 1, 2, 2],\n    'date': ['01-01', '01-02', '01-03', '01-01', '01-02'],\n    'level': ['V1', 'V1', 'V2', 'V1', 'V1']\n})\n# 你的代码\n",
        "ans": "# 💡 利用 shift 获取拉链数据比对，注意一定要加上 groupby('uid')，否则会和上个人的数据比对！\nshifted_level = df.groupby('uid')['level'].shift(1)\ndf['is_changed'] = (df['level'] != shifted_level) & (shifted_level.notna())\nprint(df[df['is_changed']])"
    },
    {
        "q": "**Q9: 组内累计求和 (Cumulative Sum)**\n计算每个用户的累计消费金额（按日期排列）。\n\n要求新增一列 `cum_amount`，对于 uid 1 分别是 100, 150, 170",
        "code": "df = pd.DataFrame({'uid': [1,1,1,2,2], 'amount': [100,50,20,200,100]})\n# 你的代码\n",
        "ans": "# 💡 cumsum 原带原生组内累加特性\ndf['cum_amount'] = df.groupby('uid')['amount'].cumsum()\nprint(df['cum_amount'].tolist())"
    },
    {
        "q": "**Q10: 组内排名计算**\n计算每个班级里，学生按分数的排名（分数高的排第1）。",
        "code": "df = pd.DataFrame({'class': ['A', 'A', 'A', 'B', 'B'], 'score': [90, 80, 95, 70, 80]})\n# 你的代码\n",
        "ans": "# 💡 rank 方法配合 ascending=False\ndf['rank'] = df.groupby('class')['score'].rank(ascending=False, method='min')\nprint(df['rank'].tolist())"
    },
    {
        "title": "### Part 4: 长宽表转换 (Reshaping: Melt & Pivot)",
        "q": "**Q11: 宽表变长表 (Melt)**\n这是典型的 Excel 透视后的宽表，你需要把它逆透视回长表。\n\n要求变成: `Name`, `Subject`, `Score`",
        "code": "df = pd.DataFrame({'Name': ['Tom', 'Jerry'], 'Math': [90, 85], 'English': [80, 95]})\n# 你的代码\n",
        "ans": "# 💡 id_vars 是保留不动的列名，var_name 是你要把旧列名塞进去的新列，value_name 是数值列\nlong_df = df.melt(id_vars='Name', var_name='Subject', value_name='Score')\nprint(long_df)"
    },
    {
        "q": "**Q12: 长表变宽表 (Pivot / Pivot_table)**\n把 Q11 刚才生成的 long_df 再变回宽表！并处理如果有重复数据则取平均值。",
        "code": "long_df = pd.DataFrame({\n    'Name': ['Tom', 'Tom', 'Jerry', 'Jerry', 'Tom'],\n    'Subject': ['Math', 'English', 'Math', 'English', 'Math'],\n    'Score': [90, 80, 85, 95, 100]  # Tom 的 Math 有两次记录 90 和 100\n})\n# 你的代码\n",
        "ans": "# 💡 遇到重复数据必须用 pivot_table (不能用 pivot)，它自带 aggfunc='mean'\nwide_df = long_df.pivot_table(index='Name', columns='Subject', values='Score', aggfunc='mean').reset_index()\nprint(wide_df)"
    },
    {
        "title": "### Part 5: 条件判断与掩码 (Conditionals & Masking)",
        "q": "**Q13: 多条件复杂派生列 (np.select 进阶)**\n根据用户的注册天数 `tenure` 和消费金额 `amount` 划分层级：\n- `tenure > 365` 且 `amount > 1000` -> 'Core'\n- `tenure > 365` 且 `amount <= 1000` -> 'Loyal'\n- `tenure <= 365` 且 `amount > 1000` -> 'Whale'\n- 其他 -> 'Newbie'",
        "code": "df = pd.DataFrame({'tenure': [400, 500, 100, 50], 'amount': [1500, 500, 2000, 100]})\n# 你的代码\n",
        "ans": "import numpy as np\n# 💡 np.select 是处理多维度 if-elif 逻辑的最佳实践\nconds = [\n    (df['tenure']>365) & (df['amount']>1000),\n    (df['tenure']>365) & (df['amount']<=1000),\n    (df['tenure']<=365) & (df['amount']>1000)\n]\nlabels = ['Core', 'Loyal', 'Whale']\ndf['Segment'] = np.select(conds, labels, default='Newbie')\nprint(df['Segment'].tolist())"
    },
    {
        "q": "**Q14: 截断极端值 (Outlier Capping)**\n找出 df['salary'] 的 95% 分位数和 5% 分位数。将大于 95% 分位数的值强行截断为 95% 分位数的值，小于 5% 的同理。\n*(不用 drop，用数值替换)*",
        "code": "df = pd.DataFrame({'salary': [1000, 2000, 3000, 4000, 5000, 6000, 7000, 8000, 9000, 1000000]})\n# 你的代码\n",
        "ans": "# 💡 Pandas 自带 clip 函数，完美解决盖帽法！\nupper = df['salary'].quantile(0.95)\nlower = df['salary'].quantile(0.05)\ndf['salary_capped'] = df['salary'].clip(lower=lower, upper=upper)\nprint(df['salary_capped'].tolist())"
    },
    {
        "title": "### Part 6: 日期专精 (Datetime Hero)",
        "q": "**Q15: 脏日期解析**\n解析带有脏数据的日期，如果解析失败则变为 `NaT` (不要报错！)。",
        "code": "df = pd.DataFrame({'date': ['2023-01-01', '2023-13-45', '2023-01-03']})\n# 你的代码\n",
        "ans": "# 💡 to_datetime 的 errors='coerce' 是保命参数\ndf['date'] = pd.to_datetime(df['date'], errors='coerce')\nprint(df['date'].tolist())"
    },
    {
        "q": "**Q16: 计算两个日期的差集 (天数)**\n计算下单日期 (`order_date`) 到收货日期 (`delivery_date`) 花了几天？",
        "code": "df = pd.DataFrame({'order_date': ['2023-01-01', '2023-01-05'], 'delivery_date': ['2023-01-10', '2023-01-07']})\ndf['order_date'] = pd.to_datetime(df['order_date'])\ndf['delivery_date'] = pd.to_datetime(df['delivery_date'])\n# 你的代码\n",
        "ans": "# 💡 日期相减得到的是 Timedelta 对象，用 .dt.days 提取纯数字\ndf['days_taken'] = (df['delivery_date'] - df['order_date']).dt.days\nprint(df['days_taken'].tolist())"
    },
    {
        "q": "**Q17: 提取月份首末日特征**\n判断这个事件是否发生在每个月的月底？(如果是月底最后一天，返回 True，否则 False)",
        "code": "df = pd.DataFrame({'date': ['2023-01-31', '2023-02-15', '2023-02-28']})\ndf['date'] = pd.to_datetime(df['date'])\n# 你的代码\n",
        "ans": "# 💡 .dt.is_month_end 直接提供这个属性！\ndf['is_month_end'] = df['date'].dt.is_month_end\nprint(df['is_month_end'].tolist())"
    },
    {
        "title": "### Part 7: 结构重组与字典映射 (Remap & Explode)",
        "q": "**Q18: `.map()` 与 `.replace()` 差异对比**\n用一个字典将城市缩写映射为全拼。\n\n若用 `map()` 遇到找不到的词会发生什么？安全的替换怎么写？",
        "code": "df = pd.DataFrame({'city': ['BJ', 'SH', 'GZ']})\nmapping = {'BJ': 'Beijing', 'SH': 'Shanghai'}\n# 分别用 map 和 replace 尝试一下\n",
        "ans": "# 💡 map 会把字典里没有的词变成 NaN！replace 则是维持原样。\nprint('Map 结果 (GZ 变 NaN):\\n', df['city'].map(mapping))\nprint('Replace 结果 (GZ 维持原样):\\n', df['city'].replace(mapping))"
    },
    {
        "q": "**Q19: 把列表炸裂开 (Explode)**\n在处理 JSON 数据时，某个字段是一箩筐标签的列表。你需要把它炸成多行！",
        "code": "df = pd.DataFrame({'uid': [1, 2], 'tags': [['A', 'B'], ['C']]})\n# 你的代码\n",
        "ans": "# 💡 explode 是专门用来把单元格里的 List 展开成多行的神器\ndf_exploded = df.explode('tags')\nprint(df_exploded)"
    },
    {
        "title": "### Part 8: 坑点和盲区 (Gotchas)",
        "q": "**Q20: Loc 对齐导致的 NaN 陷阱**\n你有两个 Series: s1 (索引为 0,1) 和 s2 (索引为 1,2)。你想把他们首尾相加，但不希望有 NaN 传染！",
        "code": "s1 = pd.Series([10, 20], index=[0, 1])\ns2 = pd.Series([100, 200], index=[1, 2])\n# 计算 s1 + s2 试试看，如何让它不会出现 0:NaN 和 2:NaN？\n",
        "ans": "# 💡 s1 + s2 如果 index 不匹配就会变空。使用 .add(fill_value=0) 让缺失一方视为 0！\nresult = s1.add(s2, fill_value=0)\nprint(result)"
    }
]

cells.append(nbf.v4.new_markdown_cell("## 模块 4: 参考答案 (请在独立练习后查看)"))

for item in questions:
    if "title" in item:
        cells.append(nbf.v4.new_markdown_cell(item['title']))
    
    # QUESTION in Markdown cell
    cells.append(nbf.v4.new_markdown_cell(item['q']))
    
    # CODE to practice
    cells.append(nbf.v4.new_code_cell(item['code']))
    
    # ANSWER
    ans_cell = nbf.v4.new_code_cell(f"# ✅ {item['q'].split(':')[0].strip('*')} 参考答案\n{item['ans']}")
    ans_cell.metadata = {"jupyter": {"source_hidden": True}}
    cells.append(ans_cell)

nb['cells'] = cells

with open('41_Python数据清洗基础_笔试专项进阶.ipynb', 'w') as f:
    nbf.write(nb, f)
print("Notebook rebuilt successfully!")
