# 🏗️ 数据工程与管道 (Data Engineering)
*(Coming Soon)*

## 核心模块
*   **SQL Advanced**: Window Functions, CTEs, Optimization.
*   **Pipeline**: Airflow basics.
*   **Data Warehouse**: Kimball Modeling (Star Schema).

## 学习路径
1. SQL 窗口函数高级应用 (RANK, LAG, PARTITION BY)
2. CTE (Common Table Expression) 简化复杂查询
3. 数据仓库建模入门 (事实表 vs 维度表)

---

## 🔥 面试高频：Hive 数据倾斜与性能调优 (Trino 用户的降维打击)

作为主要使用 Trino (Presto) 的分析师，面试中遇到 Hive 调优题可以用以下口径**降维打击**：

> "我在实际工作中主要使用 Trino/Presto。Trino 的 CBO（基于成本的优化器）非常智能，当大表 JOIN 小表时，它在底层会自动选择 Broadcast Join（广播连接），不需要像 Hive 那样手动加 Hint。但在了解底层原理时我知道，Hive 中的 `MAPJOIN` 实质上就是 Broadcast Join，把小表加载到每个 Map 节点的内存中，避免了 Shuffle 阶段，从而根治了由特定 Key 聚集导致的数据倾斜。"

### 数据倾斜常见面试三板斧 (The 3 Hacks for Data Skew)

1. **小表 JOIN 大表 (MAPJOIN / Broadcast Join)**
   - **原理**: `/*+ MAPJOIN(small_table) */` 把小表直接发到 Map 端内存，跳过 Shuffle 阶段。
   - **前提**: 小表必须足够小 (默认 < 25MB)。
2. **空值 (Null) 引发的倾斜**
   - **现象**: 表里有海量 Null，Join 时全部涌入同一个 Reduce 节点导致 OOM。
   - **解法**: 过滤掉不参与 Join 的 Null；或用 `concat('null_', rand())` 给 Null 赋随机后缀打散，因为本来就不会匹配上。
3. **大表 JOIN 大表热点 Key (打盐法 Salting)**
   - **解法**: 将大表侧的热点 Key 加上 `_0` 到 `_9` 的随机后缀分散成 10 份，另一张表对应的数据复制 10 份加上相同后缀，再进行 JOIN。把倾斜压力均摊。
