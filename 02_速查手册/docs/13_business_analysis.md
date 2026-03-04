# 💰 高级商业分析 (Advanced Business Analysis)

## 留存率计算：宽松 vs 严格 (Retention) 📉

| 类型                   | 定义 (Definition)                 | 场景 (Scenario)                       | 核心代码 (Key Code)                         |
| :--------------------- | :-------------------------------- | :------------------------------------ | :------------------------------------------ |
| **宽松留存** (Rolling) | 只要第 N 天**后**出现过，就算留存 | **社区/内容App** (很久不来，回来也算) | `groupby('uid')['date'].max()`              |
| **严格留存** (Strict)  | 必须**第 N 天当天**回来才算       | **游戏/打卡App** (断签一天就不算了)   | `pivot_table` 或 `groupby(['uid', 'diff'])` |

### 🐍 严格留存通用模板 (Strict Retention Code):

```python
# 1. 算出天数差
df['diff'] = (df['login_date'] - df['signup_date']).dt.days

# 2. 关键：把 (uid, diff) 变成唯一键，看是否有记录
# 🌟 三步心法 (Mantra):
#   1. Group: df.groupby(...) -> 只是分了组，还没数数
#   2. Size:  .size()         -> 每个人每天有几条? (变成长表)
#   3. Unstack: .unstack()    -> 把天数横过来 (变成宽表)
retention = df.groupby(['user_id', 'diff']).size().unstack(fill_value=0)

# retention 变成了一个矩阵：
# diff      1    3    7
# user_id
# 1001      1    0    1  (第3天没来，第7天回来了)
# 1002      0    0    0  (流失)

# 3. 统计第 N 天留存率
d7_retention_rate = retention[7].mean() # 1=留存, 0=流失，均值即留存率
```

## 用户价值模型 (LTV / RFM)
*(Coming Soon)*

*   **RFM**: Recency, Frequency, Monetary based segmentation.
*   **LTV**: Linear Regression or BDG/NBD models.
