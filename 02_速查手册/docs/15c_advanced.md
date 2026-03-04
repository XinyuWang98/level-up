# 🧪 进阶方法 (RDD/IV)

> **本页覆盖**：断点回归 (RDD)、工具变量 (IV)、格兰杰因果检验 (Granger)、面试 FAQ

| 方法        | 适用场景                         | 核心假设            | 估计量   |
| :---------- | :------------------------------- | :------------------ | :------- |
| **RDD**     | 有自然断点/阈值 (如考分、年龄线) | 阈值附近局部随机    | LATE     |
| **IV**      | 存在不可观测混淆，但有工具变量   | 排他性约束 + 相关性 | LATE     |
| **Granger** | 时序预测关系 (非真因果)          | 平稳性              | 预测能力 |

## 5. RDD (断点回归 - Regression Discontinuity Design)

### 5.1 原理
*   **核心思想**: 利用规则的 **"一刀切" (Cutoff)** 制造局部随机实验。
*   **场景**: 奖学金 (考分>600), 贫困补助 (收入<1000), 促销 (满100减20)。
*   **逻辑**: 在阈值附近 (e.g. 599分 vs 601分)，两群人的能力几乎没有区别，唯一的区别是 "是否拿到奖学金"。因此，阈值处的跳跃就是因果效应。

### 5.2 代码模板 (Python)

??? example "RDD 完整代码 (点击展开)"

    ```python
    import statsmodels.formula.api as smf

    # 1. 数据准备
    # running_variable: 驱动变量 (e.g. 考分)
    # cutoff: 阈值 (e.g. 600)
    df['is_treated'] = (df['score'] >= 600).astype(int)

    # 2. 中心化 (Centering) - 关键步骤!
    # 让截距项直接代表阈值处的效应
    df['score_centered'] = df['score'] - 600

    # 3. 运行回归 (Sharp RDD)
    # 允许断点左右斜率不同 (Interaction Term)
    model = smf.ols("outcome ~ score_centered * is_treated", data=df).fit()

    # is_treated 的系数就是 LATE (Local Average Treatment Effect)
    print(model.summary())
    ```

---

## 6. IV (工具变量 - Instrumental Variable)

### 6.1 原理

*   **核心思想**: 当存在无法观测的混淆变量 (e.g. 能力) 时，找到一个 **"上帝之手" (Z)**，它只影响干预 (T)，不直接影响结果 (Y)。
*   **场景**:

    *   **T**: 读书时长 → **Y**: 收入 (混淆: 智商)。
    *   **Z**: 距离图书馆的距离 (只影响读书时长，不直接影响收入)。

### 6.2 两阶段最小二乘法 (2SLS)
1.  **第一阶段**: 用 Z 预测 T ( $\hat{T}$ )。
2.  **第二阶段**: 用 $\hat{T}$ 预测 Y。

### 6.3 代码模板 (Python)

```python
from linearmodels.iv import IV2SLS

# 公式: Outcome ~ Exogenous + [Endogenous ~ Instruments]
# 1 代表截距项
# [] 内左边是内生变量 (要"提纯"的)，右边是工具变量
iv_model = IV2SLS.from_formula(
    'income ~ 1 + [education ~ distance_to_library] + age + gender', 
    data=df
).fit()

print(iv_model)
```

!!! warning "语法大坑：多个内生变量必须合并在一个 `[]` 中"
    `linearmodels` 只允许一个 `~` 分隔符在 `[]` 内。

    ```python
    # ❌ 错误写法 (ValueError: formula contains more then 2 separators)
    'Y ~ [X1 ~ Z1] + [X2 ~ Z2] + W'
    
    # ✅ 正确写法 (所有 Endog 放左边，所有 Instr 放右边)
    'Y ~ 1 + W + [X1 + X2 ~ Z1 + Z2]'
    ```

!!! warning "Exclusion Restriction (排他性约束) 铁律"
    工具变量 Z **不能直接影响** Y，只能通过 T 间接影响。
    
    **常见错误**: 把 Confounder (如 `income`) 当作 Instrument。`income` 既影响 `is_member` 又直接影响 `ltv`，违反排他性约束，估计值会严重偏高。
    
    **速查**: 问自己 "如果 Treatment 不存在，Z 还会影响 Y 吗？" 如果会，就不能用。

---

## 7. Granger Causality (格兰杰因果检验)

### 7.1 原理

*   **核心思想**: 并不是真正的因果，而是 **"预测能力" (Predictive Causality)**。
*   **逻辑**: 如果 X 的历史信息能提高对 Y 的预测精度 (比只用 Y 的历史预测 Y 更好)，则称 X 格兰杰导致 Y。
*   **场景**: 宏观经济 (GDP vs 股市)、营销 (广告投放 vs 销量)。

### 7.2 代码模板 (Python)

```python
from statsmodels.tsa.stattools import grangercausalitytests

# 检验 X 是否 Granger-cause Y
# maxlag: 滞后期数 (e.g. 过去 7 天)
res = grangercausalitytests(df[['Y', 'X']], maxlag=7)
```


---

## 8. 稳健性检验 (Robustness Checks)

> 📦 **已整合**：完整的稳健性检验 SOP（安慰剂检验、合成控制、DoWhy refute、平衡性检验、反向因果等）已统一整合到一个页面。
>
> 🔗 请参考 → [🛡️ 稳健性检验 (SC/Placebo)](15d_synthetic_control_placebo.md)

---

## 9. 面试高频问题 (Interview Q&A)

??? question "Q1: 什么时候用 DID，什么时候用 PSM？"
    *   **DID**: 适用于 **面板数据 (Panel Data)**，即有时间维度的前后对比 (Pre-Post)。要求满足平行趋势假设。
    *   **PSM**: 适用于 **横截面数据 (Cross-sectional Data)**，或者是虽然有时间维度但无法满足平行趋势的情况。PSM 只能消除 **可观测变量 (Observed Variables)** 的偏差。
    *   **速记**: 参考上方 [方法选型决策树](#step-3-方法论选型-method-selection-decision-tree) 的 Mermaid 图。

??? question "Q2: 如果不满足平行趋势假设怎么办？"
    *   **PSM-DID**: 先做 PSM 匹配找到相似的组，再对匹配后的样本做 DID。
    *   **合成控制法 (Synthetic Control)**: 用多个对照组加权合成一个虚拟对照组。

??? question "Q3: 为什么不直接把所有特征丢进 XGBoost 预测 Y？"
    *   **解释性**: XGBoost 只能告诉你 `Feature Importance`，不能告诉你 `Treatment Effect` (因果效应)。
    *   **混杂**: 如果不专门处理，模型可能会学到错误的虚假相关 (Spurious Correlation)。

??? question "Q4: PSM 的 Common Support 问题怎么处理？"
    *   **问题**: Treated 组的 Propensity Score 分布和 Control 组不重叠，导致匹配质量差。
    *   **诊断**: 画 PS 分布图 (`sns.kdeplot`)，检查是否有 overlap。
    *   **解决**: **Trimming (截断法)** —— 只保留两组 PS 交叉的区域 (`ps_min` ~ `ps_max`)。
    *   **验证**: 匹配后跑 Balance Check，所有特征的 SMD < 0.1。

??? question "Q5: OLS 控制变量 vs PSM 有什么区别？"
    *   **OLS 控制变量**: 假设线性关系，直接在回归中加入混淆变量。适合变量少、关系简单的情况。
    *   **PSM**: 不假设函数形式，通过匹配实现 "pseudo-randomization"。适合变量多、关系复杂的情况。
    *   **实战建议**: 两者都跑，结果一致则增强信心 (Robustness)。

??? question "Q6: 如何向非技术 Stakeholder 解释因果推断结果？"
    *   **模板**: "我们通过 [方法名] 排除了 [混淆因素] 的干扰，发现 [Treatment] 对 [Outcome] 的净效应是 [X 元/X%]，统计置信度超过 95%。"
    *   **关键**: 强调 "净效应" 和 "排除干扰"，不要说 P 值。
    *   **类比**: "就像做药物临床试验，我们给一组人吃药，另一组人吃安慰剂，对比结果。"

??? question "Q7: 因果推断的局限性是什么？"
    *   **不可测变量**: PSM/IPW/DML 都只能处理 **可观测的** 混淆变量，如果有遗漏的不可测变量 (e.g. 用户动机)，估计仍然有偏。
    *   **外推风险**: RDD 和 IV 估计的是 **LATE (局部效应)**，不能直接推广到全体人群。
    *   **数据要求**: DID 需要面板数据 + 平行趋势，RDD 需要明确阈值，IV 需要好的工具变量 —— 现实中很难全部满足。

---
