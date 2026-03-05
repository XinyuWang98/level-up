# 📊 数据集

> 练习用数据集存放位置

## 📖 说明

本目录存放练习用的小型数据集或通过 `generate_notebook` workflow 动态下载的实战数据集。
为了保证项目轻量化，大型数据集不在 git 追踪范围内。强烈建议通过 Kaggle API 动态检索并下载。

## 🚀 如何获取练习数据集

本仓库的实战练习（Notebook）倾向于使用真实的业务数据集。目前 Agent 系统已支持**根据你的目标岗位动态检索**最贴合业务场景的顶级数据集。

### 自动化配置 (推荐)
在使用 `/generate_notebook` 时，Agent 会在需要时主动向你索要 Kaggle API Token（即 `kaggle.json` 里的文本）。当你提供后，系统会自动帮你配置好本地鉴权，并静默下载数据至此目录。

### 手动配置 Kaggle API

如果你希望自己纯手动配置：
```bash
# 安装 Kaggle CLI
pip install kaggle

# 配置 API Key（首次使用需要）
# 从 https://www.kaggle.com/settings 获取 API Key，把内容保存到 ~/.kaggle/kaggle.json
mkdir -p ~/.kaggle
# 配置好 json 后赋予权限：
chmod 600 ~/.kaggle/kaggle.json
```

### 降级方案 (零下载)
如果因为网络限制或 API 问题无法使用 Kaggle，所有的练习和笔试题目也可平滑降级，自动采用 `sklearn.datasets` 自带的玩具数据集（如乳腺癌二维分类、加州房价等）进行替代。
