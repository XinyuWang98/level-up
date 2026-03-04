
# 📊 Senior Data Analyst Gap Analysis (Level: 某新能源车企T公司/某短视频大厂B公司/Meta)

**目标岗位**: Senior/Expert Data Analyst (E-commerce/Operations) - 阿里/美团/京东
**关键策略**: 经验嫁接 (Experience Grafting) - 客服 -> 智能运营
**当前阶段**: W2: Advanced ML & Causal Inference
**最近更新**: 2026-02-15 (知识图谱自评 + 缺口填补)

---

## 🎯 核心能力矩阵 (Detailed Skill Matrix)

### 1. 业务洞察与高级分析 (Business Insights & Advanced Analytics)
*   **核心逻辑**: 不止是看 dashboard，而是能预测未来 (Predictive) 和归因过去 (Attribution)。
*   **JD 关键词**: "Identify trends/inefficiencies", "Root cause analysis", "Operational efficiency" (某新能源车企T公司), "Fraud/Risk" (某短视频大厂B公司).

| 细分领域 (Sub-Domain)                  | 关键技术点 (Key Skills)   | Senior 标准 (Target) 🚀                             | 当前状态 (Current State) 📍 | 差距分析 (Gap Analysis) 📉                    |
| :------------------------------------- | :------------------------ | :------------------------------------------------- | :------------------------- | :------------------------------------------- |
| **用户生命周期**<br>(User Lifecycle)   | **LTV & Churn**           | 构建 LTV 预测模型 (bg/nbd) & 流失预警 (XGBoost)    | **B级 (XGBoost实战)** ✅    | **[+ Plus]** 已掌握 Churn 预测               |
|                                        | **User Segmentation**     | 高阶聚类 (K-Means/DBSCAN) 用于精细化运营           | **B级 (RFM实战过)** ⚠️      | **[- Gap]** 缺乏高维聚类经验                 |
| **风控与运营**<br>(Risk & Ops)         | **Fraud Detection**       | 识别异常行为 (Anomaly Detection) - *某短视频大厂B公司重点* | **D级 (未接触)** ❌         | **[- Gap]** 需了解 Isolation Forest          |
|                                        | **Supply Chain/Ops**      | 供应链/产能效率分析 - *某新能源车企T公司重点*                  | **D级 (未接触)** ❌         | **[- Gap]** 需补充运筹优化概念               |
| **营销科学**<br>(Marketing Science)    | **Uplift Modeling**       | 区分 "Persuadables" (因果森林) - *Meta重点*        | **D级 (未接触)** ❌         | **[- Gap]** 高阶难点 (Optional)              |
|                                        | **Attribution**           | MTA (多触点归因), Markov Chain                     | **C级 (理论了解)** ⚠️       | **[- Gap]** 缺乏代码实战                     |
| **✨ 内容与增长**<br>(Content & Growth) | **Content Understanding** | 文本挖掘 (NLP), 推荐逻辑 (User-Item Matrix)        | **D级 (未接触)** ❌         | **[- Gap]** [🤖 DeepSeek] 字节/小红书 P0 技能 |

### 2. 因果推断 (Causal Inference)
*   **核心逻辑**: 当无法做 A/B Test 时，如何证明因果性？
*   **JD 关键词**: "Causal inference", "Quasi-experiments".

| 细分领域 (Sub-Domain) | 关键技术点 (Key Skills) | Senior 标准 (Target) 🚀                          | 当前状态 (Current State) 📍 | 差距分析 (Gap Analysis) 📉               |
| :-------------------- | :---------------------- | :---------------------------------------------- | :------------------------- | :-------------------------------------- |
| **✨ 准实验设计**      | **PSM / DID**           | 解决 Selection Bias, 政策评估 (Parallel Trends) | **S级 (精通)** ✅           | **[Done]** 掌握稳健性/安慰剂检验        |
|                       | **SCM**                 | 合成控制法 (宏观实体层面)                       | **B级 (理论了解)** ✅       | **[+ Plus]** 能区分 PSM vs SCM 适用场景 |
|                       | **RDD / IV**            | 断点回归 / 工具变量法                           | **D级 (未接触)** ❌         | **[- Gap]** 学术派但在大厂偶有需要      |
| **✨ 框架**            | **CausalML / DoWhy**    | 熟练使用 Microsoft DoWhy 库建模                 | **B级 (实战过)** ✅         | **[Done]** 熟练使用 Refutation Tests    |

### 3. 实验科学 (Experimentation / A/B Testing)
*   **核心逻辑**: 科学量化收益，拒绝玄学。
*   **JD 关键词**: "Experimental design", "Statistically rigorous", "A/B testing".

| 细分领域 (Sub-Domain) | 关键技术点 (Key Skills) | Senior 标准 (Target) 🚀                          | 当前状态 (Current State) 📍 | 差距分析 (Gap Analysis) 📉      |
| :-------------------- | :---------------------- | :---------------------------------------------- | :------------------------- | :----------------------------- |
| **设计与诊断**        | **MDE / SRM / AA**      | 样本量计算, 样本比率偏差诊断                    | **A级 (熟练)** ✅           | **[+ Plus]** 意识极强          |
| **检验方法**          | **Stat Tests**          | T-test, Chi-square, Mann-Whitney, Bootstrap     | **S级 (精通)** ✅           | **[+ Plus]** 基础极其牢固      |
| **✨ 高阶技巧**        | **CUPED**               | 方差缩减 (Variance Reduction) - *Meta/Uber标配* | **S级 (精通)** ✅           | **[Done]** 掌握五步稳健性检验  |
|                       | **Delta Method**        | Ratio 指标方差估计 (CTR/CVR)                    | **S级 (精通)** ✅           | **[Done]** 手写泰勒展开方差    |
|                       | **Sequential Testing**  | 序贯检验与 Alpha Spending (应对 Peeking)        | **A级 (熟练)** ✅           | **[Done]** DTD vs LTD 双轨监控 |
|                       | **Simpson's Paradox**   | 识别分组悖论陷阱                                | **S级 (Case 8)** ✅         | **[Done]** 已完全攻克          |

### 4. 数据工程与管道 (Data Engineering & Pipeline)
*   **核心逻辑**: 不仅仅当个"取数机"，要有 Build 的能力。
*   **JD 关键词**: "Data pipelines", "Tableau", "Airflow", "Spark/Hive", "Automation".

| 细分领域 (Sub-Domain) | 关键技术点 (Key Skills) | Senior 标准 (Target) 🚀           | 当前状态 (Current State) 📍 | 差距分析 (Gap Analysis) 📉                 |
| :-------------------- | :---------------------- | :------------------------------- | :------------------------- | :---------------------------------------- |
| **✨ Pipeline**        | **Airflow / dbt**       | 自动化任务调度与数仓建模         | **B级 (实战过)** ✅         | **[+ Plus]** 搭建实时数据监控 Pipeline    |
| **✨ 工程化**          | **Modular Coding**      | 把 Analysis 封装成 Class/Library | **B级 (LiuliX)** ✅         | **[+ Plus]** DuckDB-WASM 浏览器端工程能力 |
| **可视化**            | **Tableau / Superset**  | 搭建 Self-serve Dashboard        | **B级 (Seaborn强)** ⚠️      | **[- Gap]** 需了解 BI 工具逻辑            |

### 5. 机器学习与预测模型 (Machine Learning & Predictive Modeling) 🤖
*   **核心逻辑**: Senior DA 不造轮子 (Algorithm Dev)，而是用轮子 (Application) 解决商业问题。
*   **JD 关键词**: "Predictive modeling", "Scikit-learn", "Forecasting", "Clustering", "XGBoost".
*   **边界定义**:
    *   **✅ DA Must Do**: 解释特征 (Feature Importance)、产出策略 (Actionable Insights)、快速原型 (Prototyping)。
    *   **❌ MLE Must Do**: 毫秒级延迟优化 (Latency)、大规模分布式训练 (Distributed Training)、深度学习架构设计 (Transformer/CNN)。

| 细分领域 (Sub-Domain)       | 关键技术点 (Key Skills)     | Senior 标准 (Target) 🚀                        | 当前状态 (Current State) 📍 | 差距分析 (Gap Analysis) 📉                           |
| :-------------------------- | :-------------------------- | :-------------------------------------------- | :------------------------- | :-------------------------------------------------- |
| **监督学习**                | **Classification**          | 熟练使用 **RF / XGBoost / LightGBM** 预测流失 | **A级 (XGBoost/RF实战)** ✅ | **[+ Plus]** [🤖 DeepSeek] 需补充 LightGBM/CatBoost  |
|                             | **Regression**              | 房价/LTV 预测 (Linear/Tree Models)            | **A级 (房价实战)** ✅       | **[Done]** 掌握了 Linearity Trap                    |
|                             | **Time Series**             | 销量预测 (Prophet / ARIMA / XGBoost)          | **B级 (实战过)** ✅         | **[Done]** 掌握了差分(Differencing)与回测(Backtest) |
| **非监督学习**              | **Clustering**              | K-Means / DBSCAN / **PCA** 降维               | **A级 (One-Hot修复)** ✅    | **[- Gap]** 缺 DBSCAN (异常检测) & PCA              |
| **模型解释与评估**          | **SHAP / AUC-ROC**          | **(核心)** 用 SHAP 解释"为什么他会流失"       | **A级 (SHAP实战)** ✅       | **[+ Plus]** 能够解释复杂模型                       |
| **特征工程**                | **Feature Eng**             | 高价值特征构造, One-hot, Target Encoding      | **A级 (实战过)** ✅         | **[+ Plus]** Time Series Difference                 |
| **✨ 非结构化数据**          | **VoC Analysis (NLP Lite)** | **(差异化)** 用 TF-IDF/词云 量化客户原声      | **B级 (实战过)** ✅         | **[+ Plus]** 懂业务场景比懂算法更重要               |
| **✨ 模型工程**              | **Auto-Tuning**             | Optuna 自动调参, Pipeline 封装                | **D级 (未接触)** ❌         | **[- Gap]** [🤖 DeepSeek] Senior 必备技能            |
| **未来扩展 (Nice-to-Have)** | **Deep Learning / KNN**     | 处理非结构化数据 (NLP/CV) 或 简单填补缺失值   | **D级 (未接触)** ❌         | **[Optional]** Senior DA 暂不需要，MLE 必备         |

### 6. 影响力与软技能 (Influence & Leadership)
*   **核心逻辑**: 能驱动业务决策，Mentor 初级分析师。
*   **JD 关键词**: "Storytelling", "Mentoring", "Cross-functional collaboration".

| 细分领域 (Sub-Domain) | 关键技术点 (Key Skills) | Senior 标准 (Target) 🚀           | 当前状态 (Current State) 📍 | 差距分析 (Gap Analysis) 📉              |
| :-------------------- | :---------------------- | :------------------------------- | :------------------------- | :------------------------------------- |
| **影响力**            | **Storytelling**        | 能把复杂的统计结果讲给 PM/CEO 听 | **A级 (天赋)** ✅           | **[+ Plus]** 解释 concept 很清晰       |
|                       | **Mentoring**           | 能指导 Junior Analyst 避坑       | **C级 (入门)** ⚠️           | **[+ New]** 开始关注 Data Leakage 教学 |

### 7. 面试准备与代码自信 (Interview Prep & Coding Confidence) 🎯
*   **核心痛点**: "离开 Cheat Sheet 就不会写代码" (Imposter Syndrome).
*   **面试真相**: 面试官不考背诵 API 参数 (那是 IDE 的事)，考的是 **Workflow** 和 **伪代码 (Pseudo-code)**。

| 细分领域 (Sub-Domain) | 关键技术点 (Key Skills)  | Senior 标准 (Target) 🚀                  | 当前状态 (Current State) 📍 | 差距分析 (Gap Analysis) 📉            |
| :-------------------- | :----------------------- | :-------------------------------------- | :------------------------- | :----------------------------------- |
| **白板编程**          | **Workflow Memory**      | 能手写出完整 ML 流程 (Import->Fit)      | **C级 (依赖文档)** ⚠️       | **[- Gap]** 需刻意练习"默写"         |
|                       | **Code Snippets**        | 常用的一行流 (One-liners)               | **B级 (有点印象)** ⚠️       | **[- Gap]** 需整理成 Anki 卡片       |
| **算法题**            | **LeetCode SQL**         | Medium/Hard 难度秒杀                    | **A级 (SQL强)** ✅          | **[+ Plus]** 保持手感                |
|                       | **Python Easy**          | 基础的数据处理 (Pandas/List)            | **B级 (Notebook流)** ⚠️     | **[- Gap]** 需脱离提示环境练习       |
| **面试陷阱**          | **Data Leakage (Scale)** | Split 必须在 Standardize 之前 (Peeking) | **A级 (实战过)** ✅         | **[Done]** Time Series Lag Leakage   |
|                       | **Target Leakage**       | 训练特征里绝不能包含 Y (Cheating)       | **A级 (实战过)** ✅         | **[Done]** 也就是之前的 K-Means 事故 |

### 8. 理论进阶与学习资源 (Theoretical Foundation & Resources) 🎓
*   **核心逻辑**: 如果说代码是把刀，理论就是内功。**Senior 的区别在于能不能解释 "Why"**。
*   **学习策略**: 先 Hands-on (写代码)，遇到瓶颈再看 theory (看视频)，效率最高。

| 领域 (Domain)        | 核心理论点 (Key Concepts)                       | 推荐资源 (Recommended Resources)                                                                                                                                                                                                                                                                                   | 优先级 (Priority)   |
| :------------------- | :---------------------------------------------- | :----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :------------------ |
| **Machine Learning** | **Bias vs Variance**<br>(偏差与方差权衡)        | **[StatQuest](https://www.youtube.com/watch?v=EuBBz3bI-aA)** (神级! 必看)<br>**[李宏毅 ML 2021](https://www.youtube.com/watch?v=CXgbekl66jc)** (Lecture 2: Where does error come from?)<br>**[Andrew Ng](https://www.youtube.com/playlist?list=PLkD32wF2cM1jI4-5H_rZ_Jg-k_Jg_Jg_J)** (Diagnosing Bias vs Variance) | **🚨 P0 (面试必问)** |
|                      | **Ensemble Learning**<br>(Bagging vs Boosting)  | **[StatQuest - Random Forests](https://www.youtube.com/watch?v=J4Wdy0Wc_xQ)**<br>**[StatQuest - XGBoost](https://www.youtube.com/watch?v=OtD8wVaFm6E)** (了解残差拟合原理)                                                                                                                                         | **P1**              |
|                      | **Support Vector Machines**<br>(SVM - Optional) | **[StatQuest - SVM](https://www.youtube.com/watch?v=efR1C6CvhmE)** (面试偶尔会问核函数 Kernel Trick)                                                                                                                                                                                                               | P2                  |
| **Statistics & A/B** | **Central Limit Theorem**<br>(中心极限定理)     | **[3Blue1Brown - CLT](https://www.youtube.com/watch?v=zeJD6dqJ5lo)** (最直观的数学动画)<br>理解为什么样本量大了就可以用正态分布近似。                                                                                                                                                                              | **P0**              |
|                      | **P-Value & Hypothesis**<br>(P值与假设检验)     | **[StatQuest - P Values](https://www.youtube.com/watch?v=5Dnw46eC-0o)**<br>彻底搞懂 "Reject the Null Hypothesis" 到底是什么意思。                                                                                                                                                                                  | **P1**              |
| **Causal Inference** | **Confounders**<br>(混淆变量)                   | **[CrashCourse - Statistics](https://www.youtube.com/watch?v=zxWgCgyv4Z8&list=PL8dPuuaLjXtNM_Y-bUAhblSAdWRnmBUcr)**<br>**[Causal Inference 101](https://www.youtube.com/watch?v=OdWffvD8m3g)** (Introduction to Potential Outcomes)                                                                                | P2 (Senior加分项)   |

### 🎯 面试必考题库 (Interview Q&A)
*针对 "VoC + Causal" 差异化简历的定制题库*

#### 1. VoC / NLP 挖掘类 (The Differentiator) 🗣️
| 常见问题 (Questions)                        | 核心考点 (Key Concepts)             | 推荐资源 (YouTube) 📺                                                                                   |
| :------------------------------------------ | :---------------------------------- | :----------------------------------------------------------------------------------------------------- |
| **"你是如何从海量文本中提取 Top 痛点的？"** | **TF-IDF, Stopwords, N-grams**      | [StatQuest: TF-IDF Explained](https://www.youtube.com/watch?v=4vT4fu4tC3M) (必看! 5分钟搞懂原理)       |
| **"XGBoost 如何处理文本特征？"**            | **Vectorization (Sparse Matrix)**   | [StatQuest: XGBoost Part 1](https://www.youtube.com/watch?v=OtD8wVaFm6E) (了解树模型基本原理)          |
| **"LDA 主题模型是如何工作的？"**            | **Unsupervised Learning, Clusters** | [StatQuest: PCA Main Ideas](https://www.youtube.com/watch?v=HMOI_lkzW08) (虽然不是LDA，但降维思想互通) |

#### 2. 因果推断 & A/B 测试 (The Money Maker) 💰
| 常见问题 (Questions)                 | 核心考点 (Key Concepts)                | 推荐资源 (YouTube) 📺                                                                              |
| :----------------------------------- | :------------------------------------- | :------------------------------------------------------------------------------------------------ |
| **"实验组样本量不足怎么办？"**       | **Variance Reduction, Power Analysis** | [A/B Testing Interview Questions](https://www.youtube.com/watch?v=3y9GZ_kQeAw) (ExpPlatform 实战) |
| **"做 PSM 时最重要的假设是什么？"**  | **Confounders (混淆变量)**             | [Causal Inference: The Mixtape](https://www.youtube.com/watch?v=OdWffvD8m3g) (Brady Neal Intro)   |
| **"P-value 0.04 和 0.001 的区别？"** | **Statistical Significance**           | [StatQuest: P-values, clearly explained](https://www.youtube.com/watch?v=5Dnw46eC-0o) (解释神作)  |

#### 2.5: [🔥 A/B 测试亮点追加] 面试高阶防守 (P7 平台建设者视角)
*   **Q**: "搭建完实验平台后，你觉得最大的痛点是什么？如果让你重新规划，你会在哪里投入更多精力？"
*   **Defense Strategy (从"算数据"到"建体系"的跨越 - 极度契合 Senior 核心价值观)**:
    *   **✅ 话术 (请背熟)**: "这是我在推行实验平台 0-1 落地时最有痛感的一点。前期我把大量精力投入在了降低实验误差（Delta Method / CUPED）和加速决策（mSPRT 贯序检验）上，**但随着平台上线，我发现光有强大的统计引擎是不够的，还需要配套强大的‘归因体系’**。
    *   "一个典型的现象是：产品经理看到 p-value < 0.05 且是正向收益，就会沾沾自喜要求全量；而一旦实验失败，他们立刻陷入盲区，不知道接下来该怎么改。也就是说，**快速的实验加速了‘What（好不好）’的决策，但因为缺乏事中多维下钻和归因机制，加剧了‘Why（为什么好/不好）’的解答难度。**
    *   "所以在近期的复盘中，我提出**下一阶段实验平台的核心方向是‘实验结论洞察化’**。即不能只输出干巴巴的 P 值，而是要在异常实验结束时，自动联动底层的漏斗数据（甚至关联 VoC 用户反馈文本归因），告诉你是因为法国区的新用户网络延迟导致了转化率下跌。只有让数据不仅赋能决策，更能赋能迭代方向，这才是实验平台真正的护城河。"

#### 3. 机器学习工程 (System Design) ⚙️
| 常见问题 (Questions)                       | 核心回答策略 (Strategy)                | 推荐资源                                                                                                                                                    |
| :----------------------------------------- | :------------------------------------- | :---------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **"模型怎么部署？离线还是实时？"**         | **Batch (Airflow) vs Real-time (API)** | 不需要视频，记住 **Airflow** 概念即可。实战：[Deploy ML Model with Flask (StatQuest)](https://www.youtube.com/watch?v=nugc2j4K7Gw) (只需看前10分钟了解概念) |
| **"梯度下降 (Gradient Descent) 是什么？"** | **Loss Function, Learning Rate**       | [StatQuest: Gradient Descent](https://www.youtube.com/watch?v=sDv4f4s2SB8) (看一次就能跟面试官吹牛)                                                         |


## 9. 模拟面试反馈 (Mock HR Audit) - 2026.02.10
*Source: Packaged Resume Review (Simulated HR/Hiring Manager)*

### ⚠️ 风险提示 (Red Flags)
1.  **薪资倒挂 (Salary/Skill Mismatch)**: 简历呈现 P7 能力 (NLP/Causal/Frontend)，但当前薪资 20w 对应初级。
    *   **HR 疑虑**: "简历过度包装" 或 "野路子出身"。
2.  **技术落地深度 (Depth)**: 涉及领域太宽 (Full-stack)，容易被怀疑 "博而不精"。

### 🎯 必考题 & 防守策略 (Killer Questions & Defense)

#### 1. 工程化能力 (Engineering)
*   **Q**: "你的 NLP 模型在生产环境如何部署？QPS 是多少？容灾怎么做？"
*   **Defense Strategy (实事求是 + 扬长避短)**:
    *   **❌ 别吹**: 不要硬说自己做了高并发部署 (容易露馅)。
    *   **✅ 话术**: "作为分析师，我负责**算法原型的验证与容器化 (Docker/Streamlit)**。我交付的是 `Pickle` 模型文件和推理脚本。高并发部署是由工程团队(Backend)负责的，但我会配合他们做性能测试 (Latency Check)。"
    *   **关键词**: `Prototype`, `Docker`, `Pickle`, `Latency Test`.

#### 2. 业务主导权 (Ownership)
*   **Q**: "排班系统中，算法、产品、后端具体哪部分是你做的？边界在哪里？"
*   **Defense Strategy (界限分明)**:
    *   **✅ 话术**: "我主导的是**核心调度逻辑 (Algorithm Strategy)** 和 **离线仿真 (Simulation)**。
        *   **Me**: 定义目标函数 (最小化闲时)、约束条件 (劳动法)、输出排班表 (CSV)。
        *   **Product**: 负责排班系统的 UI 交互设计。
        *   **Dev**: 负责将我的 Python 逻辑重写/封装进 Java/Go 后端，并处理并发请求。"

#### 3. 方法论深度 (Methodology)
*   **Q**: "做 A/B 实验时，遇到样本比率偏差 (SRM) 怎么排查？"
*   **Defense Strategy (硬核技术流)**:
    *   **✅ 话术**: "SRM (Sample Ratio Mismatch) 是我们实验的 First Check。
        1.  **卡方检验**: 先用 `chisquare` 算一下实际样本比是否符合 50/50 (p-value < 0.001 就报警)。
        2.  **归因**: 查日志。是因为**重定向延迟 (Latency)** 导致实验组加载慢？还是**过滤逻辑 (Filter)** 不一致？通常是漏斗顶端的埋点问题。"

---

## 10. 深度模拟面试 (Gemini HR Audit) - 2026.02.13
*Source: Gemini 模拟 HR/Hiring Manager 基于 Packaged_Resume.md 的深度审核*

> [!IMPORTANT]
> **核心判定**：简历呈现的能力跨度极大 (NLP + Causal + Full-stack)，面试的核心目标是 **"去伪存真"**。
> 需要通过 **"硬核笔试 + 场景化深挖"** 的组合拳来验证。

### 📝 笔试题库 (Written Test, 45-60min)

#### 1. SQL 进阶（数仓思维 + 窗口函数）
*   **题目**：`user_login_log` 表 (user_id, login_time, session_duration)，计算 **连续登录 ≥3 天的用户** 及其平均会话时长。
*   **考察点**：`ROW_NUMBER` 错位比较法。
*   **你的防守力**：🟢 **强** — 做过数仓建模 (Star Schema)，窗口函数是基本功。

#### 2. 统计学 & A/B 实验（严谨性）
*   **题目**：实验组转化率 +5%，P-value=0.04，但实验组样本量少 10% (SRM)。结果可信吗？如何排查？
*   **考察点**：SRM 意味着随机分流遭到破坏，P-value 无意义。
*   **你的防守力**：🟢 **强** — 简历核心亮点，防守话术已准备。

#### 3. ML 工程题（Python 手写能力）
*   **题目**：不使用 `CountVectorizer`，手动实现文本词频统计 + TF-IDF 计算。
*   **考察点**：离了包能不能写基础逻辑。
*   **你的防守力**：🔴 **弱** — 需要专项练习！
*   **补课代码**：
```python
from collections import Counter
import math

# 手动计算 TF (词频)
def compute_tf(doc_words):
    word_count = Counter(doc_words)
    total = len(doc_words)
    return {w: c / total for w, c in word_count.items()}

# 手动计算 IDF (逆文档频率)
def compute_idf(corpus):
    n_docs = len(corpus)
    idf = {}
    all_words = set(w for doc in corpus for w in doc)
    for word in all_words:
        doc_count = sum(1 for doc in corpus if word in doc)
        idf[word] = math.log(n_docs / (1 + doc_count))
    return idf
```

### 🎙️ 面试深挖题库 (Behavioral Deep-Dive)

#### Q1: VoC 数据标注 — "Label 怎么打的？"
*   **追问**：用户没点转人工按钮但骂完人走了，算正样本吗？
*   **你的防守力**：🟡 **需准备故事** — 要提到数据标注的"脏活"（模糊 case、标注冲突）。
*   **✅ 参考话术**："我们用了多维标注策略：不仅看转人工按钮点击，还加入了情感极性阈值和会话异常中断(session drop)作为辅助标签。标注团队每周对冲突 case 做校准会。"

#### Q2: 多语言 NLP — "某跨境电商S公司 是跨境电商，拼写错误怎么处理？"
*   **你的防守力**：🟢 **强** — 真实经验，可以提到 u→you、tks→thanks 等俚语映射。

#### Q3: Feature Importance Top 3
*   **你的防守力**：🟡 **需提前准备** — 想清楚 某跨境电商S公司 项目的 Top 3 特征及业务解释。
*   **✅ 建议准备**："Top 3 分别是 (1) 用户情感极性分 (2) 对话轮次 (3) 未解决意图数。因为情绪激动的用户转人工概率最高，对话轮次越多说明 bot 解决不了。"

#### Q3.5: [🔥 VoC 亮点追加] 简历未写但必备的进阶防守 (P7 杀手锏)
*   **Q**: "目前你们的文本挖掘只用到了 TF-IDF 和主题标签交叉，有没有想过进一步优化？它有什么局限性？"
*   **Defense Strategy (迭代思维 Phased Approach - 应对简历单薄的最佳策略)**:
    *   **✅ 话术 (请背熟)**: "这也是我们在近期复盘时（v2.0 阶段）重点反思的。在第一阶段（v1.0，即简历中体现的这版），为了快速跑通 MVP，我们只是用 Python 提取了差评高频短语并按「客询主题」做了 2D 交叉。**但这在落地时遇到一个问题：光看频次，无法精准评估痛点的「严重程度优先级」。**
    *   "所以在近期的深化迭代中，**我主导引入了『用户行为特征』建立 3D 交叉分析矩阵**。除了原有的客询标签，我从数仓额外拉取了用户的**『一周内重复进线次数(Repeat Call Rate)』**和**『用户价值分层 (VIP)』**指标。
    *   "在打通这三个维度后，全局数据立刻立体了：比如我发现有一个短语（如 'express station url'）在盘子上不算 Top1，但它**引发了对应法国区大量 VIP 用户的重复进线（严重体验受损）**。顺藤摸瓜下去，很快查明是运营给 VIP 错配了低级客诉表单的 URL。像这种结论，单从平面的 TF-IDF 词频里是永远挖不出来的。从『算特征』进化到『用行为标签做矩阵分层』，是我这个项目最大的沉淀。"

#### Q4: DID 平行趋势假设 ⚠️ 杀手锏题
*   **你的防守力**：🔴 **弱** — 必须补课！
*   **✅ 参考话术**：
    1.  **验证方法**：画实验前两组的时间序列图，观察趋势是否平行。
    2.  **安慰剂检验**：在实验前做一次"假 DID"，系数应接近 0。
    3.  **如果不平行**：改用 PSM-DID（先匹配再差分）或 Synthetic Control（合成控制法）。

#### Q5: Prophet vs XGBoost 选型 — "为什么不直接用 XGBoost？"
*   **你的防守力**：🟢 **强** — 今天刚讨论过！
*   **✅ 加分答案**："Prophet 擅长捕捉趋势和周期性（自动分解 trend + seasonality），适合做 Baseline；XGBoost 擅长特征交互和非线性关系，引入外部特征后做 Refinement。两者的逻辑类似于 **Residual Learning (残差学习)** — 先用简单模型拟合大趋势，再用复杂模型学习残差。"

#### Q6: LiuliX WASM 工程难点
*   **你的防守力**：🟢 **强** — 亲手做的，Web Worker、Chunk Loading、内存限制 (2-4GB) 都踩过。

#### 💰 成本计算公式 — "200万怎么算的？"
*   **✅ 必须背熟这个链条**：
    > 转人工率下降 9pp → 日均减少 ~18万次转人工 (2M × 9%) → 每次人工处理 ~5分钟 → 日均节省 ~15,000 人工分钟 → 年化 ≈ 减少 ~50 个外包坐席 → 每坐席 ~4万/年 → **年省 ~200万**

---

## 11. Agent 模拟面试 (Antigravity Audit) - 2026.02.13
*Source: 基于 Packaged_Resume.md + 学习过程观察的差异化考核*

> [!NOTE]
> 与 Gemini 侧重 "去伪存真" 不同，我的考核侧重 **"深度理解 vs 表面记忆"**，针对你这 17 天学习中暴露的认知薄弱点出题。

### 📝 笔试题 (Written, 30min)

#### 1. 时间序列特征工程（考察 Prophet 之外的理解）
*   **题目**：给定一个含 `date` 和 `sales` 的 DataFrame，请写 Python 代码构造以下特征：
    1.  7 天滚动均值 (`rolling_7d_mean`)
    2.  同比去年同日销量 (`lag_365`)
    3.  是否为月末最后 3 天 (`is_month_end`)
*   **考察点**：你是否理解 lag/rolling 特征的构造逻辑，而不只是会调 Prophet。

#### 2. 评估指标辨析（考察 MAE vs MAPE vs RMSE 的本质区别）
*   **题目**：你的模型在正常日 MAPE=15%，大促日 MAPE=45%。
    1.  如果业务方说 "整体 MAPE 25% 可以接受"，你同意直接上线吗？
    2.  如果不同意，你会怎么向业务方解释？
*   **考察点**：**分层评估思维** — 整体指标掩盖了分布不均的问题。这是你今天刚学到的！

#### 3. 超参调优理解题
*   **题目**：XGBoost 中 `max_depth=3` 和 `max_depth=15` 各有什么风险？`min_child_weight` 的作用是什么？面试时常问："你怎么防止 XGBoost 过拟合？"
*   **考察点**：不是会用 `RandomizedSearchCV` 就够，还要能解释*为什么*调这些参数。
*   **✅ 参考答案**：
    *   `max_depth=3`：欠拟合风险，模型太简单。`max_depth=15`：过拟合风险，记住了训练集噪声。
    *   `min_child_weight`：控制叶节点最小样本权重，越大越保守（防过拟合）。
    *   **防过拟合三板斧**：`max_depth` ↓ + `min_child_weight` ↑ + `gamma` ↑ + `reg_lambda` (L2 正则化)。

### 🎙️ 面试深挖题 (Behavioral)

#### Q7: 分层评估 — "你发现极值预测差之后，做了什么？"
*   **考察点**：你是否有**闭环思维** — 发现问题后有没有推动解决方案？
*   **✅ 参考答案**："分层评估发现大促日 MAE 是平日的 5 倍。我做了三步：(1) 分析特征重要性，发现时间特征权重过高、大促标记缺失；(2) 提议加入 `is_promotion` / `is_holiday` 特征做二次建模；(3) 建议算法团队评估分段模型(普通日+大促日各一个模型)的可行性。"

#### Q8: 模型对比 — "如果 Prophet 和 XGBoost 预测结果矛盾，你相信哪个？"
*   **考察点**：模型选型的**业务判断力**，不是"哪个 MAE 低就用哪个"。
*   **✅ 参考答案**："取决于场景。短期规律性强的(日常排班)信 Prophet，因为它的周期性分解更稳定；有外部冲击的(大促期间)信 XGBoost，因为它能利用促销特征做精细化预测。实际中我会做 Ensemble (加权平均)。"

#### Q9: 数据泄露 — "你的时间序列模型有没有 Data Leakage 风险？"
*   **考察点**：时间序列最常犯的错误 — 用未来数据训练过去。
*   **✅ 参考答案**："时间序列**绝对不能**用标准 KFold CV，必须用 **TimeSeriesSplit** (前向验证)。另外，rolling 特征如果在 split 前计算，会导致测试集包含训练集信息。正确做法是在每个 fold 内部单独计算。"

---

## 12. 全链路深度面试审核 (DeepSeek Audit) - 2026.02.25
*Source: 基于当前全量简历的 DeepSeek 模拟面试评估*

> [!TIP]
> **最佳回答模板**：如果我是阿里面试官，面对你这样一份优秀的简历，我的考察策略会是：**不考“会不会”，而考“有多好”和“为什么”**。
> 
> 你的简历已经展示了你掌握了P7应该具备的核心技能，所以我的面试不会停留在“你是否用过CUPED”这种问题上，而是会层层深挖，验证你的能力深度、思维严谨性和业务影响力是否真正达到了P7的“主导”和“赋能”水平。

### 📝 笔试环节：业务分析设计方案 (限时案例)
对于P7级别，笔试通常不会是一道简单的SQL题。它更可能是一个**开卷的、限时的、综合性案例分析**，考察你的业务 sense、框架思维和落地能力。

**题目示例（淘宝特价版 秒杀漏斗）：**
> **背景**：“限时秒杀”频道点击率和转化率持续下跌，流量曝光不变。运营怀疑选品，产品怀疑UI。
> 
> **任务**：
> 1. 请设计一份分析框架，系统性诊断效率下降的原因（拆解维度、需要数据）。
> 2. 改版后点击率有波动。设计严谨 A/B 实验评估效果：a) 假设是什么？ b) 单元和指标如何选？ c) 如何处理“秒杀”的时效性和稀缺性特征对实验结果的影响？
> 3. 核心原因是推荐不精准。算法资源排期满，你需要用数据案例“推销”想法争取资源，如何构建？
> 4. 用 SQL/伪代码写出清洗“频道用户停留时长”的逻辑，并说明数据质量校验点。

**考察P7能力解析：**
*   **维度1（问题拆解）**：结构化拆解模糊问题（人货场 或 流量-承接-转化）。
*   **维度2（实验设计）**：深挖秒杀场景的高阶实验方法。网络效应（商品稀缺性）、时间衰减效应、分层切分 或 **PSM/DID** 验证。呼应简历的 CUPED 经验。
*   **维度3（影响力与沟通）**：将数据转化为驱动业务的语言（如“不优化算法将损失多少GMV”）。
*   **维度4（工程化思维）**：数据生产闭环（指标定义、曝光未点击的异常清洗）。

### �️ 面试环节 (三轮深挖策略)

#### 第一轮：业务面（直属 Leader）
**考察重点**：项目深挖、硬技能验证、解决问题的细节。
*   **Q1: VoC 挖掘优先级**：”那么多用户痛点，你怎么确定算法挖掘出来的 Top 30 就是业务最应该优先解决的？有没有可能模型有偏差？“
    *   **应对策略 (业务判断力)**：结合**业务成本**（物流投诉赔付高）和**改进难度**（尺码问题短期难改）对模型产出进行二次排序。
*   **Q2: 闭环落地能力**：”举个具体的知识库盲区例子？当时的知识库怎么写？模型告诉你什么特征？推动修复后效果如何量化？“
    *   **应对策略 (STAR闭环)**：必须讲述 发现问题 → 分析根因 → 解决 → 实验验证 的全过程。

#### 第二轮：交叉面（其他部门专家）
**考察重点**：方法论深度、技术视野、统计严谨性。
*   **Q3: CUPED 局限性**：”CUPED利用实验前协变量降低方差，但如果实验前后用户分布发生显著变化（比如大促），CUPED还适用吗？怎么处理？“
    *   **应对策略 (知其然知其所以然)**：解释线性回归调整原理，提出检验协变量稳定性或引入时间趋势交叉项。
*   **Q4: 时序模型融合**：”Prophet能处理节假日，为什么还要用XGBoost引入外部特征？这两个模型你怎么结合的？“
    *   **应对策略 (模型工程)**：拆解线性趋势与非线性复杂因素，解释 Residual Learning（Baseline + 残差拟合）。

#### 第三轮：终面（总监 VP 级）
**考察重点**：业务影响力、战略思维、软素质。
*   **Q5: 战略思维与影响力**：”客服部门是成本中心，老板要砍预算。给你5分钟说服我，你要怎么证明你们还能创造价值并获得投资？“
    *   **应对策略 (跨越 P8 潜质)**：跳出降本局限，主打**增效**。通过对话发现新品机会、优化商品描述降低退货率，将客服数据赋能给前端和供应链的“大脑”。
*   **Q6: 韧性与认知**：”过去五年你做过的最艰难的（非技术类）决策是什么？“
    *   **应对策略 (成熟度)**：分享一个争取资源、面对项目质疑时的反应模式和复盘经验。

### 💡 给你的冲刺备战建议
1.  **准备 STAR 加强版**：讲每一个故事，不仅要有情节，还要有 **“Why this way”** (方法选型的 trade-off) 和 **“What if”** (如果重来哪里能更好)。
2.  **准备影响力故事**：专门讲述说服固执同事、跨团队凝聚力量的真实案例。
3.  **技术视野**：谈及前沿趋势时，用 LiuliX 引入端智能和隐私计算，让总监眼前一亮。
4.  **向上管理**：准备一个”向老板汇报坏消息（实验失败）并带偏向下一步行动“的真实案例。

---

## 12.5 P7/P6+ 真实模拟面试复盘 (Doubao Audit) - 2026.03.03
*Source: 豆包专家模型针对阿里国际AE客户体验洞察分析师进行的40分钟深度模拟面试*

> [!CAUTION]
> **真实水位测算**: **P6+ (具备P7潜力，但未稳P7)**。
> 专业软硬技能（SQL/Python/时序/A/B/因果）和业务执行闭环（3年+客服场景，0-1项目搭建）**完全达标且是强项**。
> 但缺乏覆盖全链路的**全局商业视野**与**专家级方法论体系化沉淀**，尚未达到P7“定义复杂问题并主导跨域解决”的最高要求。

### 🔴 P7 核心差距与短板 (The Gap to P7)
1.  **业务边界狭窄 (Full-link E-commerce Blindspot)**: 经验高度集中在售后侧。对导购、支付、物流、商家运营等**非客服**全链路的核心转化漏斗、痛点、及关联性理解偏表面。缺乏系统性影响。
2.  **新场景顶层框架缺失 (Lack of Top-level Design)**: 面对新场景（如B端商家体验），分析思路仍停留在已有经验的简单复用（如照搬VoC文本聚类），而未从商家全生命周期（入驻、上新、物流、退款、合规/关税）进行系统的顶层指标框架设计。
3.  **高阶方法论落地缺乏“泥土感” (Causal Inference Grounding)**: 因果推断（PSM/DID）回答偏理论化，未将“控制了哪些业务强关联的混淆变量”下钻到真实的细节。需将其落地到简历项目中（例如：对VoC提取出的Top6痛点做独立的因果归因量化）。
4.  **实验设计的终极严谨性 (Business Rigor in Exp Design)**: 面对交叉混淆变量（如季节大促），过度依赖事后PSM补救，忽视了事前实验正交分流的控制；对跨境特有的风险视角（如主动赔付被恶意群控薅羊毛、不同国家的护栏指标差异）缺乏准备。

### 🎯 P7 攻坚落地动作 (Next Steps for W5)
1. **全链路电商业务恶补**: 系统整理“转化-支付-物流-售后”每一步的**核心指标、断点及应对策略**。
2. **因果推断"套壳"落库**: 把 PSM/DID **强制**嵌回《VoC诊断体系》和《排班调度》的故事里。打造**“我不仅提取了痛点，我还用PSM量化了某个特定痛点因为选择性偏差被低估的独立影响”**的P7级防守话术。
3. **建立跨境专属变量库**: 梳理 AE 业务必须考虑的“大杀器变量”（大促爆仓清关时效、汇率波动、多语言时差、本地支付路由成功率、被税拒收率）。

---

## 13. �🎬 推荐学习视频 (Tonight & This Week)

### 🌙 今晚推荐（睡前看，不需要写代码）
| 视频                                                                             | 时长   | 为什么看                                           |
| :------------------------------------------------------------------------------- | :----- | :------------------------------------------------- |
| [StatQuest: Time Series (Concepts)](https://www.youtube.com/watch?v=nMHhl_sI0ag) | ~15min | 时间序列核心概念（平稳性、自相关）的**最直觉解释** |
| [StatQuest: XGBoost (Part 1)](https://www.youtube.com/watch?v=OtD8wVaFm6E)       | ~25min | 搞懂 XGBoost 的 Gradient Boosting 本质，面试必问   |

### 📅 本周视频清单
| 视频                                                                                   | 优先级 | 关联面试题                           |
| :------------------------------------------------------------------------------------- | :----- | :----------------------------------- |
| [StatQuest: Regularization (Ridge/Lasso)](https://www.youtube.com/watch?v=Q81RR3yKn30) | P1     | 防过拟合三板斧的理论基础             |
| [StatQuest: ROC and AUC](https://www.youtube.com/watch?v=4jRBRDbJemM)                  | P1     | 分类模型评估 (Churn 项目要用)        |
| [Krish Naik: Prophet Tutorial](https://www.youtube.com/watch?v=Gy2RtTree7s)            | P1     | Prophet 实操 + add_regressor 用法    |
| [StatQuest: Bias vs Variance](https://www.youtube.com/watch?v=EuBBz3bI-aA)             | P2     | 面试经典题，你 Day 13 学过但需要复习 |

---

## 14. 📋 知识图谱自评 & 缺口填补方案 (Knowledge Graph Self-Assessment) - 2026.02.15

> [!IMPORTANT]
> **核心发现**: 基于 [知识图谱](../00_教学课件/知识图谱.md) 的逐项自评，当前 ML 理论掌握率仅 **26%** (10/38 项)。
> 最薄弱模块: **工程化 (17%)** 和 **数据基础 (20%)**。

### 📊 自评结果概览

| 支柱            |         ✅ 已掌握         | ❌ 缺失/不足 | 掌握率  |
| :-------------- | :----------------------: | :---------: | :-----: |
| 1. 数据底层逻辑 |       1 (假设检验)       |      4      | **20%** |
| 2. 算法原理     |     2 (K-Means, PCA)     |      6      | **25%** |
| 3. 特征工程     | 4 (OHE, Stats, Corr, FI) |      7      | **36%** |
| 4. 评估与优化   |     2 (TSS, Optuna)      |      6      | **25%** |
| 5. 工程化       |         1 (SHAP)         |      5      | **17%** |
| **总计**        |          **10**          |   **28**    | **26%** |

### 🔴 Tier 1: 核心理论盲区 (面试必问，必须能用大白话讲清楚)

| #    | 知识点                            | 困惑点                      | 嵌入时机                         |
| :--- | :-------------------------------- | :-------------------------- | :------------------------------- |
| 1    | **Bias-Variance Tradeoff**        | 不清楚过拟合/欠拟合的本质   | Walmart Modeling 阶段            |
| 2    | **Linear Regression Weights**     | 不理解权重的物理含义        | 2C 分类项目 LR baseline          |
| 3    | **Logistic Regression (Sigmoid)** | 不知道 Sigmoid 如何映射概率 | 2C 分类项目 Churn 预测           |
| 4    | **Regularization L1/L2**          | 完全空白                    | 2C 分类项目 LR 的 `penalty` 参数 |
| 5    | **Decision Tree 分裂原理**        | 不了解 Entropy/Gini         | Walmart Modeling 讲 XGB 底层     |
| 6    | **Bagging vs Boosting**           | 不知道 RF 和 GBDT 的区别    | Walmart RF vs XGB 对比实验       |

### 🟡 Tier 2: 实操盲区 (知道名词，但没亲手写过代码)

| #    | 知识点                           | 困惑点                         | 嵌入时机                   |
| :--- | :------------------------------- | :----------------------------- | :------------------------- |
| 7    | **K-Fold / Stratified K-Fold**   | 不理解 CV 原理和两者区别       | Walmart 替换 single split  |
| 8    | **Grid Search / Random Search**  | 没写过代码                     | Walmart 对比 Optuna        |
| 9    | **Scaling (为什么 Tree 不需要)** | 不理解梯度下降的影响           | 2C 分类 LR 必须 Scale      |
| 10   | **Imputation 进阶**              | 只会 fillna                    | Walmart `IterativeImputer` |
| 11   | **Label Encoding 深化**          | 掌握不够                       | Walmart Store/Dept 编码    |
| 12   | **Pickle/Joblib**                | 没写过代码                     | 2C 分类完成后保存模型      |
| 13   | **RMSE vs MAE**                  | 不理解 RMSE 为什么对大误差敏感 | Walmart Evaluation         |

### 🟢 Tier 3: 进阶补充项 (Phase 3 或后续学习)

| #    | 知识点                     | 建议时机                            |
| :--- | :------------------------- | :---------------------------------- |
| 14   | Broadcasting 原理          | 知识库增补已覆盖，复习即可          |
| 15   | 分布可视化 SOP             | 知识库增补已覆盖，复习即可          |
| 16   | LogLoss                    | 2C 分类项目评估阶段                 |
| 17   | Target Encoding            | Walmart (高基数 Store/Dept)         |
| 18   | PolynomialFeatures         | 低优先级，面试罕见                  |
| 19   | RFE                        | 低优先级，Feature Importance 已够用 |
| 20   | Pandas 内存优化            | 遇到大数据集时再学                  |
| 21   | Pipeline/ColumnTransformer | Phase 3 系统设计                    |
| 22   | Permutation Importance     | Phase 3                             |
| 23   | Concept Drift              | Phase 3                             |
| 24   | 异常值 Z-Score/IQR         | 知识库增补已覆盖                    |

### 🗓️ 嵌入策略

> **核心原则**: 不单独开课，在 Walmart 项目和 2C 分类项目中**边做边学**。

1. **Walmart 项目 (当前)**: 嵌入 Tier 1 的 #5-6 (Tree 原理) + Tier 2 的 #7-8, 10-11, 13
2. **2C 分类项目 (下一步)**: 嵌入 Tier 1 的 #2-4 (LR 原理) + Tier 2 的 #9, 12
3. **Phase 3 面试准备**: 补充 Tier 3 中的 Pipeline/Concept Drift 等概念

### 📚 知识库增补记录

已将以下内容追加到 [knowledge_base_full.md](../02_速查手册/knowledge_base_full.md) 的 `# 🧠 知识库增补` 章节:
*   Broadcasting 原理 (SIMD/C-Level/Memory Locality)
*   分布可视化 SOP (skew → log1p workflow)
*   LR Weights / Sigmoid / L1 vs L2
*   Decision Tree / Bagging vs Boosting 对比表
*   Scaling 为什么 Tree 不需要
*   Imputation 进阶 (MICE/KNN)
*   RMSE 敏感性 / LogLoss
*   K-Fold / Stratified K-Fold / Time Series Split
*   Pickle/Joblib SOP 代码


## 📝 历史进度追踪 (Progress Log)

### 📅 2026-02-08 (Day 12)
*   **[+ New]** **Two-Part Model** & **Bootstrap**: 攻克非正态分布数据难题。
*   **[+ New]** **JD 调研**: 明确了 某新能源车企T公司 (Ops/Engineering) 和 某短视频大厂B公司 (Risk/Strategy) 的侧重点。
*   **[- Gap]** **Engineering**: 发现离 Pipeline/Airflow 等大厂基建还有距离。
*   **[- Goal]** 下一步：**Case 8 (辛普森悖论)** -> **Phase 4 ML建模**。

### 📅 2026-02-09 (Day 13)
*   **[+ New]** **XGBoost**: 成功部署进阶分类模型，对比 Random Forest 提升了 AUC。
*   **[+ New]** **SHAP**: 掌握了模型归因神器，解决了 "Why" 的问题。
*   **[+ New]** **Clustering**: 实战 K-Means 进行用户分层。
*   **[Done]** **Time Series**: 攻克时序预测难关，掌握 **Differencing (差分)**、**Reconstruction (还原)** 与 **Cross-Validation (交叉验证)**。
*   **[+ New]** **Robustness Check**: 学会了 **敏感性检验** (添加噪音测试模型抗干扰性)。
*   **[+ Theory]** **Bias vs Variance**: 深刻理解了 Underfitting vs Overfitting 的权衡。
*   **[+ Theory]** **Loss Function vs Metric**: 明白了 MSE 是给模型求导用的，Metric 是给人看的。
*   **[- Goal]** 下一步：**Phase 5 数据工程** (Airflow/Spark) 或更多的 ML 0-1 实战练习 (防过拟合)。

### 📅 2026-02-10 (Day 14) - The Senior Pivot 🚀
*   **[+ Strategy] VoC Transformation**: 成功将 "NLP算法工程师" 人设转型为 **"VoC 商业分析专家"**。
    *   *Insight*: 面试官不关心 TF-IDF 怎么算，只关心你如何用它发现了 "Top 30 痛点" 并节省了 200万。
*   **[+ Skill] Text Mining Loop**: 彻底跑通 **Input (Text) -> Vector (TF-IDF) -> Model (XGBoost/K-Means)** 全流程。
    *   *坑点排查*: 敏锐发现了 **"Language Trap"** (多语言 TF-IDF 导致聚类偏差)，这是 Senior 级别的 Feature Engineering 洞察。
*   **[+ Resume] Value-Based**: 简历去肥增瘦，强调 **Business Impact (Result)** 而非 Tech Stack (Implementation)。
*   **[- Gap] Theory Prep**: 锁定 **StatQuest** 为理论补给站，针对性准备 "TF-IDF 原理"、"Gradient Descent"、"A/B Testing" 面试题。
*   **[- Goal] 下一步**: **W2 启动** —— 攻克 **LightGBM** 与 **Causal Inference (因果推断)**。


### 📅 2026-02-11 (Day 15)
*   **[+ New] LightGBM w/ Optuna**: 跟随 Agent 跑通了 LightGBM 自动调参框架，理解了 `objective='binary'` 和 `metric='auc'` 的配置。
*   **[- Gap] Coding Independence**: 尝试脱离 Agent 从 0-1 复现案例时，卡在了**数据清洗** (Data Cleaning) 环节。
    *   *Symptom*: 面对脏数据第一反应是写 `for` 循环，导致代码冗余且报错。
*   **[+ Fix] Data Cleaning Gym**: 紧急启动专项训练 (Gym)，完成了 63/100 题。
    *   **Mastered**: 熟练掌握 `fillna` (均值插补), `dropna`, `str.contains`, `str.extract`。
    *   **Shift**: 成功从 "Python Loop" 思维转变为 "Pandas Vectorization" (向量化) 思维。
*   **[- Goal]** 下一步：完成剩余 37 题 (GroupBy/Time Series)，扫清代码障碍，重新挑战 LightGBM 0-1 实战。

### 📅 2026-02-12 (Day 16)
*   **[+ New] Search Analytics Dashboard**: 全栈开发搜索分析看板系统 (Flask + Chart.js + MkDocs)，实现搜索埋点 → 数据持久化 → 可视化看板全链路。
*   **[+ New] Local LLM Integration**: 集成 Ollama 本地模型，实现 AI 学习建议（函数文档速查、薄弱模块定位、练习 Prompt 生成）。
*   **[+ New] Workflow Automation**: 创建 `/daily_progress` 工作流，自动整合搜索分析 + 对话记录 + Gap Analysis 生成每日报告。
*   **[+ Skill] Module C Filtering Drill**: 完成 Pandas 复杂过滤专项（boolean indexing, `str.contains`, negation, `query()`）。
*   **[+ Skill] Module D Pivot Table**: 彻底掌握 `pivot_table` vs `groupby`，理解 MultiIndex 打平技巧。
*   **[Done] Data Cleaning Gym**: 完成 Pandas 专项训练 (Module A/B/C/D)，彻底克服对 "脏数据" 的恐惧。
    *   *Pivot*: 从 "写 For 循环" 进化到 "Pandas 向量化思维" (Series Mapping / Vectorized String Ops)。
*   **[+ New] Clustering Mastery**: 完成 Project 2A 用户分层。
    *   *Technique*: 掌握 **K-Means** (Elbow Method), **Silhouette Score** (轮廓系数), **Log Transformation** (纠偏).
    *   *Insight*: 理解 **Rule-based RFM** vs **K-Means** 的商业权衡 (Interpretability vs Discovery)。
*   **[📊 Search]** 今日高频搜索：`groupby`, `KMeans`, `silhouette_score`.
*   **[- Goal]** 下一步：启动 **Project 2: Retail Operations Masterclass**，涵盖 RFM (Clustering), Sales Forecast (Regression), Churn (Classification)。

### 📅 2026-02-13 (Day 17)
*   **[+ New]** XGBoost 回归建模实战：`RandomizedSearchCV` 调参、分层评估 (Stratified Evaluation) 识别极值问题。
*   **[+ New]** 简历优化 (Resume Polishing)：将建模经历重构为 "Baseline (Prophet) -> 精细化 (XGBoost) -> 调优" 的迭代叙事，修正评价指标 (MAE -> MAPE)。
*   **[+ New]** 面试模拟 (Mock Interview)：使用 Gemini 模拟 HR 审核简历，生成笔试题+面试题库，识别出 TF-IDF 手写 和 DID 平行趋势 两个必补盲区。
*   **[+ Insight]** 跨团队协作认知：理清了 DA vs ML Engineer 的边界——特征工程+业务归因是分析师的活，模型架构+线上部署是工程师的活。
*   **[- Gap]** 极值预测 (Extreme Value Prediction) 仍是难点，Prophet + Regressor 混合模型尚未实操。
*   **[- Gap]** TF-IDF 手写实现、DID 平行趋势假设验证 尚未练习。
*   **[📊 Search]** Time Series (Prophet), ML Models (XGBoost/LightGBM), Feature Engineering (Pandas).
*   **[- Goal]** 下一步：(1) 晚间看 StatQuest 时间序列视频加深理论；(2) 明日继续 Prophet baseline 实操；(3) 准备面试题防守策略。

### 📅 2026-02-14 (Day 18) - 认知负荷过载 & 概念突破
*   **[+ Concept]** **聚合粒度黄金法则**：Aggregation Level = Business Question Level。理解了 Global vs Store vs SKU 粒度的选型逻辑。
*   **[+ Concept]** **宽表 vs 竖表**：XGBoost 喜欢竖表 (Long Format)，Store 当特征而非当列。
*   **[+ Concept]** **Per-Store 特征工程**：`groupby('Store').shift()` 代替全局 `shift()`，防止跨店数据污染。
*   **[+ Concept]** **外部特征因果链**：油价 → 宏观经济 → 消费能力 → 零售销量 (厄瓜多尔 = 石油出口国)。
*   **[+ Knowledge]** 沉淀到速查手册：`07_ml_models.md` (调优诊断表)、`06_feature_engineering.md` (Leakage 检测)、`08_evaluation.md` (分层评估)。
*   **[+ Data]** 完成 Walmart 数据集选型 (Superstore → Store Sales → Walmart 三级跳)，理解了数据集难度评估。
*   **[⚠️ Blocker]** **认知负荷过载 (Cognitive Overload)**：代码能力 (层1-3) 已足够，卡在方法论 + 业务判断 (层4-5)。这是 Senior vs Junior 分水岭。
*   **[📊 Search]** `pd.date_range(freq=)`, `pd.merge()`, `groupby().shift()`, Time Series 速查页面。
*   **[- Goal]** 下一步：(1) 休息消化概念；(2) 明日从 Walmart EDA 开始，不急着建模；(3) 一步一步来，先画图再加特征。

### 📅 2026-02-15 (Day 19) - The Regression Breakthrough & Knowledge Graph Assessment 📋📈
*   **[+ New] Time Series Featurization**: 彻底掌握 **Lag Features** (滞后特征) 和 **Rolling Window** (滚动窗口) 的代码实现与业务含义。
*   **[+ New] Metric Strategy**: 确立了 **某跨境电商S公司 场景下的指标选型** —— Volume 用 WAPE (百分比) 汇报精度，Headcount 用 MAE (绝对值) 汇报业务价值。
*   **[+ New] Inference Pipeline**: 理解了 **Lookback Window** (特征回溯) 的必要性，解决了 "模型如何预测明天" 的工程困惑。
*   **[+ Knowledge] SOP Refinement**: 重构了 ML SOP，增加了 Regression vs Classification 的参数对比表和 Interview Cheat Sheet。
*   **[+ Concept] Bagging vs Boosting**: 彻底搞懂了核心区别 —— **Bagging (如 RF) 并行训练降方差 (Variance)**，**Boosting (如 XGB) 串行训练降偏差 (Bias)**。
*   **[+ Assessment] 知识图谱自评**: 对照 5 大支柱 38 项技能点逐一打勾，发现当前 ML 理论掌握率约 26%。
*   **[+ Knowledge] 知识库增补**: 向 `knowledge_base_full.md` 追加了 18 个知识点 (Broadcasting, Sigmoid, L1/L2, K-Fold, RMSE 等)。
*   **[- Gap] Code Muscle Memory**: 发现基础函数 (KFold, SimpleImputer) 记忆模糊，需通过 Cheat Sheet 强化。
*   **[- Gap] Algorithmic Theory**: 算法底层原理 (Tree Split, ID3/C4.5) 仍需在后续实战中补充。
*   **[+ Future] Hybrid Model**: (User Proposed) 计划尝试 **Prophet Trend + XGBoost Residuals** 的高阶打法（Senior DA 加分项）。
*   **[📊 Search]** `metrics` (MAE vs MAPE), `deployment` (Lookback), `SOP` (Refinement).
*   **[- Goal]** 下一步 (除夕): **"挂机复习"** —— 观看 StatQuest 视频，浏览 Cheat Sheet，为年后 Causal Inference 蓄力。

### 📅 2026-02-17 (Day 21) - 因果推断开篇 & 实战突破 (Causal Inference Kickoff & Breakthrough) 🚀
*   **[+ Plan] Week 3 核心目标**: 攻克 **DID (双重差分)** 和 **PSM (倾向性得分匹配)**，配合 A/B Test 高阶实战。
*   **[+ Action] 环境配置**: 创建 `04_因果推断` 专栏，准备模拟数据。
*   **[+ Concept] Correlation ≠ Causation**: 从 "尿布与啤酒" 到 "辛普森悖论"，深刻理解混淆变量 (Confounder) 的危害。
*   **[Done] Membership LTV 因果推断挑战 (0-1 Coding)**: 完整走通 IV → OLS → PSM → IPW → DoWhy 全流程。
    *   **IV-2SLS**: 修复公式语法 (`[endog ~ instr]` 格式)，识别出 Exclusion Restriction 违规 (把 Confounder 误当 Instrument)。
    *   **OLS**: 控制混淆变量后估计 ATE ≈ 201.5，敏感性检验偏差仅 0.02%。
    *   **PSM**: 诊断 Common Support Violation (仅 707/5900 唯一匹配)，实施 Trimming 截断策略 (n=5121)。
    *   **IPW**: 逆概率加权估计 ATE ≈ 221.1，与 OLS 结果一致。
    *   **DoWhy Refutation**: Placebo (New Effect ≈ 0, P=0.94 ✅) + Random Common Cause (New Effect ≈ 201.5, P=0.84 ✅)。
*   **[+ Concept] 预测 vs 因果**: 理解了 "P值高=好" 的反直觉场景 (Refutation Tests)，以及 "R² 低不代表模型差" (因果推断中的 Confounders 不需要完美预测 Treatment)。
*   **[📊 Search]** `15_causal_inference` (14+ 次访问), `drop(columns=)` (3 次搜索)。
*   **[- Goal]** 下一步：(1) 更新速查手册 PSM/IPW/DoWhy 代码片段；(2) 启动 A/B Test 高阶实战 (Delta Method / CUPED)。

### 📅 2026-02-18 (Day 22)
*   **[+ New]** **Placebo Test**: 掌握了时间安慰剂 (Fake Time) 和个体安慰剂 (Fake Treatment) 的代码实现。
*   **[+ New]** **Event Study**: 成功绘制动态效应图验证平行趋势。
*   **[+ Env]** **MathJax Local**: 解决了离线环境下的公式渲染问题。
*   **[- Gap]** **Reporting**: 业务汇报 (Step 7) 仍需加强，需从单纯报数字转向讲故事。
*   **[📊 Search]** `DID`, `Placebo Test`, `MathJax`, `pyfixest`

### 📅 2026-02-25 (Day 29) - A/B Test 高阶爆发 & 面试武器库升级 💣
*   **[+ Milestone]** **A/B 测试高阶专栏通关**: 彻底攻克了传统初级基建，跨越到大厂中后台实验平台的高阶算法边界。
*   **[+ Core]** **Delta Method**: 突破了 Ratio Metric（如转化率、大盘转人工率）方差估计的盲区，理解了分子分母独立计算再用协方差修正的精髓。
*   **[+ Core]** **CUPED**: 除了掌握 $\theta$ 的计算，真正具备了 Senior 视角的 **“五步稳健性检验”**（均值不变、减少方差、Pre-experiment 隔离等），能对线算法工程师。
*   **[+ Core]** **Sequential Testing**: 理解了 DTD (Day-to-day) 和 LTD (Life-to-date) 监控体系的本质区别，引入 **O'Brien-Fleming Alpha Spending** 解决 Peeking 问题。
*   **[+ Strategy]** **面试降维打击**: 构建了极其硬核的 `P-value = 0.08` 处理流程：SRM排查 → PSM/IPW 解决选择性偏差 → CUPED 终极降噪。彻底串联了 A/B 测试和因果推断。
*   **[+ Concept]** 分清了 **PSM (个体匹配)** 和 **SCM (宏观实体合成)** 的业务适用边界。
*   **[- Gap]** **Coding / Implementation**: A/B 测试高阶算法的代码实现比较多依赖 Snippets，白板默写能力较弱（但面试大概率只考业务思路和原理）。
*   **[- Goal]** 下一步：转入真实投递阶段（今天已定制某在线旅游平台C公司国际机票简历），重点转为 **Mock Interview (行为面试/白板/STAR 故事表述)**。

---

## 🗓️ 修订版冲刺路线图 (Revised Sprint Plan, Target: 3/13 Offer)
*Strategy: **简历项目防守优先** (Resume Defense First)*
*Updated: 2026-02-15*

> [!CAUTION]
> **现实检查**: 今天是 2/15，距离 3/13 还剩 **26 天**。简历上已经写了 XGBoost/Prophet/DID/PSM/A/B Test，**面试官会默认你全都会**。
> 因此策略调整为：**不是"学会所有东西"，而是"能防守住简历上的每一条"**。

---

### 📊 简历 vs 能力现状对照表

| 简历声称 (Resume Claim)          | 面试官会怎么问                         |        当前防守力         |    本轮重点    |
| :------------------------------- | :------------------------------------- | :-----------------------: | :------------: |
| **VoC + NLP (TF-IDF/XGBoost)**   | "Top 3 Feature? 怎么处理多语言?"       |           🟢 强            |    ✅ 已具备    |
| **时序预测 (Prophet + XGBoost)** | "Prophet vs XGB 选型? MAPE 8% 怎么验?" |           🟡 中            |  **本周收尾**  |
| **A/B Test (SRM/Delta Method)**  | "SRM 怎么排查? Delta Method 公式?"     |        🟢 强 (理论)        | W3 补实战代码  |
| **DID/PSM (因果推断)**           | "平行趋势怎么验? Confounders?"         | 🟡 中 (PSM/IPW/DoWhy 已通) | **W3 补 DID**  |
| **XGBoost/LightGBM 分类**        | "过拟合怎么防? Bagging vs Boosting?"   |   🟡 中 (代码有,理论弱)    | **本周补原理** |
| **Pipeline/Airflow**             | "怎么部署? Batch vs Real-time?"        |       🟢 强 (实战过)       |    ✅ 已具备    |

---

### 📍 本周末 (2/15 - 2/16): ML 模块收尾 🔧

> **核心原则**: **够用即可，不追求完美**。简历上已经写了 Prophet + XGBoost，目标是能复述流程 + 防守面试问题。

#### ✅ 必须完成 (Must Do)
| 任务                                                      | 预计时间 | 产出                                               |
| :-------------------------------------------------------- | :------: | :------------------------------------------------- |
| **Walmart 快速收尾**: EDA + 基础特征 + XGBoost baseline   |    3h    | 能说出 "Store-level weekly forecasting, MAPE ~15%" |
| **ML 理论补课**: 复习知识库增补 (Tier 1 六项)             |    1h    | 能用大白话讲 Bagging vs Boosting, L1 vs L2         |
| **分类 Mini-Project**: 用 Online Retail 做 Churn (简化版) |    2h    | 能说出 "LR baseline → XGBoost, AUC 0.85"           |

#### ❌ 砍掉 (Cut)
- ~~Walmart 高阶调优 (Optuna/GridSearch 实操)~~ → 面试用 Optuna 伪代码即可
- ~~Walmart 分层评估极值优化~~ → 面试用话术防守
- ~~完整 K-Fold 代码实操~~ → 面试能讲原理即可

---

### 📍 W3 (2/17 - 2/23): 因果推断 + A/B 实战 🎯

> **核心原则**: 这周的目标是**简历防守**，不是学术研究。聚焦简历里提到的 DID/PSM/A/B Test。

#### 🔴 简历项目 2: 人力调度 → 因果推断验证
*简历原文: "设计随机对照实验验证 AI 预测排班 vs 人工经验排班, 使用 Delta Method 校正比率指标方差"*

| 任务                                                | 预计时间 | 面试防守目标                  |
| :-------------------------------------------------- | :------: | :---------------------------- |
| **DID 实操**: 用模拟数据跑一遍 DID (双重差分)       |    2h    | 能手写 DID 公式 + 代码        |
| **PSM 实操**: 用模拟数据跑一遍 PSM (倾向性得分匹配) |    2h    | 能解释 "为什么要先匹配再差分" |
| **平行趋势检验**: 画图 + 安慰剂检验                 |    1h    | 能回答 "平行趋势不满足怎么办" |

#### 🔴 简历项目 3: A/B 实验平台 → 高阶实战
*简历原文: "分层重叠实验框架, SRM 诊断, CUPED"*

| 任务                                                         | 预计时间 | 面试防守目标                               |
| :----------------------------------------------------------- | :------: | :----------------------------------------- |
| **A/B Test 完整 Case**: 设计→执行→分析→结论                  |    2h    | 能白板画出实验设计流程图                   |
| **Delta Method 实操**: 用 CTR 数据演示 Ratio Metric 方差估计 |    1h    | 能写出公式 + 解释为什么不能直接 t-test     |
| **CUPED 概念**: 方差缩减原理 (不需要写代码)                  |   0.5h   | 能解释 "为什么加 Pre-experiment covariate" |

#### 🟡 ML 理论巩固 (穿插进行)
| 任务                               | 方式                  |
| :--------------------------------- | :-------------------- |
| Sigmoid / Weights / Regularization | 2C 分类项目中边做边讲 |
| K-Fold / Stratified K-Fold         | 因果推断代码中使用 CV |

---

### 📍 W4 (2/24 - 3/2): 面试准备 🎤

> **核心原则**: 不再写新代码，全力 STAR 故事 + Mock Interview。

| 任务                                      | 预计时间 | 产出                        |
| :---------------------------------------- | :------: | :-------------------------- |
| **STAR 故事打磨** (3个)                   |    3h    | VoC + 调度 + A/B 实验各一个 |
| **简历定稿**                              |    1h    | 最终版 Packaged_Resume.md   |
| **Mock Interview** (Agent 模拟)           |    2h    | 录制 + 复盘                 |
| **SQL 刷题** (LeetCode Medium ×5)         |    2h    | 保持手感                    |
| **理论复习**: StatQuest 视频 + 知识库增补 |    2h    | 每天看 1 个视频             |

---

### 📍 W5 (3/3 - 3/13): 密集面试 🏁

| 目标公司 | 岗位              | 策略                       |
| :------- | :---------------- | :------------------------- |
| **阿里** | 客服智能/天猫运营 | VoC 差异化，NLP + A/B Test |
| **美团** | 外卖/到店运营     | 调度优化 + 因果推断        |
| **京东** | 供应链分析        | 时序预测 + Pipeline        |

**底线**: 25w | **目标**: 30w | **冲刺**: 35w

---

### ⚠️ 不做清单 (Anti-Goals)

> [!WARNING]
> 以下事项在 3/13 之前**不要做**，防止分心：

- ❌ 不追求完美的 Walmart 模型 (MAPE < 10%)
- ❌ 不学 Deep Learning / Transformer / CNN
- ❌ 不花时间在 Kaggle 竞赛
- ❌ 不重构知识库 MkDocs 结构
- ❌ 不做 LiuliX 功能开发
- ❌ 不学新工具 (Spark/dbt)

---

## 🔮 导师寄语 (Re-calibration)
> 你现在最大的风险不是"技术不够"，而是**"学得太多但说不清楚"**。
> 面试官问的不是"你会不会 XGBoost"，而是"你为什么选 XGBoost 而不是 LR？Tradeoff 是什么？"
> 接下来 26 天的核心任务是：**把你已经做过的事情讲得滴水不漏**。
> Let's close this sprint strong! 💪
