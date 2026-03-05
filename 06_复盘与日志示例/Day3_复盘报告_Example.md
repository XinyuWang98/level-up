# 📝 Day 3 复盘报告：脏数据清洗与 RFM 实战

## 1. 核心报错复盘 (Error Log)

### 🚨 报错：`ValueError: Length mismatch`
*   **场景**: 试图算出每个用户的 M值 和 F值，存入一个新的 DataFrame。
*   **错误代码**:
    ```python
    rfm_df = {'user_id', 'M_score', 'F_score'}  # ❌ 这是一个集合(Set)，无序且只有一行
    rfm_df = pd.DataFrame(rfm_df)               # ❌ 生成了只有3行的表
    rfm_df['user_id'] = ...                     # ❌ 试图塞入5个用户ID -> 爆炸
    ```
*   **根本原因**: **Excel 思维 vs Pandas 思维**。
    *   Excel 思维：先画好格子（表头），然后一个一个填数。
    *   Pandas 思维：**数据即表**。通过计算直接“生”出表，而不是“填”表。
*   **正确解法 (The Pythonic Way)**:
    ```python
    rfm_df = df.groupby('user_id')['amount'].agg(['sum', 'count']).reset_index()
    ```

## 2. 知识点地图 (Key Takeaways)

### 🧹 清洗三板斧
1.  **`dropna(subset=['...'])`**: 就像 `WHERE col IS NOT NULL`。精准打击，不误伤无辜。
2.  **`drop_duplicates(subset=['...'], keep='last')`**: 就像 `DISTINCT`，但更能控制保留哪一行（比如保留最新的）。
3.  **`astype` vs `to_datetime`**:
    *   普通类型转 `astype(int)`。
    *   复杂时间转 `pd.to_datetime(..., errors='coerce')`。**`errors='coerce'` 是容错的神器**。

### 📊 RFM 模型实现
*   **R (Recency)**: (今天 - 最近购买日期).days
*   **F (Frequency)**: `groupby('user_id')['order_id'].count()`
*   **M (Monetary)**: `groupby('user_id')['amount'].sum()`
*   **打分**: `pd.qcut(..., q=3)` -> 自动按排名切分（前33%，中33%，后33%），而不是拍脑袋定阈值。

## 3. 下一步行动 (Action Plan)
*   [ ] **强化训练**: 您感觉“欠缺练习”，建议进行专门的 **Cleaning Drill (清洗专项训练)**。
*   [ ] **挑战**: 完成 `02++. Week 2 Pandas盲测挑战`，这个挑战不给任何提示，完全模拟真实面试/工作场景。
