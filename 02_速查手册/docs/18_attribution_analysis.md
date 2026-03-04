# 🕵️ 归因分析 (Attribution Analysis)

> **核心逻辑**: 在多渠道营销中，用户往往接触了多个触点 (Touchpoints) 才最终转化。如何科学地分配“功劳”？
> **关系**: 归因分析是 **因果推断 (Causal Inference)** 在 **营销科学 (Marketing Science)** 领域的特例。它本质上是在回答反事实问题：“如果没有这个渠道，转化率会跌多少？”

## 1. 核心挑战

传统的归因模型往往基于规则 (Rule-based)，存在明显缺陷：

*   **Last Click (末次点击)**: 忽略了种草渠道的贡献 (e.g. 小红书种草，淘宝搜索购买 → 淘宝全拿功劳)。
*   **First Click (首次点击)**: 忽略了临门一脚的转化。
*   **Linear (线性归因)**:大锅饭，无法区分渠道真实价值。

我们需要 **基于算法的归因 (Data-driven Attribution)**。

## 2. 马尔可夫链归因 (Markov Chain Attribution)

### 2.1 原理
将用户的转化路径视为一连串的状态转移。

*   **状态 (State)**: 渠道 (e.g. Start, Ads, Search, Social, Conversion, Null)。
*   **转移概率 (Transition Probability)**: 从一个渠道跳到另一个渠道的概率。

### 2.2 核心指标：移除效应 (Removal Effect)
这是因果推断思想的体现：
$$ Removal\ Effect = 1 - \frac{Conversion(Total\ without\ X)}{Conversion(Total)} $$

> **直觉**: 如果把渠道 X 彻底关掉 (从图中抹去)，总转化率会下降多少？下降得越多，说明它越重要。

### 2.3 代码实现 (Python)

??? example "Markov Chain 归因代码模板"

    ```python
    import pandas as pd
    from pychattr.channel_attribution import MarkovModel

    # 1. 准备数据: Path (路径String) + Conversion (次数) + Null (未转化次数)
    data = {
        "path": ["Start > Social > Search > Conversion", "Start > Ads > Conversion"],
        "conversions": [10, 5],
        "null_conversions": [100, 50]
    }
    df = pd.DataFrame(data)

    # 2. 建模
    # pychattr 是常用的归因库 (需 pip install pychattr)
    # 或者手写状态转移矩阵
    path_feature="path"
    conversion_feature="conversions"
    null_feature="null_conversions"

    mm = MarkovModel(
        path_feature=path_feature,
        conversion_feature=conversion_feature,
        null_feature=null_feature,
        separator=" > ",
        k_order=1 # 一阶马尔可夫 (只看前一步)
    )

    mm.fit(df)

    # 3. 输出移除效应
    print(mm.removal_effects_)
    ```

## 3. Shapley Value (博弈论归因)

### 3.1 原理
源自合作博弈论 (Cooperative Game Theory)。
*   **思想**: 考虑所有渠道的 **排列组合** (Permutations)。
*   **计算**: 只要有渠道 X 参与的组合，转化率提升了多少？(Marginal Contribution)。最后取平均值。

### 3.2 特点
*   **优点**: 数学上被证明是 **最公平** 的分配方式。
*   **缺点**: 计算量是指数级增长 ($2^N$)，渠道多了算不动。
*   **应用**: 通常作为 Markov 结果的校验基准 (Ground Truth)。

## 4. 业务应用 (Actionable Insights)

拿到归因结果后，你可以做三件事：

1.  **预算分配 (Budget Allocation)**: 
    *   移除效应高的渠道 (High Removal Effect) → **加预算/保预算**。
    *   Last Click 虚高但移除效应低的渠道 → **砍预算** (它是收割者，不是种草者)。
2.  **渠道定位 (Channel Role)**:
    *   利用转移矩阵可视化：谁总是指向 Conversion (收割位)？谁总是指向其他渠道 (种草位)？
3.  **ROAS 修正**:
    *   用归因后的权重重新计算 ROAS，往往会发现 Display/Social 广告被低估了。
