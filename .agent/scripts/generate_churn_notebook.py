import json
import os

# Notebook Content Definition
notebook_content = {
 "cells": [
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "# 🚀 Project: 用户流失预测 Pro (LightGBM + Optuna)\n",
    "\n",
    "> **Senior Data Scientist Mentor**\n",
    "> \n",
    "> *   **Target**: 掌握工业界主流的 GBDT 模型 (LightGBM) 与自动化调参 (Optuna)，并进行可解释性分析 (SHAP)。\n",
    "> *   **Business Context**: 电信运营商希望预测哪些客户可能流失，以便进行挽留。\n",
    "> *   **Dataset**: [Telco Customer Churn](https://www.kaggle.com/datasets/blastchar/telco-customer-churn) (真实业务数据)\n",
    "\n",
    "---\n",
    "\n",
    "## 🛠️ Module 0: Function Cheat Sheet (代码加油站)\n",
    "\n",
    "| 函数/方法 | 大白话解释 | 典型用法 | SQL 类比 |\n",
    "| :--- | :--- | :--- | :--- |\n",
    "| `pd.to_numeric(..., errors='coerce')` | 强行变数字，不听话的变 NaN | `df['col'] = pd.to_numeric(df['col'], errors='coerce')` | `CAST(col AS FLOAT)` |\n",
    "| `LabelEncoder().fit_transform()` | 把“文字”变成“编号” (0, 1, 2) | `le.fit_transform(df['category_col'])` | `DENSE_RANK() OVER (...)` |\n",
    "| `lgb.Dataset(X, y)` | LightGBM 的专属粮仓 (省内存) | `train_data = lgb.Dataset(X, label=y)` | (无) |\n",
    "| `lgb.train(params, ...)` | 开火！训练模型 | `model = lgb.train(params, train_data)` | (无) |\n",
    "| `optuna.create_study()` | 雇佣一个 AI 帮你调参 | `study = optuna.create_study(direction='maximize')` | (无) |\n",
    "| `shap.TreeExplainer(model)` | 模型的翻译官 | `explainer = shap.TreeExplainer(model)` | (无) |"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## 💡 Module 1: Concept Mapping (核心概念)\n",
    "\n",
    "### 1. Label Encoding vs One-Hot Encoding\n",
    "*   **One-Hot (独热编码)**: 像“查户口”。有很多列 (Is_Male? Is_Female?)。**缺点**: 树模型不喜欢太稀疏的矩阵，容易过拟合且慢。\n",
    "*   **Label Encoding (标签编码)**: 像“发学号”。直接给每个类别一个 ID (0, 1, 2)。**优点**: 树模型可以直接处理数字大小关系 (Split)，效率极高。**Senior Choice**。\n",
    "\n",
    "### 2. LightGBM (Leaf-wise Growth)\n",
    "*   **特点**: “唯利是图”。哪个叶子分裂收益大就分裂哪个，不管树均不均衡。**速度快，精度高**。"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": None,
   "metadata": {},
   "outputs": [],
   "source": [
    "# [Init] 数据下载 (Run Once)\n",
    "# !kaggle datasets download blastchar/telco-customer-churn --path ./data --unzip\n",
    "\n",
    "import pandas as pd\n",
    "import numpy as np\n",
    "import matplotlib.pyplot as plt\n",
    "import seaborn as sns\n",
    "import lightgbm as lgb\n",
    "import optuna\n",
    "import shap\n",
    "from sklearn.model_selection import train_test_split\n",
    "from sklearn.metrics import roc_auc_score, accuracy_score\n",
    "from sklearn.preprocessing import LabelEncoder\n",
    "import warnings\n",
    "\n",
    "warnings.filterwarnings('ignore')\n",
    "pd.set_option('display.max_columns', None)\n",
    "plt.rcParams['font.sans-serif'] = ['Arial Unicode MS']\n",
    "\n",
    "# Load Data\n",
    "try:\n",
    "    df = pd.read_csv('./data/WA_Fn-UseC_-Telco-Customer-Churn.csv')\n",
    "    print(\"✅ Data Loaded Successfully\")\n",
    "    display(df.head())\n",
    "except FileNotFoundError:\n",
    "    print(\"❌ 数据文件未找到，请检查路径或运行下载命令！\")"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## ⚔️ Module 2: Data Preparation (数据清洗挑战)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": None,
   "metadata": {},
   "outputs": [],
   "source": [
    "# 🎯 Task 1.1: 数值型清洗\n",
    "# 'TotalCharges' 实际上是 object 类型 (因为含有空格)，请将其转换为 numeric。\n",
    "df_clean = df.copy()\n",
    "\n",
    "# TODO: 使用 pd.to_numeric 处理 TotalCharges\n",
    "# df_clean['TotalCharges'] = ...\n",
    "\n",
    "# TODO: 填充转换后产生的 NaN (建议用均值或中位数)\n",
    "# df_clean['TotalCharges'] = ..."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": None,
   "metadata": {},
   "outputs": [],
   "source": [
    "# 🎯 Task 1.2: 目标列处理\n",
    "# 将 'Churn' (Yes/No) 转换为 1/0\n",
    "\n",
    "# TODO: 使用 map 或 replace\n",
    "# df_clean['Churn'] = ..."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": None,
   "metadata": {},
   "outputs": [],
   "source": [
    "# 🎯 Task 1.3: 类别特征编码 (Label Encoding)\n",
    "# 只有把文字变成数字，LightGBM 才能吃。\n",
    "\n",
    "# 1. 找出所有 object 类型的列 (排除 customerID)\n",
    "cat_cols = [col for col in df_clean.select_dtypes(include='object').columns if col != 'customerID']\n",
    "print(f\"需要编码的特征: {cat_cols}\")\n",
    "\n",
    "# 2. TODO: 循环遍历 cat_cols，对每一列进行 LabelEncoder 转换\n",
    "# le = LabelEncoder()\n",
    "# for col in cat_cols:\n",
    "#     df_clean[col] = ..."
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## ⚔️ Module 3: Modeling & Tuning (模型与调优)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": None,
   "metadata": {},
   "outputs": [],
   "source": [
    "# 🎯 Task 2: 建立 Baseline 模型\n",
    "# 1. 准备 X 和 y (记得 drop 掉 customerID 和 Churn)\n",
    "# 2. 切分 Train/Test (8:2)\n",
    "# 3. 创建 lgb.Dataset\n",
    "# 4. 训练一个最简单的模型\n",
    "\n",
    "# TODO: Write your code here"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": None,
   "metadata": {},
   "outputs": [],
   "source": [
    "# 🎯 Task 3: Optuna 自动调参 (高级)\n",
    "# 定义 objective 函数，让 Optuna 帮你找 num_leaves 和 learning_rate\n",
    "\n",
    "def objective(trial):\n",
    "    # 1. 采样参数\n",
    "    # params = {\n",
    "    #     'num_leaves': trial.suggest_int('num_leaves', 20, 100),\n",
    "    #     'learning_rate': trial.suggest_float('learning_rate', 0.01, 0.1)\n",
    "    # }\n",
    "    \n",
    "    # 2. 训练并返回 AUC\n",
    "    pass\n",
    "\n",
    "# study = optuna.create_study(direction='maximize')\n",
    "# study.optimize(objective, n_trials=20)"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## ⚔️ Module 4: Interpretation (模型解释)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": None,
   "metadata": {},
   "outputs": [],
   "source": [
    "# 🎯 Task 4: SHAP 归因分析\n",
    "# 看看哪些特征最重要\n",
    "\n",
    "# explainer = shap.TreeExplainer(model)\n",
    "# shap_values = explainer.shap_values(X_test)\n",
    "# shap.summary_plot(shap_values[1], X_test)"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {
    "collapsed": True
   },
   "source": [
    "# 🔐 Reference Solution (点击展开参考答案)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": None,
   "metadata": {
    "collapsed": True
   },
   "outputs": [],
   "source": [
    "# --- 完整流程参考 ---\n",
    "\n",
    "# 1. Cleaning\n",
    "df['TotalCharges'] = pd.to_numeric(df['TotalCharges'], errors='coerce').fillna(0)\n",
    "df['Churn'] = df['Churn'].map({'Yes': 1, 'No': 0})\n",
    "\n",
    "le = LabelEncoder()\n",
    "for col in df.columns:\n",
    "    if df[col].dtype == 'object' and col != 'customerID':\n",
    "        df[col] = le.fit_transform(df[col])\n",
    "\n",
    "# 2. Modeling\n",
    "X = df.drop(['customerID', 'Churn'], axis=1)\n",
    "y = df['Churn']\n",
    "X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)\n",
    "\n",
    "dtrain = lgb.Dataset(X_train, label=y_train)\n",
    "dtest = lgb.Dataset(X_test, label=y_test, reference=dtrain)\n",
    "\n",
    "params = {'objective': 'binary', 'metric': 'auc', 'verbosity': -1}\n",
    "model = lgb.train(params, dtrain, num_boost_round=100, valid_sets=[dtest])"
   ]
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.9.6"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 4
}

# Write to file
file_path = "01_专项专栏/02_机器学习/09_Week2_用户流失预测实战_Pro.ipynb"
with open(file_path, 'w', encoding='utf-8') as f:
    json.dump(notebook_content, f, indent=1, ensure_ascii=False)

print(f"Generated standardized notebook at {file_path}")
