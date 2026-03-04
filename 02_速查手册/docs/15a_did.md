# 📊 DID (双重差分)


## 2. DID (双重差分 - Difference in Differences)

### 2.1 原理

用于 **政策评估** 或 **自然实验**。

*   **公式**: `(Treatment_Post - Treatment_Pre) - (Control_Post - Control_Pre)`
*   **直觉**: (干预组的变化量) - (对照组的自然增长量) = 净干预效应。

#### DID 全流程 SOP (7 步)

| Step  | 名称                 | 核心动作                                                               | 关键判断                          |
| :---- | :------------------- | :--------------------------------------------------------------------- | :-------------------------------- |
| **0** | **适用性判断**       | 确认面板数据 + 明确干预时点 + 分组外生                                 | 缺一不可                          |
| **1** | **EDA**              | 折线图 + 干预标记线 `plt.axvline`                                      | 直觉判断趋势                      |
| **2** | **平行趋势检验**     | L1 可视化 → L2 分组斜率 → L3 OLS `week*is_treated` (仅干预前数据)      | `week:is_treated` P > 0.05 → 通过 |
| **3** | *(如需)* **PSM+DID** | Logistic → 倾向得分 → 匹配/IPW → 检查 Common Support → 再跑 DID        | PS 分布需有重叠                   |
| **4** | **DID 回归**         | `Y ~ is_treated * is_post`                                             | `is_treated:is_post` 系数 = ATE   |
| **5** | **Event Study**      | 构建 `relative_week` → pyfixest `i(relative_week, is_treated, ref=-1)` | 干预前 ≈ 0, 干预后显著            |
| **6** | **Placebo 检验**     | 假时间 (干预前数据提前切分) + 假对象 (对照组随机拆分)                  | 两项 P > 0.05 → 通过              |
| **7** | **业务汇报**         | Executive Summary: 背景→方法→结果→建议                                 | 能用非技术语言讲清                |

!!! warning "Step 3 常见误区"

    PSM **不是构造新的实验/对照组**，而是对已有样本**重新配对或加权**，让两组在协变量上"齐平"。截断 (Trimming) 取决于 **Common Support** (倾向得分分布是否重叠)，而非单纯的样本量。

### 2.2 核心假设：平行趋势 (Parallel Trends)

*   **定义**: 如果没有干预，干预组和对照组的趋势应该是平行的。
*   **检验方法 (三层递进)**:

| 层级 | 方法           | 做法                     | 严谨度 |
| :--- | :------------- | :----------------------- | :----- |
| L1   | **可视化**     | 画折线图看是否平行       | ⭐      |
| L2   | **分组斜率**   | 分别拟合斜率，人工比较   | ⭐⭐     |
| L3   | **交互项检验** | 一个模型直接检验斜率差异 | ⭐⭐⭐    |

!!! tip "为什么 L3 比 L2 更严谨？"

    分组看斜率只告诉你"各自的斜率是多少"，但没有直接检验 **两个斜率之间的差异** 是否显著。交互项检验把两组放进同一个模型，直接输出斜率差的 P-value，考虑了两个估计各自的不确定性如何叠加。

    **常见陷阱**: 斜率点估计看着差很多 (如 5.0 vs 1.2)，但样本小 + 噪声大时，P-value 仍可能 > 0.05。这说明这个差异可能纯靠随机波动产生。

### 2.3 代码模板 (Python)
使用 `statsmodels` 运行 OLS 回归：`Y ~ Treat + Post + Treat:Post`。

??? example "DID 完整代码 (点击展开)"

    ```python
    import pandas as pd
    import statsmodels.formula.api as smf
    import seaborn as sns
    import matplotlib.pyplot as plt

    # 数据准备
    # df 包含: 'Sales', 'City' (0=Control, 1=Treat), 'Time' (0=Pre, 1=Post)

    # 1. 可视化检验平行趋势 (Visual Inspection)
    # 自动定位干预线: (Post=0的最大时间 + Post=1的最小时间) / 2
    pre_max = df[df['Time'] < 5]['Time'].max() # 注意: 实战中应用 df[df['Post']==0]
    post_min = df[df['Time'] >= 5]['Time'].min()
    intervention_x = (pre_max + post_min) / 2

    plt.figure(figsize=(10, 6))
    # err_style='bars': 显示置信区间
    sns.lineplot(data=df, x='Time', y='Sales', hue='City', err_style='bars')
    plt.axvline(x=intervention_x, color='red', linestyle='--', label='Intervention Start')
    plt.title("Parallel Trend Check")
    plt.legend()
    plt.show()

    # 2. 科学检验: 斜率一致性 (Slope Consistency Check)
    # 逻辑: 取干预前 (Pre-intervention) 数据，分别计算两组的回归斜率。
    df_pre = df[df['Time'] < 5]

    slopes = []
    for city in [0, 1]:
        # 简单回归: Sales ~ Time
        model_pre = smf.ols("Sales ~ Time", data=df_pre[df_pre['City'] == city]).fit()
        slopes.append({
            'City': 'Control' if city==0 else 'Treated',
            'Slope': model_pre.params['Time'],
            'P_value': model_pre.pvalues['Time'],
            'R2': model_pre.rsquared
        })
    print(pd.DataFrame(slopes))

    # 3. ⭐ 交互项检验 (更严谨，推荐用这个)
    # 原理: Time:City 的系数 = 两组斜率之差
    #   如果 P > 0.05 → 斜率差不显著 → 平行趋势成立 ✅
    #   如果 P < 0.05 → 斜率差显著 → 平行趋势可能不成立 ⚠️
    model_parallel = smf.ols("Sales ~ Time * City", data=df_pre).fit()
    interaction_p = model_parallel.pvalues['Time:City']
    print(f"交互项 P-value = {interaction_p:.4f}")
    print(f"结论: {'✅ 平行趋势成立' if interaction_p > 0.05 else '⚠️ 考虑 PSM-DID'}")

    # 4. 运行 DID 模型
    # 公式 "Sales ~ City * Post"
    model = smf.ols("Sales ~ City * Post", data=df).fit()
    print(model.summary())
    ```

---

### 2.4 DID 业务汇报模版 (Business Reporting Template)

> **场景**: 老板问你 "这次活动到底提升了多少销售额？模型靠谱吗？"
> **输入**: `model.summary()` 的结果。
> **公式**: `Sales = Intercept + City + Post + City:Post`

#### 1. 系数解读 (Coefficient Interpretation)

| 参数 (Term)   | 系数 (Coef) | 统计学含义 | **业务人话 (Business Insight)**                                                 |
| :------------ | :---------- | :--------- | :------------------------------------------------------------------------------ |
| **Intercept** | 521.4       | 截距       | **基准销量**: 对照组在活动前的自然销量。                                        |
| **City**      | 50.8        | 组间差异   | **体量差距**: "实验组哪怕不做活动，平时也比对照组多卖 50 块。" (Selection Bias) |
| **Post**      | 46.8        | 时间趋势   | **自然增长**: "不管做不做活动，随时间推移大家都会多卖 46 块。" (Time Trend)     |
| **City:Post** | **100.5**   | **交互项** | **净增量 (DID Effect)**: "剔除体量差距和自然增长后，活动带来的**真实提升**。"   |

#### 2. 统计显著性 (Significance)

*   **P > |t|**: 必须 **< 0.05** (最好是 0.000)。
    *   *话术*: "置信度超过 95%，结果不是随机波动。"
*   **R-squared**: 拟合优度 (e.g., 0.677)。
    *   *话术*: "模型解释了 67.7% 的销量波动，说明主要因素都考虑进去了。"
*   **Conf. Interval**: 置信区间 (e.g., [94.7, 106.2])。
    *   *话术*: "我们有 95% 的把握，真实提升在 94-106 元之间。"

#### 3. 汇报话术示例 (Script)

> "老板，经过因果推断模型测算，本次促销活动为单店带来 **平均 100.5 元的净销售额提升** (DID Effect)。"
>
> "如果我们直接对比活动前后，会误以为提升了 **147 元** (包含 46 元自然增长)；直接对比实验组和对照组，会误以为提升了 **151 元** (包含 50 元门店体量差距)。"
>
> "我们的模型剥离了这些干扰因素，锁定了真实的促销效果。统计置信度超过 **99.9%**，结论非常稳健。"

---

### 2.5 Event Study (动态因果效应) ⭐ *进阶必备*

!!! info "Event Study 是什么？"

    标准 DID 只能告诉你 **"活动有没有效"** (一个数字)。
    Event Study 能告诉你 **"活动哪一期最有效、效果是否在消退"** (一条曲线)。

    **核心逻辑**: 不再把所有 Post 期合并成一个系数，而是**逐期估计**因果效应。

#### 原理：逐期交互项回归

$$
Y_{it} = \alpha_i + \lambda_t + \sum_{k \neq 0} \beta_k \cdot (\text{Treated}_i \times \mathbb{1}[t - t^* = k]) + \varepsilon_{it}
$$

| 符号        | 含义                                  |
| :---------- | :------------------------------------ |
| $\alpha_i$  | 个体固定效应 (城市间的固有差异)       |
| $\lambda_t$ | 时间固定效应 (自然增长趋势)           |
| $t^*$       | 干预开始的时间点 (基准期，系数设为 0) |
| $\beta_k$   | **第 k 期的 DID 效应** (核心输出)     |

!!! tip "面试速记"
    - **Pre-treatment 的 $\beta_k$ 应接近 0** → 验证平行趋势
    - **Post-treatment 的 $\beta_k$ 应显著为正** → 因果效应
    - $\beta_k$ 递减 → 效果消退；$\beta_k$ 递增 → 长尾效应

!!! warning "基准期 (ref) 的选择至关重要"

    | `ref` 选择         | 含义                 | Pre 系数期望                  | 推荐场景           |
    | :----------------- | :------------------- | :---------------------------- | :----------------- |
    | **`ref=-1`** ⭐推荐 | 干预前最后一期为基准 | **≈ 0** (直观判断平行趋势)    | 面试、标准报告     |
    | `ref=0`            | 干预当期为基准       | **负数** (正常，因为还没干预) | 也可，但解读不直观 |

    **面试注意**: 如果用 `ref=0`，干预前系数为负 **不代表平行趋势不通过**，只是说明干预前的 treated-control 差距比干预当期小 (还没干预当然小)。用 `ref=-1` 更清晰。

#### 代码模板

=== "🔧 手动挡 (statsmodels)"

    适合 **学习原理** 和 **面试现场手写**。

    ```python
    import statsmodels.formula.api as smf
    import matplotlib.pyplot as plt
    import pandas as pd

    # 1. 构造相对时间 (以干预前最后一期为基准)
    TREATMENT_START = 7  # 活动从 Week 7 开始
    df['week_relative'] = df['week'] - TREATMENT_START  # -1 = 干预前最后一期

    # 2. 回归: 交互项 + 取 -1 期为基准 (⭐ 面试标准做法)
    model_event = smf.ols(
        'orders ~ is_treated + C(week_relative, Treatment(-1)) + '
        'is_treated:C(week_relative, Treatment(-1))',
        data=df
    ).fit()

    # 3. 提取交互项系数 (动态效应)
    event_study_results = []
    for param_name, coef in model_event.params.items():
        if 'is_treated:C(week_relative' in param_name:
            week_num = int(float(param_name.split('[T.')[1].rstrip(']')))
            ci = model_event.conf_int().loc[param_name]
            event_study_results.append({
                'week_relative': week_num,
                'effect': coef,
                'ci_lower': ci[0], 'ci_upper': ci[1],
                'p_value': model_event.pvalues[param_name]
            })

    # 加上基准期 -1 (效应 = 0，不出现在回归结果里)
    event_study_results.append({
        'week_relative': -1, 'effect': 0,
        'ci_lower': 0, 'ci_upper': 0, 'p_value': 1.0
    })
    es_df = pd.DataFrame(event_study_results).sort_values('week_relative')

    # 4. 可视化
    plt.figure(figsize=(10, 5))
    plt.errorbar(es_df['week_relative'], es_df['effect'],
                 yerr=[es_df['effect'] - es_df['ci_lower'],
                       es_df['ci_upper'] - es_df['effect']],
                 fmt='o-', capsize=4, color='steelblue', markersize=8)
    plt.axhline(y=0, color='gray', linestyle=':')
    plt.axvline(x=0, color='red', linestyle='--', label='干预开始')
    plt.title('Event Study: 动态因果效应')
    plt.xlabel('相对干预的时期'); plt.ylabel('DID 效应')
    plt.legend(); plt.grid(alpha=0.3); plt.show()
    ```

=== "🚀 自动挡 (pyfixest, 推荐)"

    3 行代码完成建模 + 出图。需要 **Python ≥ 3.10**。

    ```python
    import pyfixest as pf

    # 1. 构造相对时间
    TREATMENT_START = 7
    df['week_relative'] = df['week'] - TREATMENT_START

    # 2. 一行建模
    # i(week_relative, is_treated, ref=-1): ⭐ 基准期 = 干预前最后一期
    # | city: 城市固定效应
    fit = pf.feols(
        "orders ~ i(week_relative, is_treated, ref=-1) | city",
        data=df,
        vcov={'CRV1': 'city'}  # 按城市聚类标准误
    )

    # 3. 一行画图
    pf.iplot(fit, figsize=(10, 5),
             title='Event Study (pyfixest)')
    ```

    > `pyfixest` 是 R 语言 `fixest` 的 Python 移植版，底层优化过，
    > 百万级数据也能秒算。`i()` 语法自动处理交互项和基准期。

#### 如何解读 Event Study 图

```
     Effect (ref = -1)
  80 │               ●────●────●────●────●   ← Post: 显著正效应
  60 │             /
  40 │           /
  20 │         ●
   0 │──●────●────●────●──┤                  ← Pre: 接近 0 ✅ (平行趋势)
 -20 │                    │
     └──────────────────────────────────→ 时间
     -4  -3  -2  -1   0   1   2   3   4
                  ↑ 基准期 (ref=-1, 系数强制=0, 不显示)
```

| 区域                      | 期望                      | 如果不符合                       |
| :------------------------ | :------------------------ | :------------------------------- |
| **Pre-treatment** (左半)  | 所有系数 ≈ 0，CI 穿过零线 | 平行趋势不成立 → 考虑 PSM-DID    |
| **Post-treatment** (右半) | 系数为正且显著            | 若不显著 → 效果不明确            |
| **趋势**                  | 看系数是递增还是递减      | 递减 = 效果衰退，递增 = 累积效应 |

#### Pre-treatment 系数不全为 0？分情况处理

!!! tip "面试决策树"

    ```
    干预前系数是否 ≈ 0？
    │
    ├── 全部 ≈ 0 (CI 都跨 0)
    │   └── ✅ 完美，平行趋势通过
    │
    ├── 近期 (-1, -2) ≈ 0，远期 (-3, -4) 显著
    │   └── ⚠️ 可接受 (可能是小样本噪声)
    │       话术: "近期平行趋势成立，远期波动受样本量限制"
    │       处理: 缩短分析窗口 / 增大聚类标准误
    │
    └── 多数/所有系数显著，且呈系统性趋势
        └── ❌ 平行趋势不成立
            处理: PSM-DID / 换方法 / 加控制变量
    ```

    **关键区分**: "个别远期显著" vs "系统性趋势" → 前者可能是噪声，后者是真问题

!!! warning "Staggered DID (分批上线) 的陷阱"

    如果不同城市在**不同时间点**上线活动（例如北京 Week 3、上海 Week 7），
    传统 TWFE Event Study 可能产生**负权重偏差** (de Chaisemartin & D'Haultfœuille, 2020)。

    **解决方案**:

    - Callaway & Sant'Anna (2021) → Python: `csdid` 包
    - Gardner (2022) DID2S → Python: `pyfixest.did2s()`
    - Sun & Abraham (2021) → Python: `pyfixest` 的 `SaturatedEventStudy`

    面试时提到这些文献 = **强烈加分**。


---

### 2.6 Placebo Test (安慰剂检验) 🛡️ *稳健性必做*

!!! info "为什么需要 Placebo Test？"

    DID 模型给出一个估计值后，你怎么知道它不是"碰巧"？Placebo Test 的逻辑是：**用你的模型去估计一个"不应该存在"的效应，如果确实估不出来 → 你的模型是靠谱的。**

    类比：医生给病人吃了"安慰剂"（假药），如果病人没有好转 → 说明"吃真药好转"不是心理作用。

#### 方法 1: Placebo Time (假时间检验) ⭐ *最常用*

**逻辑**: 把干预时间**提前**到干预前某个时间点，然后用同样的 DID 模型做回归。如果你的模型是对的，那"假干预"不应该产生显著效应。

```python
import statsmodels.formula.api as smf

# 假设真实干预从 Week 5 开始
REAL_INTERVENTION_WEEK = 5

# ===== Placebo Time: 把干预时间提前到 Week 3 =====
FAKE_INTERVENTION_WEEK = 3

# 只用干预前数据 (Week 1~4)
df_pre = df[df['week'] < REAL_INTERVENTION_WEEK].copy()

# 构造假的 is_post 变量
df_pre['is_post_fake'] = (df_pre['week'] >= FAKE_INTERVENTION_WEEK).astype(int)

# 用同样的 DID 回归公式
model_placebo = smf.ols(
    'daily_orders ~ is_treated * is_post_fake',
    data=df_pre
).fit()

print(model_placebo.summary())

# 核心判断: is_treated:is_post_fake 的系数
placebo_coef = model_placebo.params['is_treated:is_post_fake']
placebo_p = model_placebo.pvalues['is_treated:is_post_fake']
print(f'\n安慰剂效应 = {placebo_coef:.2f}, P = {placebo_p:.4f}')
print(f'结论: {"✅ 通过 (P > 0.05, 无虚假效应)" if placebo_p > 0.05 else "❌ 失败 (模型可能不可靠)"}')
```

#### 方法 2: Placebo Treatment (假干预组检验)

**逻辑**: 把对照组内部**随机拆成"假处理组"和"假对照组"**，然后做 DID。如果模型靠谱，这个"假分组"不应该产生显著效应。

```python
import numpy as np

# 只取对照组数据
df_control = df[df['is_treated'] == 0].copy()

# 随机拆分: 把一半对照组城市标为"假处理组"
np.random.seed(42)
control_cities = df_control['city'].unique()
n_fake_treat = len(control_cities) // 2
fake_treat_cities = np.random.choice(control_cities, n_fake_treat, replace=False)
df_control['is_treated_fake'] = df_control['city'].isin(fake_treat_cities).astype(int)

# DID 回归
model_placebo2 = smf.ols(
    'daily_orders ~ is_treated_fake * is_post',
    data=df_control
).fit()

placebo_coef2 = model_placebo2.params['is_treated_fake:is_post']
placebo_p2 = model_placebo2.pvalues['is_treated_fake:is_post']
print(f'安慰剂效应 = {placebo_coef2:.2f}, P = {placebo_p2:.4f}')
print(f'结论: {"✅ 通过" if placebo_p2 > 0.05 else "❌ 失败"}')
```

#### Placebo 检验结果解读

| 检验方式              | 期望结果           | 如果不符合                         |
| :-------------------- | :----------------- | :--------------------------------- |
| **Placebo Time**      | 系数 ≈ 0，P > 0.05 | 说明干预前趋势已经偏了，DID 不可靠 |
| **Placebo Treatment** | 系数 ≈ 0，P > 0.05 | 说明组间差异可能非干预导致         |

!!! tip "面试速记"

    - Placebo Test 的 P 值逻辑**和正常检验相反**：**P 越大越好**
    - 你**希望** P > 0.05，因为你想证明"假的干预没有效果"
    - 如果 Placebo 也显著 → 你的 DID 结果**不可信**
    - 至少做 1 种 Placebo，面试时提到 2 种 = **加分项**

---

### 2.7 DID 业务汇报 Executive Summary 模板

!!! note "完成 DID 全流程后，用以下框架写业务结论"

    **六段式结构**：

    1. **背景**: 什么活动？对谁？从什么时候开始？
    2. **方法**: 用 DID 方法，干预组 vs 对照组
    3. **前提验证**: 平行趋势检验通过 (交互项 P > 0.05)
    4. **核心结论**: DID 估计效应 = X 单位，P < 0.05，95% CI = [a, b]
    5. **动态趋势**: Event Study 显示效应在第 k 期达到峰值/持续/消退
    6. **稳健性**: Placebo Test 通过 → 结论可靠

```python
# 模板代码: 一键输出 Executive Summary
def did_executive_summary(model_did, model_event_study, model_placebo, 
                          true_ate=None, treatment_desc="促销活动"):
    """生成 DID 分析的 Executive Summary"""
    # 提取核心结果
    did_coef = model_did.params['is_treated:is_post']
    did_p = model_did.pvalues['is_treated:is_post']
    did_ci = model_did.conf_int().loc['is_treated:is_post']
    
    placebo_p = model_placebo.pvalues.get(
        'is_treated:is_post_fake',
        model_placebo.pvalues.get('is_treated_fake:is_post', None)
    )
    
    print("=" * 60)
    print(f"📊 DID 分析 Executive Summary: {treatment_desc}")
    print("=" * 60)
    print(f"\n🎯 核心结论:")
    print(f"   DID 效应 = {did_coef:.2f}")
    print(f"   P-value  = {did_p:.4f}")
    print(f"   95% CI   = [{did_ci[0]:.2f}, {did_ci[1]:.2f}]")
    if true_ate:
        print(f"   真实 ATE  = {true_ate} (偏差: {abs(did_coef - true_ate):.2f})")
    print(f"\n🛡️ 稳健性:")
    if placebo_p is not None:
        status = "✅ 通过" if placebo_p > 0.05 else "❌ 未通过"
        print(f"   Placebo P = {placebo_p:.4f} → {status}")
    print(f"\n📝 结论可信度: {'高 ✅' if did_p < 0.05 and (placebo_p is None or placebo_p > 0.05) else '需进一步验证 ⚠️'}")
    print("=" * 60)
```

---

### 2.8 pyfixest API 速查 🚀

#### 常用方法一览

```python
import pyfixest as pf

# 建模
fit = pf.feols(
    "Y ~ i(relative_week, is_treated, ref=-1) | city",
    data=df, vcov={'CRV1': 'city'}
)

# 报告类
fit.summary()       # 回归摘要 (系数、SE、t、P、CI)
fit.coef()          # 提取所有系数 (Series)
fit.se()            # 提取标准误
fit.pvalue()        # 提取 P 值
fit.tstat()         # 提取 t 统计量
fit.confint()       # 提取 95% 置信区间 (DataFrame)

# 可视化
pf.iplot(fit, figsize=(10, 5))  # Event Study 系数图

# ⭐ 多模型对比表 (面试加分! 类似 R 的 stargazer)
fit2 = pf.feols("Y ~ is_treated * is_post", data=df)
pf.etable([fit, fit2])  # 并排对比两个模型
```

#### etable 结果解读要点

| 指标                          | 看什么                   | 面试话术                           |
| :---------------------------- | :----------------------- | :--------------------------------- |
| **`is_treated:is_post`** 系数 | ATE 大小和显著性         | "净干预效应为 X 单位，P < 0.05"    |
| **`is_treated`** 系数         | 两组基础水平差异         | 不显著 → "两组起跑线可比"          |
| **`is_post`** 系数            | 所有组的时间趋势         | "不论干预与否，自然增长 X 单位"    |
| **R²** 对比                   | 固定效应模型 >> 基础模型 | "控制城市固定效应后解释力显著提升" |
| **S.E. type**                 | by: city vs iid          | 聚类标准误更稳健                   |

---

### 2.9 动态因果效应：如何判断长尾 vs 噪声

!!! warning "不是看到递增就能说'长尾效应'！"

    判断长尾效应必须**同时满足两个条件**：

    1. **Pre-treatment 系数干净** (≈ 0) → 没有 pre-trend
    2. **Post-treatment 系数递增** → 效果在累积

    如果 pre 本身就有趋势，post 的递增可能只是既有趋势的延续。

#### 三种典型模式

```
① 真·长尾效应 (Pre 干净 + Post 递增)
     0 │──●────●────●────●──┤
    40 │                  ●────●────●
    80 │                              ●────●   ← 持续累积

② 效果衰退 (Pre 干净 + Post 递减)
     0 │──●────●────●────●──┤
    40 │                  ●
    20 │                     ●────●────●────●   ← 刺激过后回落

③ 噪声 / pre-trend 延续 (Pre 不干净 + Post 递增)
   -20 │──●
   -10 │     ●────●
     0 │              ●──┤
    40 │                  ●────●
    80 │                         ●────●────●   ← 全程单调上升，无法归因
```

!!! tip "面试话术"

    *"Event Study 显示递增模式，但需要结合 pre-treatment 系数判断：如果 pre 干净（≈0），说明是真正的累积效应；如果 pre 本身也有趋势，递增可能只是噪声或既有趋势的延续，不能归因于干预。"*

---

### 2.10 因果推断方法选型指南 🗺️

```
"我想估计因果效应，应该用什么方法？"
│
├── 有面板数据 + 明确干预时点？
│   │
│   ├── 同时干预 + 样本 >30 → 标准 DID + Event Study
│   │
│   ├── 分批干预 (Staggered) → Callaway-Sant'Anna / did2s
│   │
│   └── 处理组极少 (1-2个) → 合成控制法 (SCM)
│
├── 截面数据 + 连续型 Treatment？
│   │
│   ├── 协变量少 (<20) → PSM + 回归
│   │
│   └── 协变量多 / 非线性 → DML (Double ML)
│
└── 有 "断点" 或 "门槛"？ → RDD (断点回归)
```

#### 方法速查对比

| 方法    | 核心思路         | 适用场景                | 面试频率 |
| :------ | :--------------- | :---------------------- | :------- |
| **DID** | 时间×分组双差分  | 面板数据 + 明确干预时点 | ⭐⭐⭐⭐⭐    |
| **PSM** | 倾向得分匹配同类 | 协变量不平衡 + 样本多   | ⭐⭐⭐⭐     |
| **SCM** | 加权合成虚拟对照 | 处理组极少 (1-2 个)     | ⭐⭐       |
| **DML** | ML 控制高维混杂  | 协变量多 + 非线性关系   | ⭐⭐⭐      |
| **RDD** | 利用准入门槛     | 存在分数/等级断点       | ⭐⭐⭐      |

!!! info "PSM vs SCM 快速区分"

    |              | PSM                              | SCM                                    |
    | :----------- | :------------------------------- | :------------------------------------- |
    | **一句话**   | 给处理组个体**找一个最像的**对照 | 用多个对照组**加权拼出一个虚拟的**对照 |
    | **类比**     | 找一个和你年龄体重差不多的人比   | 用 70% 小明 + 30% 小红 合成"虚拟的你"  |
    | **依据**     | 倾向得分 P(treated \| X)         | 干预前 outcome 的时间序列              |
    | **处理组数** | 需要**很多** (>30)               | 可以只有 **1-2 个**                    |

---
