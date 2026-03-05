---
description: 生成特定学习模块的标准化 Jupyter Notebook。
---

# 生成教学笔记本工作流 (Generate Teaching Notebook)

此工作流强制执行所有教学材料和练习的一致结构。

## 数据集优先级 (Dataset Priority)

**核心原则**: 优先使用真实数据集（通过 Kaggle API），禁止使用模拟数据（除非仅验证语法）。

### 🎯 个性化业务场景数据集检索 (Role-based Dataset Retrieval)

**核心流程**:
1. **读取用户背景**: 分析目标岗位的 JD 或用户的 Gap Analysis，提取核心业务场景（如：金融风控、短视频推荐、本地生活履约、SaaS B2B 增长等）。
2. **Kaggle API 鉴权索取**: 
   - 主动向用户询问：“为了保证代码实战贴合你的专属业务场景，请问你是否有 Kaggle API Token (`kaggle.json`)？如果有，请将内容发送给我，我将为你配置环境自动下载数据集。”
   - 若用户提供，通过 `run_command` 为其配置 `~/.kaggle/kaggle.json`。
   - 若用户无 API 或拒绝提供，则降级使用 `sklearn.datasets` （见下文"备选"）或使用本地已有的样例数据。
3. **通过 API 搜索数据集**:
   - 使用匹配业务场景的关键词调用 Kaggle API 搜索：`kaggle datasets list -s "your business keyword"`
   - 挑选 1-3 个下载量大、质量高的数据集，最终选择一个最贴合的数据集 ID (`<dataset-id>`) 用于本次出题。

### 备选：sklearn 自带数据集 (零下载)
```python
from sklearn.datasets import load_breast_cancer, fetch_california_housing
```

## 步骤

1.  **上下文设置**:
    *   检查 `task.md` 以确定当前的周/模块。
    *   执行上方的**数据集检索流程**获取最匹配的数据集。
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
        *   使用检索到的 Kaggle 或 sklearn 真实数据集，**禁止使用 mock 数据**。
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
