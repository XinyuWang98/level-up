# 机器学习系统设计：模型监控与大厂落地架构

在目标大厂、美团等大厂的高阶数据分析/挖掘面试中，除了问“你怎么训练出 XGBoost 的？”，更致命的问题通常是：“**模型上线以后呢？你怎么证明它还在起作用？如果变差了怎么办？**”
本指南涵盖了系统设计中最核心的两大考点：**模型漂移监控 (Model Drift)** 和 **数据闭环质检 (Active Learning)**。

---

## 📉 1. 监控与重训体系: Model Drift (模型漂移)

### 1.1 什么是模型漂移？
在推荐系统、预测模型中，昨日之日不可留。你今天训练的完美模型，下个月表现可能会惨不忍睹。这就是漂移。通常分为两类：
* **概念漂移 (Concept Drift)**：用户目标变了。过去大家买口罩是因为疫情，现在买口罩是因为防晒。输入特征 $X$ 没变，但真实的预测目标 $Y$ 和 $X$ 之间的映射关系变了。
* **数据漂移 (Data Drift / Covariate Shift)**：输入分布变了。比如你的模型是在发达城市人群上训练的，后来业务下沉扩展到了三四线城市，人群特征 $X$ 的统计学分布彻底变了，导致原来稳健的模型“水土不服”。

### 1.2 监控与自动重训架构设计 (The Pipeline)

你要向面试官展示出你懂 MLOps，懂如何用 **Airflow** 把整个生命周期串起来。

> [!TIP]
> **标准 高级专家 级面试回答框架 ("Airflow DAG 定时任务闭环")**:
> 
> "在我的模型上线后，我会设定三级监控体系，并用 Airflow 设置不同的 DAG 触发条件。"
> 
> 1. **数据分布监控 (Data Quality Checks)**: 每天新数据入库时，跑一次 PSI (Population Stability Index)。如果输入特征分布发生急剧偏移（$PSI > 0.2$），我会触发告警邮件，并在下游截断模型预测，转为降级的人工或规则策略。
> 2. **下游指标与误差监控 (Performance Checks)**: 比如我的客服话务量预测模型，每周五晚我会对这一周的历史预测和真实 Ground Truth 计算 MAPE （比如设置阈值为 15%）。如果近两周 MAPE 连续超过阈值，说明可能发生了概念漂移。
> 3. **自动触发重训 (Auto-Retraining)**: 在 Airflow 中配置一个 Sensor。只有当监控器报出漂移警告（或是定期每月初），并且新积累的样本量达到 $N$ 条以上时，触发“再训练 DAG”。新模型训练出来后并不是立刻替换，而是采用**影子模式 (Shadow Mode)** 跑三天预测（不干预业务），或者在 A/B 测试实验区分配 5% 流量对比旧模型，确认真的有提升后才滚动部署（Rolling Update）。

### 1.3 PSI (群体稳定性指标) 的计算逻辑

PSI 是判断 Data Drift 最经典的工业级防线：

$$PSI = \sum (\text{Actual \%} - \text{Expected \%}) \times \ln\left(\frac{\text{Actual \%}}{\text{Expected \%}}\right)$$

```python
import numpy as np
import pandas as pd

def calculate_psi(expected, actual, buckets=10):
    """
    计算预期分布（训练集）和实际分布（线上新数据）之间的 PSI
    :param expected: 训练集上的某个特征 Array
    :param actual: 线上近期产生的新特征 Array
    """
    # 构造分段的分位数边界
    breakpoints = np.percentile(expected, np.arange(0, 101, 100 / buckets))
    breakpoints[0] = -np.inf
    breakpoints[-1] = np.inf

    # 计算预期的占比分布 (Expected %)
    expected_perc = np.histogram(expected, breakpoints)[0] / len(expected)
    # 计算实际新数据的占比分布 (Actual %)
    actual_perc = np.histogram(actual, breakpoints)[0] / len(actual)

    # 替换 0，防止 log(0) 报错
    expected_perc = np.where(expected_perc == 0, 0.0001, expected_perc)
    actual_perc = np.where(actual_perc == 0, 0.0001, actual_perc)

    # PSI 核心公式
    psi_value = np.sum((actual_perc - expected_perc) * np.log(actual_perc / expected_perc))

    # 判断结论
    if psi_value < 0.1:
        status = "🟢 绿灯：特征分布稳定"
    elif psi_value < 0.2:
        status = "🟡 黄灯：轻微偏移，需要持续关注"
    else:
        status = "🔴 红灯：发生显著数据漂移 (Data Drift)，建议暂停或重训"
        
    return psi_value, status

# 使用示例
# psi_score, alert = calculate_psi(df_train['user_age'], df_deployed['user_age'])
```

---

## 🤖 2. 自动化质检与 Active Learning (主动学习)

结合您简历中提到的 **"智能客服体验优化与流失归因 (VoC System)"**，如果在面试时提到“文本挖掘模型”和“自动打标签”，接下来必然会受到灵魂拷问：
**“一开始没数据怎么办？打标成本那么高，你是怎么冷启动，并持续提升数据集质量的？”**

### 2.1 什么是主动学习 (Active Learning)？
**痛点**：标注一条客服对话的“意图标签”需要 1-2 分钟，海量数据全量人工标注成本是不现实的。如果随便抽样让模型学，模型往往只会学会最简单的日常寒暄，遇到罕见疑难杂症 (Corner Cases) 常常误判。
**解法**：**让模型“自己决定”哪些数据值得被人工标注。** 模型如果对某句话的预测概率极不确定（例如：51% 是问物流，49% 是退换货），那这句话就是模型目前的“软肋”，把它拿去给质检员人肉精标，收益最大。

> [!IMPORTANT]
> **简历 STAR Story - Active Learning 的业务闭环**:
> “在构建我的 VoC (Voice of Customer) 意图识别体系时，我没有像传统分析师那样申请大量预算外包打标。我设计了一套基于 **Active Learning 的数据飞轮 (Data Flywheel)**：
> 1. 先用 **弱监督规则 (TF-IDF/关键词正则)** 对 5% 数据做弱打标，训练出 M0 初始分类器 (如 LightGBM)。
> 2. 用 M0 扫描全量海量无标签的实时会话流，输出每个类别的概率分布。
> 3. 我提取出 **预测置信度最低** (如 Top1 和 Top2 类别概率差值最小：Margin Sampling)、以及 **罕见高警报特征** 的样本。
> 4. 我每天只圈取这 200 条最难判断的“盲区样本”，推送到客服质检后台让高级主管精标。
> 5. 这批“高质量硬骨头样本”隔天自动回流数据库训练 M1 模型。
> **业务收益**：以 1/10 的人工质检抽样量（也就是节约了巨大的人力成本），快速逼近了 90% 的意图分类准召率。”

### 2.2 Active Learning - Uncertainty Sampling 代码框架

最常用的方法是 **不确定度采样 (Uncertainty Sampling)** 中的 **边缘采样 (Margin Sampling)**。

```python
import numpy as np

def query_uncertain_samples(model_proba_preds, top_n=200):
    """
    通过边缘采样寻找模型最不确定的样本，推送给人工精标
    :param model_proba_preds: 分类器对无标签样本预测的概率分布矩阵 (shape: [num_samples, num_classes])
    :param top_n: 需要挑给人工标注的样本数
    :return: 最不确定的样本索引列表
    """
    # 按照概率对每个样本的所有类别得分进行排序 (从小到大)
    sorted_probas = np.sort(model_proba_preds, axis=1)
    
    # 提取最大的概率 (Top-1) 和第二大的概率 (Top-2)
    highest_prob = sorted_probas[:, -1]
    second_highest_prob = sorted_probas[:, -2]
    
    # 计算 Margin (边缘差 = Top-1概率 - Top-2概率)
    # 这个差值越小，说明模型越在两个标签之间犹豫不决，最容易出错！
    margin = highest_prob - second_highest_prob
    
    # 提取 Margin 最小的 top_n 个样本的索引 (Argsort 默认从小到大排)
    uncertain_indices = np.argsort(margin)[:top_n]
    
    return uncertain_indices

# --- 模拟运行 ---
# predict_proba 返回了未标注数据属于(物流, 退款, 尺码等)各个类别的概率
# probas = lgb_model.predict_proba(X_unlabeled_tfidf)
# 圈出模型最纠结的 200 条记录
# hard_cases = query_uncertain_samples(probas, top_n=200)

# 然后你把 df_unlabeled.iloc[hard_cases] 导出给客服团队做人肉评级。这就是数据闭环！
```
