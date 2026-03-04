# 📊 数据集

> 练习用数据集存放位置

## 📖 说明

本目录存放练习用的小型数据集。大型数据集建议通过 Kaggle API 按需下载，避免仓库过大。

## 📂 当前数据集

| 文件        | 大小 | 来源 | 用途     |
| :---------- | :--- | :--- | :------- |
| `train.csv` | 14B  | 示例 | 占位文件 |

## 🚀 如何下载更多数据集

### 方法 1: Kaggle API（推荐）

```bash
# 安装 Kaggle CLI
pip install kaggle

# 配置 API Key（首次使用需要）
# 从 https://www.kaggle.com/settings 获取 kaggle.json
mkdir -p ~/.kaggle && cp kaggle.json ~/.kaggle/

# 下载数据集示例
kaggle datasets download blastchar/telco-customer-churn --path ./data --unzip
```

### 方法 2: sklearn 自带数据集（零下载）

```python
from sklearn.datasets import load_breast_cancer, fetch_california_housing
```

## 推荐数据集列表

| 场景         | Kaggle Dataset ID                                             | 说明                |
| :----------- | :------------------------------------------------------------ | :------------------ |
| 用户流失预测 | `blastchar/telco-customer-churn`                              | 7K 电信客户，二分类 |
| 电商评论 NLP | `nicapotato/womens-ecommerce-clothing-reviews`                | 23K 条评论          |
| 时序预测     | `rakannimer/air-passengers`                                   | 经典时序数据        |
| 电商用户行为 | `mkechinov/ecommerce-behavior-data-from-multi-category-store` | 用户行为日志        |
