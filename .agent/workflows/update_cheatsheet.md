---
description: Update the MkDocs knowledge base with new knowledge points, code snippets, or cases.
---

## 前置条件
- MkDocs 知识库位于 `./02_速查手册/`
- 内容文件在 `docs/` 目录下，按主题分类

## 文件索引 (Route Map)
| 主题                     | 目标文件                         |
| :----------------------- | :------------------------------- |
| Python 基础/心法/SOP     | `docs/01_python_basics.md`       |
| NumPy                    | `docs/02_numpy.md`               |
| Pandas                   | `docs/03_pandas.md`              |
| 可视化 Seaborn           | `docs/04_visualization.md`       |
| 假设检验/统计学基础      | `docs/05_statistics.md`          |
| A/B 实验基础             | `docs/05b_ab_testing.md`         |
| A/B 高阶 (CUPED/Delta)   | `docs/05a_ab_advanced.md`        |
| 特征工程/Sklearn         | `docs/06_feature_engineering.md` |
| 数据集拆分               | `docs/06b_data_splitting.md`     |
| 建模 LGB/Cat/Optuna      | `docs/07_ml_models.md`           |
| 评估指标/混淆矩阵        | `docs/08_evaluation.md`          |
| SHAP 模型解释            | `docs/09_interpretation.md`      |
| 模型保存与加载           | `docs/10_deployment.md`          |
| 聚类 K-Means/DBSCAN/PCA  | `docs/11_clustering.md`          |
| 时序预测 Prophet/XGBoost | `docs/12_time_series.md`         |
| 留存/漏斗/RFM            | `docs/13_business_analysis.md`   |
| NLP 文本分析             | `docs/14_nlp.md`                 |
| 因果推断 PSM/DID         | `docs/15_causal_inference.md`    |
| 数据工程 SQL/Pipeline    | `docs/16_data_engineering.md`    |
| 面试准备                 | `docs/17_interview_prep.md`      |

## 执行步骤

1. 根据新知识点的主题，从上表中选择目标文件。
2. 读取该文件当前内容，理解已有结构和风格。
3. 格式化新内容为 Markdown，保持与已有内容一致的风格：
   - 表格用于速查对比
   - 代码块必须有中文注释
   - **Tips/Warnings 用 admonition 格式**（`!!! tip "标题"`），**禁止**使用 blockquote (`> * **`) 包裹列表，否则列表换行符会被吞掉
   - admonition 类型速查：`tip`(建议), `note`(说明), `warning`(注意), `important`(重要)
   - admonition 内部的代码块和列表需要 **4 空格缩进**
   - **admonition 内多段文字必须用空行分隔**：MkDocs 会把连续的缩进行合并成一个段落。如果希望段落之间换行显示（例如"❌ 陷阱"和"✅ 正确答法"分两段），中间**必须**插入一个空行（仅保留 4 空格缩进的空行即可）
   - **列表前必须有空行**：段落文字后紧跟 `*` 或 `1.` 列表时，MkDocs 会把列表吞成行内文本。**必须**在段落和列表之间插入一个空行
   - **粗体标题行后必须有空行**：`**标题**` 独占一行时，下一行如果紧跟描述文字，MkDocs 会合并成一段。**必须**在标题和描述之间插入一个空行
   - **LaTeX 公式独立成段**：使用 `$$ ... $$` 渲染块级数学公式时，公式前后**必须**有空行，且独占一行，否则无法被正确解析。
4. 使用 `replace_file_content` 或 `multi_replace_file_content` 将新内容插入到目标文件的对应章节。
// turbo
5. 重建并重启服务：
   ```bash
   # 先杀掉旧进程，再重新启动（包含 mkdocs serve + Flask 分析服务）
   lsof -ti:8000 -ti:5111 | xargs kill 2>/dev/null
   cd ./02_速查手册 && bash start.sh
   ```
   > ⚠️ **必须重启**：`mkdocs build` 只会更新 `site/` 目录的静态文件，但不会刷新正在运行的 `mkdocs serve` 进程的内存缓存。必须杀掉旧进程并重新启动 `start.sh`，用户才能在浏览器中看到最新内容。
6. 通知用户知识库已更新，告知更新了哪个文件和哪个章节。

## 质量审查 (可选后续)

当本次更新涉及 **3 个以上新知识点** 或用户显式要求优化时，调用 `/review_cheatsheet` workflow 对目标文件执行完整的质量审查。

审查范围：
- **内容**: 是否有对比总表、决策树、面试 Q&A、业务话术
- **格式**: 代码折叠、列表空行、箭头符号、LaTeX 渲染、章节编号
- **Mermaid**: 节点标签、颜色规范

详见 [review_cheatsheet.md](file://./.agent/workflows/review_cheatsheet.md)。
