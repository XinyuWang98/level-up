# 🌲 模块 C: 树模型与集成学习

> 📖 速查手册：[ML 建模](07_ml_models.md) | [特征工程](06_feature_engineering.md) | [SHAP 解释](09_interpretation.md)
> 🎯 对应简历项目：**Story 1 — 用户行为轨迹 XGBoost 预测流失** | **Story 2 — 调度 XGBoost 残差修正**

---

## 📺 第一步：看视频建立心智模型

|   #   | 视频                                                                       | 推荐度 & 食用指北                                                         |  时长  | 看完能理解什么                                                 | 状态  |
| :---: | :------------------------------------------------------------------------- | :------------------------------------------------------------------------ | :----: | :------------------------------------------------------------- | :---: |
|   1   | [StatQuest: Decision Trees](https://www.youtube.com/watch?v=7VeUPuFGJHk)   | ⭐⭐⭐⭐ **基石必看**<br>极其生动。必须搞懂 Gini 不纯度的直觉（怎么算分裂）。 | ~18min | 树是怎么"分裂"的？Gini vs Entropy 的直觉理解                   |   ⬜   |
|   2   | [StatQuest: Random Forests](https://www.youtube.com/watch?v=J4Wdy0Wc_xQ)   | ⭐⭐⭐⭐⭐ **高频防坑**<br>Bagging 降低方差的经典解释，面试官最爱拿来对比。    | ~10min | Bagging 的本质：多棵弱鸡树投票 → 降低方差（Variance）          |   ⬜   |
|   3   | [StatQuest: XGBoost (Part 1)](https://www.youtube.com/watch?v=OtD8wVaFm6E) | ⭐⭐⭐⭐⭐ **核心武器核心**<br>吃透"后一棵树去拟合前一棵树的残差"这个概念。    | ~25min | Boosting 的本质：每棵新树拟合上一棵树的残差 → 降低偏差（Bias） |   ⬜   |

---

## 💡 第二步：核心概念卡片

!!! info "Decision Tree 分裂原理"
    每个节点选择一个特征和阈值，使得分裂后的两个子集"更纯"。
    **Gini** = 1 - Σ(pᵢ²)，越小越纯。**Entropy** = -Σ(pᵢ·log₂pᵢ)，越小越纯。
    面试时说 Gini 就够了，它是 XGBoost 的默认选择。

!!! info "Bagging vs Boosting（面试最高频题之一！）"
    | 维度       | Bagging (如 Random Forest) | Boosting (如 XGBoost)              |
    | :--------- | :------------------------- | :--------------------------------- |
    | 训练方式   | **并行**，每棵树独立       | **串行**，每棵树修正前一棵树的残差 |
    | 解决的问题 | 降低**方差** (Variance)    | 降低**偏差** (Bias)                |
    | 过拟合风险 | 低（投票平均）             | 高（需要正则化）                   |
    | 类比       | 民主投票（多数决）         | 名师逐层辅导（错题本学习）         |

!!! info "XGBoost 三大改进"
    1. **二阶导数 (Hessian)**：比 GBDT 只用一阶梯度更精准
    2. **正则化 (γ + λ)**：叶子数惩罚 + L2 权重约束 → 防过拟合
    3. **工程优化**：列采样、缺失值处理、并行化

!!! info "防过拟合三板斧"
    `max_depth` ↓ (限制树的复杂度) + `min_child_weight` ↑ (限制叶节点最小样本) + `gamma` ↑ (限制分裂增益阈值) + `reg_lambda` (L2 正则化)

!!! info "特征重要性三重解读"
    不要只看一种指标，三种综合判断：
    1. **Gain**：该特征对模型增益贡献多大
    2. **Cover**：该特征覆盖多少样本
    3. **Permutation**：随机打乱该特征后，模型效果下降多少

---

## ❓ 第三步：面试巩固题

### 基础题

??? note "Q1: XGBoost 相比 GBDT 有哪些改进？"
    **骨架**：二阶导数 + 正则项 + 列采样 + 缺失值处理 + 并行化

??? note "Q2: 如何调参？重点调了哪些参数？"
    **骨架**：RandomizedSearchCV → `max_depth`(复杂度)、`learning_rate`(步长)、`subsample`(防过拟合)、`colsample_bytree`(特征采样)

??? note "Q3: 特征重要性怎么解读？"
    → [查看降维打击回答：难题 3](17_interview_prep.md#hard-flashcards)

### 进阶题（来源：模拟面试）

??? warning "Q4: max_depth=3 vs 15 各有什么风险？怎么防过拟合？"
    **来源**：Antigravity 模拟面试 #3
    **答法**：3=欠拟合（太简单），15=过拟合（记住了噪声）→ 三板斧：max_depth↓ + min_child_weight↑ + gamma↑ + reg_lambda

??? warning "Q5: Feature Importance Top 3 是什么？怎么解释？"
    **来源**：Gemini 模拟面试 Q3
    **答法**：(1) 用户情感极性分 (2) 对话轮次 (3) 未解决意图数。情绪激动+追问多=流失概率最高

??? warning "Q6: 用户行为轨迹 挖掘出 Top 30 痛点，怎么确定优先级？模型有偏差吗？"
    **来源**：DeepSeek 模拟面试 Q1
    **答法**：算法产出 ≠ 最终决策。结合**业务成本**（物流投诉赔付高）和**改进难度**（尺码=供应链问题，短期难改）二次排序
