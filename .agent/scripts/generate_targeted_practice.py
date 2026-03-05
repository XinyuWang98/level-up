import nbformat as nbf
import json

nb = nbf.v4.new_notebook()
cells = []

# Title
cells.append(nbf.v4.new_markdown_cell("# 🏋️ 模块: P7 笔试模拟 03 — 盲区专项突击加练\n\n根据上一轮的复盘，你在最后 4 道题（`groupby.filter` / `cut缺失值` / `时间偏移` / `query传参`）卡壳了。\n这一份练习专门为你定制，每种题型提供 2 个变体，确保你彻底吃透底层机制，形成肌肉记忆。"))

questions = [
    {
        "q": "### 1.1 找出活跃度达标的“全团成员” (groupby + filter)\n**业务场景**：一个游戏公会（Guild）里有多个玩家。如果某个公会的**平均活跃天数 >= 10天**，则该公会达标，我们需要提取出该达标公会里的**所有玩家（哪怕有人的活跃度只有 1 天）**。\n*预期结果：只保留 Guild 为 A 的全部 3 名玩家，剔除 Guild B 所有人。*",
        "code": "df_guild = pd.DataFrame({\n    'guild': ['A', 'A', 'A', 'B', 'B'],\n    'player': ['P1', 'P2', 'P3', 'P4', 'P5'],\n    'active_days': [12, 15, 5, 2, 8]\n})\n# 你的代码\n",
        "ans": "# ✅ 参考答案\nres = df_guild.groupby('guild').filter(lambda x: x['active_days'].mean() >= 10)\ndisplay(res)"
    },
    {
        "q": "### 1.2 找出包含“作弊玩家”的整个对局 (groupby + filter) \n**业务场景**：一旦某个对局（Match_ID）中出现任何一个标记为作弊（is_cheat=1）的玩家，我们就要把这个对局里的**所有 10 个人全部拉出来排查**。\n*预期结果：Match_ID 1001 中 P2 作弊，所以 P1和P2 都要被拉出来；1002 没人作弊，全员安全不显示。*",
        "code": "df_match = pd.DataFrame({\n    'match_id': [1001, 1001, 1002, 1002],\n    'player': ['P1', 'P2', 'P3', 'P4'],\n    'is_cheat': [0, 1, 0, 0]\n})\n# 你的代码\n",
        "ans": "# ✅ 参考答案\n# 💡 逻辑：只要组里 is_cheat 的最大值 == 1 (或者 sum > 0)，就说明有人作弊\nres = df_match.groupby('match_id').filter(lambda x: x['is_cheat'].max() == 1)\ndisplay(res)"
    },
    {
        "q": "### 2.1 财务账单分箱的边界陷阱 (pd.cut include_lowest)\n**业务场景**：按照订单金额分类：\n- 0 - 50 元：Low\n- 50 - 100 元：High\n有一个订单恰好是 **0 元** (比如用了白嫖券)，如果不加特定参数，它会变成 NaN。\n请用 `pd.cut` 并确保 0 元订单被正确分入 'Low' 组。",
        "code": "df_order = pd.DataFrame({'amt': [0, 25, 50, 80]})\n# bins 必须是 [0, 50, 100]\n# 你的代码\n",
        "ans": "# ✅ 参考答案\ndf_order['level'] = pd.cut(df_order['amt'], bins=[0, 50, 100], labels=['Low', 'High'], include_lowest=True)\ndisplay(df_order)"
    },
    {
        "q": "### 3.1 跨月订阅到期计算 (DateOffset)\n**业务场景**：用户在 2024年1月31日 购买了 1 个月的会员。\n请算出到期日。注意：如果直接加 30 天，闰年和平年的2月会算错；必须让他智能跳到 2月29日（2024是闰年）。",
        "code": "df_sub = pd.DataFrame({'buy_date': pd.to_datetime(['2024-01-31'])})\n# 你的代码 (使用 pd.DateOffset)\n",
        "ans": "# ✅ 参考答案\ndf_sub['expire_date'] = df_sub['buy_date'] + pd.DateOffset(months=1)\ndisplay(df_sub)"
    },
    {
        "q": "### 4.1 动态名单过滤 (Query + @)\n**业务场景**：找出部门在 `target_departments` 列表中，**并且** 评级等于 `target_level` 的员工。\n请**只用一行 `.query()`** 来完成，不要用传统的 `df[(df...in...) & (df...==...)]`",
        "code": "df_emp = pd.DataFrame({\n    'name': ['A', 'B', 'C', 'D'],\n    'dept': ['Sales', 'Tech', 'HR', 'Tech'],\n    'level': ['P5', 'P6', 'P5', 'P5']\n})\ntarget_departments = ['Tech', 'Sales']\ntarget_level = 'P5'\n\n# 你的代码 (只写一行 query)\n",
        "ans": "# ✅ 参考答案\nres = df_emp.query(\"dept in @target_departments and level == @target_level\")\ndisplay(res)"
    }
]

for i, item in enumerate(questions):
    cells.append(nbf.v4.new_markdown_cell(item['q']))
    cells.append(nbf.v4.new_code_cell("import pandas as pd\nimport numpy as np\n" + item['code']))
    ans_cell = nbf.v4.new_code_cell(item['ans'])
    ans_cell.metadata = {"jupyter": {"source_hidden": True}}
    cells.append(ans_cell)

nb['cells'] = cells

with open('P7笔试模拟_03_Pandas高阶机制专项加练.ipynb', 'w') as f:
    nbf.write(nb, f)
print("Targeted Notebook rebuilt successfully!")
