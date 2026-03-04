# 🎯 模块 E: 分类与模型评估

> 📖 速查手册：[ML 建模](07_ml_models.md) | [评估指标](08_evaluation.md) | [SHAP 解释](09_interpretation.md) | [NLP 文本分析](14_nlp.md)
> 🎯 对应简历项目：**Story 1 — VoC XGBoost 预测转人工意图** | **隐藏武器 — 准时宝 K-Means 分群**

---

## 📺 第一步：看视频建立心智模型

|   #   | 视频                                                                                   | 推荐度 & 食用指北                                                       |  时长  | 看完能理解什么                                             | 状态  |
| :---: | :------------------------------------------------------------------------------------- | :---------------------------------------------------------------------- | :----: | :--------------------------------------------------------- | :---: |
|   1   | [StatQuest: Logistic Regression](https://www.youtube.com/watch?v=yIYKR4sgzI8)          | ⭐⭐⭐⭐ **地基**<br>搞懂 Sigmoid 是怎么把线性映射成概率的。看一遍就行。    | ~15min | Sigmoid 如何把线性输出映射成 0-1 概率                      |   ⬜   |
|   2   | [StatQuest: ROC and AUC](https://www.youtube.com/watch?v=4jRBRDbJemM)                  | ⭐⭐⭐⭐⭐ **重中之重**<br>每个面试官都会问 AUC 代表什么！这里讲得全网最好。 | ~15min | AUC 的本质：模型把正样本排在负样本前面的概率               |   ⬜   |
|   3   | [StatQuest: Regularization (Ridge/Lasso)](https://www.youtube.com/watch?v=Q81RR3yKn30) | ⭐⭐⭐⭐⭐ **高频防坑**<br>L1 稀疏选特征，L2 惩罚防过拟合。必须倒背如流。    | ~20min | L1 产生稀疏解（自动选特征），L2 让权重均匀缩小（防过拟合） |   ⬜   |

---

## 💡 第二步：核心概念卡片

!!! info "Logistic Regression 本质"
    线性回归 $z = w^Tx + b$ 套上 **Sigmoid** 函数 $\sigma(z) = \frac{1}{1+e^{-z}}$，把输出映射到 (0, 1) 区间。
    **权重物理含义**：$w_i$ 大小表示特征 $x_i$ 对预测概率的影响强度；正号=正相关，负号=负相关。
    **面试陷阱**：LR 的 "Regression" 容易被误认为回归模型，本质是分类模型。

!!! info "L1 vs L2 正则化"
    | 维度   | L1 (Lasso)                   | L2 (Ridge)                  |
    | :----- | :--------------------------- | :-------------------------- |
    | 惩罚项 | $\lambda \sum                | w_i                         | $ | $\lambda \sum w_i^2$ |
    | 效果   | 产生**稀疏解**（部分权重=0） | 权重**均匀缩小**（都不为0） |
    | 用途   | 自动**特征选择**             | **防过拟合**                |
    | 类比   | 断臂求生（砍掉没用的特征）   | 集体减薪（所有特征都降权）  |

!!! info "AUC-ROC vs Precision-Recall"
    **AUC-ROC**：适用于正负样本比较均衡的场景（如转人工 vs 不转人工，比例不太极端时）。
    **Precision-Recall**：适用于**正样本极少**的场景（如欺诈检测、罕见疾病）。
    **面试话术**："在我的转人工预测项目中，正负比约 3:7，我选 AUC 作为主指标。如果正负比到 1:100，我会转用 PR-AUC。"

!!! info "K-Fold / Stratified K-Fold / TimeSeriesSplit"
    - **K-Fold**：标准交叉验证，数据随机切 K 份轮流做验证集
    - **Stratified**：保证每份中正负样本比例一致（分类任务优先用这个！）
    - **TimeSeriesSplit**：只允许用过去预测未来（时序专用）

!!! info "SHAP 模型解释"
    回答"为什么他会流失/转人工"：SHAP 把每个特征对单个预测的贡献量化为一个值。
    **红色=推高预测，蓝色=拉低预测**。可以对单个用户画 waterfall 图，也可以对全局画 beeswarm 图找整体规律。

---

## ❓ 第三步：面试巩固题

### 基础题

??? note "Q1: Logistic Regression 的 Sigmoid 如何映射概率？"
    **骨架**：线性输出 z → Sigmoid 映射到 (0,1) → 阈值 0.5 分类 → 权重 wᵢ 表示特征影响强度

??? note "Q2: L1 和 L2 正则化的区别？"
    **骨架**：L1 产生稀疏解（自动选特征）vs L2 均匀缩小权重（防过拟合）。LR 中 `penalty='l1'` 或 `penalty='l2'`

??? note "Q3: AUC-ROC 的含义？什么时候用 PR-AUC？"
    **骨架**：AUC = 模型排序能力（把正样本排前面的概率）→ 正负均衡用 ROC → 正样本极少用 PR-AUC

### 进阶题（来源：模拟面试）

??? warning "Q4: 手写 TF-IDF 计算（不使用 CountVectorizer）🔴"
    **来源**：Gemini 笔试 #3
    ```python
    from collections import Counter
    import math

    def compute_tf(doc_words):
        word_count = Counter(doc_words)
        total = len(doc_words)
        return {w: c / total for w, c in word_count.items()}

    def compute_idf(corpus):
        n_docs = len(corpus)
        idf = {}
        all_words = set(w for doc in corpus for w in doc)
        for word in all_words:
            doc_count = sum(1 for doc in corpus if word in doc)
            idf[word] = math.log(n_docs / (1 + doc_count))
        return idf
    ```

??? warning "Q5: VoC 标注策略——用户没点转人工但骂完走了，算正样本吗？"
    **来源**：Gemini 模拟面试 Q1
    **答法**：多维标注策略 → 不仅看按钮点击，还加入情感极性阈值和 session drop 作为辅助标签 → 标注团队每周校准冲突 case

??? warning "Q6: NLP 模型怎么部署的？QPS 多少？"
    **来源**：Gemini 模拟面试 / Gap Analysis
    **答法**（实事求是）："作为分析师，我负责算法原型验证和容器化 (Docker)。交付 Pickle 文件+推理脚本。高并发部署由 ML Engineer 负责，但我配合做 Latency Check。"

??? warning "Q7: 闭环落地——具体举一个知识库盲区修复的例子？ ⭐"
    **来源**：DeepSeek 模拟面试 Q2
    **答法**：必须讲 STAR 闭环 → 发现问题（退货政策关键词高频命中但满意度低）→ 根因（描述拗口）→ 解决（优化话术）→ 验证（A/B 测试转人工率优化 X%）
