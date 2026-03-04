# A/B 测试高阶评估：CUPED 与 Delta Method

在常规的 A/B 实验中，我们最希望看到的是“只因为策略的不同”而导致的指标差异。但现实世界充满了噪音，不仅样本天然具有异质性，更有诸多复合指标让人难以简单计算统计显著性。
大厂高阶 DA 面试中，**缩减方差 (Variance Reduction)** 和 **复合指标评估** 是区分“跑数机器”和“实验架构师”的核心考点。

---

## 📉 1. 缩减方差神器：CUPED

### 1.1 背景与痛点：方差太大了！
**痛点**：有时候我们的 A/B 实验策略明明是有效的，但因为用户的**天然基础差异太大了**（比如大盘里的土豪用户和羊毛党混在一起），导致**指标的方差 (Variance) 极大**。方差一变大，统计检验的灵敏度就下降了，真正的策略提升被噪音所淹没，导致实验得出 `不显著 (p > 0.05)` 的结论。
**无效解法**：拉长实验周期、增加样本量（但流量和时间都是昂贵的！）。

### 1.2 什么是 CUPED？(Controlled-experiment Using Pre-Experiment Data)
微软提出的一种利用**实验前的数据 (Pre-Experiment Data)** 来“剔除掉用户天然固有差异”的方法。

> [!TIP]
> **大白话原理 (面试必背)**:
> 假设我们在考察用户在实验期 (Y) 的购买金额。有的用户哪怕没有这个实验策略，他平时（实验前，X）也买得很多；有的人平时就一毛不拔。这部分**平时买得很多/很少的特质，本来就和你的策略无关，是你本不该承担的误差**。
> CUPED 的核心思想就是：**“剥离出那些在实验前就能被预测出来的固有差异，只去看剩下的、真正由策略激发出的『增量』”。**

### 1.3 数学原理与 Python 实现

CUPED 的做法是构造一个调整后的新指标 $Y_{cuped}$：
$$Y^{cuped}_i = Y_i - \theta \cdot (X_i - \mu_X)$$

其中：
- $Y_i$: 用户 $i$ 实验期间的核心指标（如消费额）。
- $X_i$: 用户 $i$ 实验前一周的核心指标（称为协变量 Covariate）。
- $\mu_X$: 实验前一周全部用户的指标均值。
- $\theta$: 使得 $Y_{cuped}$ 的方差最小化的最优调节系数（实际上就是 $Y$ 和 $X$ 的协方差除以 $X$ 的方差，或者线性回归的系数）。

```python
import numpy as np
import pandas as pd
from scipy import stats

def calculate_cuped_metric(df, target_metric='Y', pre_metric='X'):
    """
    计算基于 CUPED 调整后的指标
    """
    Y = df[target_metric].values
    X = df[pre_metric].values
    
    # 1. 计算协方差与方差
    cov_matrix = np.cov(X, Y)
    cov_xy = cov_matrix[0, 1]
    var_x = cov_matrix[0, 0]
    
    # 2. 计算最优调整系数 theta
    theta = cov_xy / var_x
    
    # 3. 计算预实验指标大盘均值
    mean_X = np.mean(X)
    
    # 4. 构造 CUPED 指标
    Y_cuped = Y - theta * (X - mean_X)
    
    # 分别返回新指标、以及方差缩减比例
    var_reduction_ratio = 1 - (np.var(Y_cuped) / np.var(Y))
    
    return Y_cuped, var_reduction_ratio

# --- 模拟运行 ---
# df 含有 'user_id', 'group' (0是对照组, 1是实验组), 'Y_sales' (实验期消费), 'X_pre_sales' (实验前两周消费)
# 1. 算出调整后的指标列
# df['Y_cuped_sales'], reduction = calculate_cuped_metric(df, 'Y_sales', 'X_pre_sales')

# 2. 对这个全新的列 'Y_cuped_sales' 执行 T-Test
# control_cuped = df[df['group'] == 0]['Y_cuped_sales']
# treated_cuped = df[df['group'] == 1]['Y_cuped_sales']
# t_stat, p_value = stats.ttest_ind(treated_cuped, control_cuped)
# print(f"CUPED 调整后，方差缩减了: {reduction:.2%}")
# print(f"新的 P-value: {p_value}") # 如果原来不显著的，现在可能显著了！
```

### 1.4 CUPED vs DID：易混淆概念辨析

CUPED 和 DID 在思想上都是"利用历史数据剔除基础差异"，但**适用场景和数学本质**完全不同：

| 维度               | CUPED (A/B 测试方差缩减)               | DID (因果推断双重差分)                |
| :----------------- | :------------------------------------- | :------------------------------------ |
| **前提条件**       | ✅ 有完美的随机分流 (A/B Test)          | ❌ 无法随机分流 (观察性数据)           |
| **核心痛点**       | 方差太大 → 信号被噪音淹没              | 选择偏差 → 两组天生不一样             |
| **历史数据的角色** | 协变量 (Covariate)，用于解释个体方差   | 基线 (Baseline)，用于消除群体固有差距 |
| **减去的是什么**   | 每个用户的历史偏差 × 回归系数 $\theta$ | 两组的历史平均差距 (Group-level)      |
| **关键假设**       | 协变量不受实验影响 (Pre-experiment)    | 平行趋势假设 (Parallel Trends)        |
| **最终效果**       | 方差缩减 → 同样本量下更容易显著        | 消除选择偏差 → 估计因果效应           |

!!! tip "面试区分话术"
    "CUPED 和 DID 都利用了历史数据，但解决的是不同层面的问题。CUPED 用在**已经有随机分流**的 A/B 测试中，目的是**降噪**——把个体天然差异导致的方差减小，让实验更灵敏。而 DID 用在**无法随机分流**的场景（如不同城市上线不同策略），目的是**去偏**——通过差分消除两组天生不同的基础水平。"

!!! note "什么叫"构建新指标"？"
    CUPED 并不改变你的分析框架，而是把原始指标 $Y$ **替换**成一个经过修正的新指标 $Y_{cuped}$。

    **举个例子**：

    * 原始指标：用户 A 实验期购买了 ¥500
    * 实验前数据：用户 A 上周就购买了 ¥450（远超大盘均值 ¥200）
    * 修正后指标：$Y_{cuped} = 500 - \theta \times (450 - 200)$

    修正后的指标，**扣除了**用户 A "本来就爱买"的那部分金额。最终你对 $Y_{cuped}$ 做 T-test，而不是对原始的 $Y$ 做。这个新指标的方差更小，P-value 更容易显著。

    本质上，CUPED 就是对每个用户做了一次"起跑线校准"。

### 1.5 💡 高频面试真题：没有历史数据的用户怎么处理？

> **面试官**：如果在做 CUPED 时，发现有一批用户在实验前一周根本没有登录，或者干脆是新注册用户，导致历史协变量 $X$ 为空（Missing Data）。我们能把这部分用户剔除掉再算吗？如果不能，应该怎么处理？

**❌ 绝对不能剔除（破坏随机性与 ITT 原则）**
剔除无数据用户会引入严重的**选择偏差 (Selection Bias)**，留下的样本变成了"高活跃老用户"，实验结果无法推广到大盘。

**✅ 工业界标准处理方案（分两种情况）**：

1. **老用户但不活跃（休眠用户）**：
    - **做法**: 直接用 $0$ 填补缺失值。
    - **数学本质**: 代入公式 $Y_i - \theta \cdot (0 - \mu_X) = Y_i + \theta\mu_X$。公式自动在他们原本的 $Y_i$ 上**补偿**了一个正值（因为他们基础差），把他们拉长到了大盘起跑线。
2. **纯新用户（实验期刚注册）**：
    - **做法 A（均值填充法）**: 用老用户的历史大盘均值 $\mu_X$ 填补。代入公式 $Y_i - \theta \cdot (\mu_X - \mu_X) = Y_i$。结果是**新用户的指标完全不作调整**，只对老用户做调整。
    - **做法 B（分层方差法 Post-stratification）**: 更严谨的大厂做法。把大盘分为"有历史的老用户分层"和"无历史的新用户分层"。老用户层走 CUPED 算均值方差，新用户层走普通 T-Test 算均值方差。最后通过分层抽样公式将方差加权合并起来，既解决了缺失数据，又进一步缩减了总体方差。

---

## 🧮 2. 复合指标的 Delta Method

### 2.1 痛点：除数和被除数都在波动！
在 A/B 实验中，最喜欢用的是**比率指标 (Ratio Metrics)**，比如：
* **点击率 (CTR)** = 点击量 (Clicks) / 曝光量 (Views)
* **人均收入 (ARPU)** = 总收入 (Revenue) / 活跃用户数 (DAU)

这个时候，普通的 T-Test (两独立样本 T 检验) 就**不能直接用**了！
**为什么？** 因为你在算 T-Test 时，默认分母是常量，每个人的观测值是相互独立的。但是对于 CTR，一个人可能点 3 次曝光 5 次，另一个人点 1 次曝光 10 次。分子分母在这个聚合层面上都在发生波动！普通的方差公式失效。

### 2.2 什么是 Delta Method？
简而言之，就是利用泰勒展开 (Taylor Expansion)，把一个非线性的函数（比如 $f(x, y) = x/y$）做一阶线性近似，从而推导出这个比率的方差。

> [!IMPORTANT]
> **面试黄金回答范例（比率指标如何做 T-Test？）**:
> “平时做单纯的点击次数对比时，算样本均值和方差就可以了。但如果是 CTR 这种 Ratio 指标，分子（点击数 $X$）和 分母（曝光数 $Y$）**是两个随机变量构成的复合函数**。我会使用 **Delta Method** 来预估比率的整体方差。”
>
> 核心公式：
> $Var(\frac{\overline{X}}{\overline{Y}}) \approx \frac{1}{\overline{Y}^2} Var(X) - \frac{2\overline{X}}{\overline{Y}^3} Cov(X, Y) + \frac{\overline{X}^2}{\overline{Y}^4} Var(Y)$

### 2.3 Delta Method Python 实现

由于纯数学公式计算比较容易出错，业界常常用**基于用户的层面**把 Ratio Metric 降维成普通的均值。具体实施代码如下：

```python
import numpy as np
import scipy.stats as stats

def delta_method_ttest(df, numerator='clicks', denominator='views', group='variant'):
    """
    计算处理组和对照组两组基于 Delta Method 的 T 检验
    :param df: 用户级数据表，一行代表一个用户的总点击(numerator)和总曝光(denominator)
    """
    # 拆分两组
    control = df[df[group] == 0]
    treated = df[df[group] == 1]
    
    def calculate_ratio_and_var(data_group):
        X = data_group[numerator].values
        Y = data_group[denominator].values
        
        n = len(data_group)
        mean_x = np.mean(X)
        mean_y = np.mean(Y)
        ratio = mean_x / mean_y
        
        var_x = np.var(X, ddof=1)
        var_y = np.var(Y, ddof=1)
        cov_xy = np.cov(X, Y)[0, 1]
        
        # Delta method 核心方差公式
        var_ratio = (var_x / (mean_y ** 2)) - \
                    (2 * mean_x * cov_xy / (mean_y ** 3)) + \
                    ((mean_x ** 2) * var_y / (mean_y ** 4))
        
        # 返回均值和它的标准误平方 (Standard Error Squared)
        return ratio, var_ratio / n

    # 1. 计算各自的均值和方差
    r_ctrl, var_ctrl = calculate_ratio_and_var(control)
    r_trt, var_trt = calculate_ratio_and_var(treated)
    
    # 2. 两组的比率差
    diff = r_trt - r_ctrl
    
    # 3. T 统计量与 P 值
    t_stat = diff / np.sqrt(var_ctrl + var_trt)
    
    # 自由度使用样本量之和减 2
    df_dof = len(control) + len(treated) - 2
    p_value = 2 * (1 - stats.t.cdf(abs(t_stat), df_dof))
    
    return diff, t_stat, p_value

# 使用此函数不仅保证了非独立事件的准确评估，更是你区别于普通取 p-value 的巨大亮点！
```

---

## ⚡ 3. 贯序检验与 mSPRT：不偷看会死的时代

### 3.1 痛点：业务方要提前看数据！

在真实的业务环境中，"跑满 7 天再看"几乎是奢望。老板、PM、运营每天都会问："实验有结论了没？"

如果你每天偷看一次 P 值，然后一看到 P < 0.05 就欢天喜地宣布"显著了！上线！"，你的假阳性率会从 5% 飙升到近 **30%**（$1 - 0.95^7 \approx 0.30$）。

!!! danger "偷看 (Peeking) 问题的本质"
    每次偷看 = 做了一次额外的假设检验。硬编码 α = 0.05 意味着"只要有一次中奖就宣布胜利"，但你买了 7 张彩票（偷看 7 次），中奖概率当然暴增。

### 3.2 解法：mSPRT (混合贯序概率比检验)

核心思想：传统 T-Test 只能在事先规定好样本量跑满后看一次。而 **mSPRT (Mixture Sequential Probability Ratio Test)** 允许你在实验期间随时、无限次地看数据。

它的底层逻辑是计算**似然比 (Likelihood Ratio)** $\Lambda_n$：

$$ \Lambda_n = \frac{\text{数据在有策略效应下的似然概率}}{\text{数据没效果下的似然概率}} $$

只要 $\Lambda_n > 1/\alpha$ （比如业务要求的 $\alpha=0.05$，阈值就是 20），我们就可以安全地提前拒绝原假设，宣布显著。

因为它是基于似然比的鞅 (Martingale) 性质建立的理论，从数学底层保证了：**不管你每天甚至每小时偷看多少次，在整个实验周期内发生第一类错误（假阳性）的总概率，都永远被死死压制在 $\alpha$ 以下。**

### 3.3 实战：反向推导的动态显著性门槛 (喇叭口)

虽然 mSPRT 内部算的是似然比，但为了让业务端和传统看板更容易理解，我们通常通过数学变换，将其**反向映射为每天所需的等效 P 值门槛**。

由于每天累积的样本量 $n$ 不同：
- **前期（Day 1-2）**：样本极少，想让似然比冲上 20 难度极大，所以反算出来的 P 值门槛极其变态（比如 $P < 0.0001$ 才算显著）。
- **后期（Day 6-7）**：样本充足，似然比达到 20 相对容易，P 值门槛逐渐放宽到接近 $0.05$。

这在直观上就形成了一把逐渐张开的"喇叭口"。

**mSPRT 的 Python 核心计算推导（面试防身代码）**：

在 mSPRT 中，如果是针对大样本均值校验，底层似然比 $\Lambda_n$ 的分布可由正态分布的共轭先验推导出以下闭式解（其中 $\tau^2$ 为混合先验方差）：

$$ \Lambda_n = \sqrt{\frac{1}{1 + n\tau^2}} \exp \left( \frac{n\tau^2 Z_n^2}{2(1 + n\tau^2)} \right) $$

由于我们要硬卡死似然比 $\Lambda_n = 1/\alpha$，通过上述公式反解 $Z_n$，最后转化成便于业务理解的"等效 P 值门槛"：

```python
import numpy as np
import scipy.stats as stats

def calc_max_sample_size(base_rate, mde_relative, alpha=0.05, power=0.80, variant_ratio=0.5):
    """
    第一步：实验开启前，基于常规 T-test 的原理计算"固定周期"下的最大样本总量
    这是为了给 mSPRT 提供混合分布方差 tau_sq 的锚点，并作为兜底期限
    """
    z_alpha = stats.norm.ppf(1 - alpha/2)
    z_power = stats.norm.ppf(power)
    
    # 绝对 MDE
    mde_abs = base_rate * mde_relative
    # 假设两组方差相近 (p*(1-p))
    variance = base_rate * (1 - base_rate)
    
    # 标准样本量公式
    n_per_group = (z_alpha + z_power)**2 * (2 * variance) / (mde_abs**2)
    total_n_max = n_per_group / variant_ratio
    return total_n_max

def calc_msprt_tau_sq(mde_relative, base_rate, total_n_max):
    """
    第二步：实验开启前，根据 MDE 和 最大样本量 锁定先验分布参数 tau_sq
    工业界经验公式：tau = MDE_abs / sqrt(var * 2 / total_n) (近似推导)
    简单起见，这里采用常用的渐近近似设定：tau_sq ≈ (MDE_abs^2) / 分布方差
    """
    mde_abs = base_rate * mde_relative
    variance = base_rate * (1 - base_rate)
    # 这是一个简化的方差参数锚定
    tau_sq = (mde_abs ** 2) / (2 * variance) 
    return tau_sq

def msprt_open_ended_threshold(current_accumulated_n, tau_sq, alpha=0.05):
    """
    第三步：实验进行中！这是一个【完全无天数限制】的开放式计算函数。
    只要你传入此时此刻大盘累积的样本量 n，它就吐出此时应该严守的 Z 和 P 门槛。
    """
    likelihood_threshold = 1 / alpha
    n = current_accumulated_n
    
    # 核心公式反推：令 Likelihood Ratio = 1/alpha，求解对应此时大盘的 Z 统计量
    # Lambda = sqrt(1/(1+n*tau_sq)) * exp( (n*tau_sq * Z^2) / (2*(1+n*tau_sq)) ) = 1/alpha
    term1 = 2 * (1 + n * tau_sq) / (n * tau_sq)
    term2 = -np.log(alpha) + 0.5 * np.log(1 + n * tau_sq)
    
    z_critical = np.sqrt(term1 * term2)
    equivalent_p_value = 2 * (1 - stats.norm.cdf(z_critical))
    
    return z_critical, equivalent_p_value

# ================= 模拟工业界闭环 =================

# 1. 实验前规划
BASE_RATE = 0.20   # 基线转人工率 20%
MDE_REL = 0.05     # 业务要求至少干预掉 5% 的转人工率 (MDE_abs = 0.01)

n_max = calc_max_sample_size(BASE_RATE, MDE_REL)
tau_squared = calc_msprt_tau_sq(MDE_REL, BASE_RATE, n_max)

print(f"【阶段1】实验立项前计算：")
print(f"为检测 5% 提升，传统需要总样本 {n_max:,.0f} 人作为兜底周期 (假定每天进线1万，兜底期为 {n_max/10000:.0f} 天)")
print(f"根据此 MDE 预设锁定系统级别的 tau_sq = {tau_squared:.6f}\n")

print(f"【阶段2】看板动态每天监控门槛 (Open-ended)：")
# 业务说：遇到周末流量低迷，我跑到第 8 天行不行？
# 行！只要输入当时的累积样本，随时吐出门槛
for day in range(1, 9): 
    accumulated_n = day * 10000 # 假设日均1w进线
    z_th, p_th = msprt_open_ended_threshold(accumulated_n, tau_squared)
    print(f"Day {day} (累积 {accumulated_n} 人) | 要求 Z > {z_th:.3f} | 或等效 P值 < {p_th:.6f}")
```

输出的“等效 P 值门槛”就是下表中我们展示给业务方的“喇叭口”：

| 监控阶段 | 似然比阈值 | 等效 P 值门槛 (示意) | 实际含义               |
| :------: | :--------: | :------------------: | :--------------------- |
|  Day 1   |    > 20    |      < 0.00001       | 几乎不可能通过，别看了 |
|  Day 3   |    > 20    |       < 0.002        | 非常严格               |
|  Day 5   |    > 20    |       < 0.020        | 开始有可能通过         |
|  Day 7   |    > 20    |      < 0.05000       | 终于接近（但小于）0.05 |

### 3.4 💡 深水区考点：mSPRT 需要算最小样本量吗？第7天会冲突吗？

> **面试官连环追问**：
> 1. 既然 mSPRT 可以随时看、随时停，那开展实验前还需要根据 MDE 推算最小样本量和实验天数吗？
> 2. 如果前 6 天被 mSPRT 的严苛门槛压着一直不显著，但到了第 7 天，跑传统的 T-Test 显著了，但跑 mSPRT 依然不显著，会有这种可能吗？听谁的？

**核心痛点与防守话术：**

**问题1：mSPRT 要不要提前算样本量和天数？**
**答**：“需要，但目的不一样。
传统 T-Test 算样本量是为了『合规』——没跑满这么多样本，你看的 P 值就是错的。
而 mSPRT 算样本量是为了**『兜底预算』和『设定先验参数』**。
1. **兜底预算**：mSPRT 是为了支持提前**赢或输（早停）**，如果一直没达到阈值，总不能让实验无限期挂在上面空耗流量吧？所以我们依然会根据常规的 MDE 算出一个『最大实验周期』（比如 7 天或 14 天）。到了最后一天还没撞线，就强制平局拉倒。
2. **设定先验参数 $\tau^2$**：我们在代码里构造 mSPRT 似然比时，需要预设一个『混合先验分布方差 $\tau^2$』。在工业界，最科学的做法就是令 $\tau \approx \text{MDE} / \sqrt{n_{max}}$。你只有先算了固定周期的最小样本量，才能给 mSPRT 定好这个锚点，让它的检验功效（Power）最大化。”

**问题2：第 7 天传统显著，但 mSPRT 不显著，可能吗？听谁的？**
**答**：“**完全可能，并且必须听 mSPRT 的！**
这就是贯序检验**必须付出的代价（Power Penalty）**。
因为 mSPRT 允许你在 Day 1 到 Day 6 疯狂偷看（享受特权），为了维持整个 7 天生命周期内总假阳性率 $<5\%$，它必须把每一天的门槛都提高。哪怕到了最后一天（Day 7），mSPRT 的阈值依然会比无脑 T-test 的 $0.05$ 要稍微苛刻一点点（比如 $0.04$ 等等）。
如果恰好第 7 天的数据落在 $0.04 \sim 0.05$ 之间：
* 传统 T-test 会亮绿灯：‘显著啦！’
* mSPRT 会亮红灯：‘不显著，你不许上！’

**听谁的？绝对听 mSPRT 的。** 只要你前面 6 天看板上亮着数据（哪怕你看一眼也是看了），你就不再享有传统 T-test 的宽松准入资格。这是为了提前止损必须交的『保护费』。”

**问题3（绝杀局）：第 7 天不显著，PM 死活不想下线，非要再跑几天，但第 8 天已经没有给定的动态门槛了，怎么办？**

> 这个问题直指你在大厂跟业务方极限拉扯的实战经验。

**答**：“绝对不能因为 PM 取闹就无脑延期，这会彻底破坏实验的科学性（本质上就是 P-hacking 捞显著）。我的处理 SOP 分三步：

1. **第一道防线（诊断 MDE）**：
   马上查当前的**效应量（Lift）**和预设的 MDE。如果当前的业务提升只有 0.5%，而预设的 MDE 是 2%，说明这个策略『微效或无效』，这不叫没测出来，而是**真理已经浮出水面**了。我会用数据告诉 PM：『这策略天生底子太弱，就算你再跑一个月凑够样本把它强行跑出统计显著，它也是个没有业务价值（ROI 极低）的垃圾策略，趁早放弃投入新点子。』
   
2. **第二道防线（诊断底噪）**：
   如果 Lift 已经达到了 MDE（比如 2.5%），但依然不显著，说明是**方差太大（底噪太高）导致置信区间过宽**。我会立刻加一道 **CUPED 方差缩减**，把历史两周的数据拿来作为协变量进行降噪。很多时候 CUPED 压制了 30% 的方差后，P 值当场就会击穿门槛变显著，立刻解决问题。

3. **最终妥协（mSPRT 的永远开放特性）**：
   如果在以上两步依然无果，且 PM 坚信只是因为大盘这两天流量低迷导致样本不足（比如撞上周末），确实可以延期。
   并且，**mSPRT 的伟大之处就在于它是 Open-ended（开放截尾）的**！不同于传统 alpha spending 必须预设固定天数，mSPRT 的底层 $\Lambda_n = 1/\alpha$ 阈值是与天数无关的绝对算子。由于 $\tau^2$ 在实验前已经确立（$\tau \approx \text{MDE}/\sqrt{n_{max}}$），你只需要把第 8 天、第 9 天的累积样本量 $n$ 代入上面的 Python 算式，系统会**自动吐出第 8 天、第 9 天对应的等效 P 值门槛**。
   所以，我不仅可以让他接着跑，还能顺带告诉他第 8 天的通关难度。”

!!! tip "实战应用总结"
    所以大厂真实的做法是：**双轨并行**。
    看板上透出的所谓“显著/不显著”永远用 mSPRT 算出来的动态门槛卡着；只有当实验强行跑满预设周期（比如 14 天），且你保证中间**没有任何基于看板的早停决策**时，我们在期末做全量 Review 时，才会用传统 T-Test 复盘。

### 3.5 💡 高频面试追问：为什么不直接用 Bonferroni 修正？

> **面试官**: 你说每天偷看一次总共看 7 次，那我直接用 Bonferroni 修正 $\alpha' = 0.05/7 \approx 0.007$ 不就行了？干嘛还要搞那么复杂的似然比？

**答**: Bonferroni 假设每次检验都是**完全独立**的。但 A/B 实验大盘看板每天的数据是**层层累加**的——Day 3 的数据包含了 Day 1 和 Day 2 的全部数据。这些重复检验高度相关。

在这种高度相关的数据流上使用 Bonferroni 会导致门槛**过度保守 (Overly Conservative)**，导致实验的统计功效 (Power) 严重下降，原本有效的策略也被冤枉成无效。mSPRT 的似然比就是专门为了处理这种"累积数据流"的连续监测而设计的，能**在控制假阳性的前提下最大化保留统计功效**。

---

## 📦 4. 极度长尾分布的检验 (Heavy-Tailed Data)

在电商（打赏、GMV、内购）等真实业务场景中，很多指标（尤其是钱）都不符合正态分布，而是呈现出**极度偏态的"二八定律"长尾分布**。绝大多数用户可能消费为 $0$，极少数"鲸鱼用户"贡献了极高的金额。

对于这类数据，直接套用 T 检验会因为**方差被极值无限放大**而导致检验效能极低甚至失效（不显著）。

### 4.1 四大流派应对方案

大厂面试中，处理长尾 GMV 数据的标准组合拳有以下四种：

| 流派                               | 做法                                                                | 适用范围                            | 致命缺陷                                                           |
| :--------------------------------- | :------------------------------------------------------------------ | :---------------------------------- | :----------------------------------------------------------------- |
| **1. 对数变换**                    | $log(X+1)$ 后做 T-Test                                              | 正数部分服从对数正态                | **业务不可解释**：无法向老板解释"对数均值涨了代表到底多赚了多少钱" |
| **2. 截断过滤 / 缩尾**             | 直接删去/封顶前 1%的极端土豪                                        | 明确确认大单是偶然噪音              | **"削足适履"**：如果策略本来就是拉动高净值客户，删掉就等于掩耳盗铃 |
| **3. 非参数检验**                  | Mann-Whitney U test                                                 | 任何畸形分布                        | **无绝对量化**：只能得出排名中位数大小提升，算不出平均多赚的金额   |
| **4. 两部模型 / 栅栏模型** (推荐!) | Hurdle / Two-Part Model：**广度 (是否消费) + 深度 (客单价)** 拆开看 | 含有海量 0 的消费、打赏等转化类漏斗 | 需要向业务解释"结构性变化"                                         |

### 4.2 🌟 工业界最强杀器：两部模型 (Two-Part Model) 代码实战

这是解决 "一堆 0 + 极度长尾少部分大额" 数据的最佳答案，原因在于：**它把一个混沌的业务问题，精准解构成了两个可行动的业务结论。**

1. **广度探索 (Part 1)**：把所有非零金额转化为 1，看策略是否带来了更多的**付费人数渗透率**（Z 检验）。
2. **深度挖掘 (Part 2)**：剔除掉所有 0 元未付费样本，仅对付费用户进行客单价检验（T 检验），看是否**激发了单客消费潜力**。

??? example "🐍 Two-Part Model (Hurdle) 核心检验代码"

    ```python
    import numpy as np
    from scipy import stats
    from statsmodels.stats.proportion import proportions_ztest

    # 假设你的原始数据是 tip_exp 和 tip_ctrl
    # 真实工业数据中，大部分人应该是0。如果全是连续生成的数值，必须手动把没产生行为的人填为 0
    # ==========================================

    # 💡 Part 1: 广度检验 —— 转化率 (是否产生打赏/消费)
    # 将所有大于0的值变为1，等于0的值保持为0
    is_tipped_exp = (tip_exp > 0).astype(int)
    is_tipped_ctrl = (tip_ctrl > 0).astype(int)

    # 统计转化人数和总进线人数
    count_tipped = [is_tipped_exp.sum(), is_tipped_ctrl.sum()]
    nobs = [len(is_tipped_exp), len(is_tipped_ctrl)]

    # 核心判断：因为样本>1000，使用 proportions_ztest 检验转化率差异
    stat_cv, p_val_cv = proportions_ztest(count_tipped, nobs)
    print(f"✅ Part 1 - 转化率检验 (是否有更多人掏钱):")
    print(f"   实验组转化率: {is_tipped_exp.mean():.2%}, 对照组: {is_tipped_ctrl.mean():.2%}")
    print(f"   Z检验 p_value: {p_val_cv:.4f} ({'显著' if p_val_cv < 0.05 else '不显著'})")
    print("-" * 40)

    # 💡 Part 2: 深度检验 —— 客单价 (仅针对产生过消费的用户!)
    # 这一步过滤掉所有 0 元的"白嫖"用户，只提取真实产生利润的买单用户
    amount_exp_nonzero = tip_exp[tip_exp > 0]
    amount_ctrl_nonzero = tip_ctrl[tip_ctrl > 0]

    # 核心判断：剔除 0 之后，使用普通的 Welch's T-test (不假设方差齐性)
    stat_amt, p_val_amt = stats.ttest_ind(amount_exp_nonzero, amount_ctrl_nonzero, equal_var=False)

    print(f"✅ Part 2 - 客单价检验 (只看消费过的用户):")
    print(f"   实验组均价: ￥{amount_exp_nonzero.mean():.2f}, 对照组均价: ￥{amount_ctrl_nonzero.mean():.2f}")
    print(f"   T检验 p_value: {p_val_amt:.4f} ({'显著' if p_val_amt < 0.05 else '不显著'})")
    print("=" * 40)

    # 💡 终极业务归因指导 (向老板汇报用)：
    # 1. 广度显著，深度不显著: "策略成功破圈，吸引了更多新客尝试购买，但老客/大盘的平均核心消费力没变。"
    # 2. 广度不显著，深度显著: "策略没能有效拉新，但成功刺激了那批核心高净值客户的消费潜能（薅老客羊毛）。"
    # 3. 广度深度双显著: "全垒打！策略既提升了付费破冰率，又带动了客单价的大盘拉升。"
    ```

---

## 🚦 5. 全量上线决策清单 (Go-Live Checklist)

> **认知升级 (2026.02.26, Ron Kohavi 视频)**:
> 短期统计显著 ≠ 可以直接全量上线。Senior DA 需要在 Go/No Go 决策后，进一步评估**长期效应的可持续性**。

### 5.1 全量上线五步检查表

|   #   | 检查维度                | 具体动作                                  | 通过标准               |
| :---: | :---------------------- | :---------------------------------------- | :--------------------- |
|   ✅   | **统计显著性**          | P-value < 0.05 + 效应量达到 MDE           | 主指标正向显著         |
|   ✅   | **护栏指标**            | 核心 KPI 无负面影响                       | 无负向显著变化         |
|   ✅   | **SRM 检查**            | 样本比率无偏差 (卡方检验)                 | p > 0.001              |
|   ⚠️   | **Novelty Effect 衰减** | **DTD 趋势监控** (见 5.2)                 | DTD 后期无持续下降趋势 |
|   ⚠️   | **长期代理指标**        | 是否存在 Leading Indicator 预示长期风险？ | 无滞后负面信号         |

### 5.2 💡 DTD 监控的第二重身份：Novelty Effect 检测器

!!! important "认知突破"
    **之前的理解**: DTD (Day-to-day) 监控只是为了在实验初期校验分流是否正确（SRM 诊断）。

    **升级后的理解**: DTD 同时是 **Novelty Effect（新奇效应）衰减**的最佳监控工具！

**什么是 Novelty Effect？**
用户对**任何变化**都会短期表现出好奇（如点击率上升），但一旦习惯后就会回落到基线水平。如果不检测，你会把一个"只有短期效果"的策略当成"永久有效"而全量上线。

**如何用 DTD 检测？**
```
DTD (实验效果的日增量) 观察规律：

Day 1-3:  ████████████  +8%   ← 新奇效应最强
Day 4-5:  ████████      +5%   ← 开始衰减
Day 6-7:  ████          +2%   ← 如果持续下降 → ⚠️ Novelty Effect！
Day 7+:   ██            +1%   ← 如果趋近于 0 → 实际效果可能不存在

vs 真实有效的策略：

Day 1-3:  ████████      +5%   ← 初期偏高（轻微新奇效应）
Day 4-5:  ██████        +4%   ← 小幅回落
Day 6-7:  ██████        +4%   ← 稳定 → ✅ 真实效果！
```

!!! tip "面试黄金话术"
    "DTD 监控不仅用于分流诊断，我还用它来检测 Novelty Effect。如果 DTD 的增量效应在实验后期呈持续下降趋势且趋近于 0，说明短期正向结果可能是用户对变化的新奇反应，而非策略本身的价值。此时我会建议延长实验周期至少 2 个完整业务周期，或者拆分新老用户分别评估，再做全量决策。"

### 5.3 长期指标盲区 (Lagging Metrics)

即使护栏指标在实验期间表现正常，某些**滞后影响**可能要数周甚至数月后才会显现。

| 场景               | 短期表现        | 长期隐患                              |
| :----------------- | :-------------- | :------------------------------------ |
| FAQ 改版减少转人工 | ✅ 转人工率 -9pp | ⚠️ 用户问题未真正解决 → 复购率可能下降 |
| 推荐算法优化 CTR   | ✅ CTR +3%       | ⚠️ 同质化推荐 → 用户长期兴趣衰减       |
| 激进弹窗提升注册   | ✅ 注册率 +15%   | ⚠️ 用户体验恶化 → 7 日留存下降         |

**应对策略**：全量上线后设置 **Post-launch 监控窗口**（通常 2-4 周），持续跟踪滞后指标（留存率、复购率、NPS 等）。如果出现负向趋势，立即回滚。

---

## 🎬 6. 推荐学习资源 (YouTube)

### CUPED 方差缩减

| 视频                                                                                                                            | 说明                                                                      |
| :------------------------------------------------------------------------------------------------------------------------------ | :------------------------------------------------------------------------ |
| [CUPED for Variance Reduction in A/B Testing (Experimentation & Causal Inference)](https://www.youtube.com/watch?v=FT0fwIx4w4I) | 从直觉到公式推导，讲解 CUPED 如何利用协变量降低实验方差                   |
| [Variance Reduction in Experiments — CUPED & Beyond](https://www.youtube.com/watch?v=vy3vUfPMX_U)                               | 讲解 CUPED 以及更多方差缩减技术（Stratification, Post-Stratification 等） |

### Delta Method

| 视频                                                                                                 | 说明                                                               |
| :--------------------------------------------------------------------------------------------------- | :----------------------------------------------------------------- |
| [The Delta Method (Mathematical Statistics)](https://www.youtube.com/watch?v=9QbqbTMEkbw)            | 数学统计角度详解 Delta Method 的泰勒展开推导过程                   |
| [Real World Data Science: The Delta Method in Practice](https://www.youtube.com/watch?v=XdJQgeYfz6o) | 实践导向，展示如何在实际营销实验中使用 Delta Method 计算 ROAS 方差 |

### Sequential Testing / Alpha Spending

| 视频                                                                                                    | 说明                                                                        |
| :------------------------------------------------------------------------------------------------------ | :-------------------------------------------------------------------------- |
| [Sequential Testing in A/B Experiments (Uber Engineering)](https://www.youtube.com/watch?v=nMCnmr0AErg) | Uber 工程团队讲解 mSPRT 贯序检验在其实验平台中的实战应用                    |
| [Group Sequential Tests: Alpha Spending (PASS Software)](https://www.youtube.com/watch?v=s6gMW8VEy5I)   | 详细讲解 O'Brien-Fleming 和 Pocock Alpha Spending Function 的数学推导与用法 |

!!! tip "学习顺序建议"
    1. 先看 CUPED 视频理解"方差缩减"的直觉
    2. 再看 Delta Method 视频理解"比率指标方差估计"的数学原理
    3. 最后回到 Notebook 动手实操，对比 CUPED 前后的 P-value 变化
