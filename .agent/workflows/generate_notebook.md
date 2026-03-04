---
description: 生成特定学习模块的标准化 Jupyter Notebook。
---

# 生成教学笔记本工作流 (Generate Teaching Notebook)

此工作流强制执行所有教学材料和练习的一致结构。

## 数据集优先级 (Dataset Priority)

**核心原则**: 优先使用真实数据集（通过 Kaggle API），禁止使用模拟数据（除非仅验证语法）。

### 🎯 电商客服场景专用数据集库 (Curated for Resume Stories)

按简历 STAR Story 分类，优先使用以下数据集：

| Story                     | 场景              | Kaggle Dataset ID                                             | 说明                                            |
| :------------------------ | :---------------- | :------------------------------------------------------------ | :---------------------------------------------- |
| **Story 1: 智能客服 VoC** | 文本挖掘/情感分析 | `nicapotato/womens-ecommerce-clothing-reviews`                | 23K 条电商评论，含评分+文本，练 TF-IDF/情感分析 |
|                           | 客服对话分类      | `thoughtvector/customer-support-on-twitter`                   | 推特客服对话，练文本分类/意图识别               |
|                           | 电商评论情感      | `snap/amazon-fine-food-reviews`                               | Amazon 食品评论，500K+ 条，练大规模 NLP         |
| **Story 2: 人力调度**     | 呼叫中心预测      | `kyanyoga/call-center-data`                                   | 呼叫中心记录，含时段/等待时间/处理时长          |
|                           | 时序预测          | `rakannimer/air-passengers`                                   | 经典时序数据，练 Prophet/ARIMA                  |
| **Story 3: 用户流失**     | 客户流失预测      | `blastchar/telco-customer-churn`                              | 7K 电信客户，二分类，练 LightGBM/SHAP           |
|                           | 电商用户行为      | `mkechinov/ecommerce-behavior-data-from-multi-category-store` | 电商用户行为日志，练留存/漏斗/RFM               |
| **通用 ML**               | 二分类基础        | `uciml/breast-cancer-wisconsin-data`                          | sklearn 自带，569 条，快速验证 Pipeline         |

### 备选：sklearn 自带数据集 (零下载)
```python
from sklearn.datasets import load_breast_cancer, fetch_california_housing
```

## 步骤

1.  **上下文设置**:
    *   检查 `task.md` 以确定当前的周/模块。
    *   从上方数据集库中选择最匹配的数据集。
    *   定义文件名，遵循约定：`XX_WeekX_主题_描述.ipynb`（确保 XX 是顺序编号）。

2.  **数据导入 (Kaggle API)**:
    *   第一个代码 Cell 固定为数据下载，**必须使用以下绝对路径调用 kaggle**，以免引发 command not found 错误：
    ```python
    # 数据导入 (Kaggle API)
    # 强制使用绝对路径调用 kaggle
    !kaggle datasets download <dataset-id> --path ./data --unzip -f <filename>.csv
    
    import pandas as pd
    df = pd.read_csv('./data/<filename>.csv')
    df.head()
    ```

3.  **内容生成 (JSON 结构)**:
    *   创建一个有效的 `.ipynb` JSON 结构，包含 `cells`。
    *   **模块 0: 函数加油站 (Function Cheat Sheet)**:
        *   在练习开始前，列出今日核心函数的：
            *   **函数名与大白话解释** (e.g., `dropna`: 删除空行)。
            *   **标准语法与常用参数** (e.g., `subset=['col']`)。
            *   **SQL 类比** (e.g., `WHERE col IS NOT NULL`)。
    *   **模块 1: 概念映射**:
        *   使用 **SQL 类比** 解释概念的 Markdown 单元格。
    *   **模块 2: 数据准备**:
        *   使用 Kaggle 真实数据集（按上方数据集库选择），**禁止使用 mock 数据**。
    *   **模块 3: 分级挑战**:
        *   Level 1: 基础语法（该主题的 "Hello World"）。
        *   Level 2: 业务逻辑（真实世界场景）。
        *   Level 3: 边界情况（处理空值、重复项或复杂逻辑）。
    *   **模块 4: 参考答案**:
        *   带有 `metadata: {"collapsed": true}` 的代码单元格，包含最佳的 "Pythonic" 解决方案。

4.  **验证**:
    *   确保所有 JSON 语法有效（正确转义引号）。
    *   确保 Kaggle 数据集 ID 正确可下载。

5.  **输出**:
    *   使用 `write_to_file` 写入文件。
    *   更新 `task.md`，将新文件链接包含在"学习资料"部分。
