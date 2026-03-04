# 🛡️ 稳健性检验 (Robustness Checks)

在无法进行理想 A/B 实验的观测性研究中，我们常常使用 DID (双重差分) 或 PSM (倾向性得分匹配)。但这些方法都有局限性（例如 DID 依赖于严格的平行趋势假设，PSM 无法控制**不可观测变量**）。
为了证明因果效应的稳健性 (Robustness)，大厂面试和顶级论文中必考两大护法：**合成控制法 (Synthetic Control, SC)** 与 **安慰剂检验 (Placebo Test)**。

## 0. 稳健性检验 SOP 速查 (30 秒)

| 检验方法          | 目的                     | 操作               | 预期结果                |
| :---------------- | :----------------------- | :----------------- | :---------------------- |
| **安慰剂 (时间)** | 排除时间趋势干扰         | 假设干预提前发生   | 效应不显著 (P > 0.05)   |
| **安慰剂 (空间)** | 排除非干预因素           | 假设干预在非干预组 | 效应不显著              |
| **随机共因**      | 检验对未观测混淆的敏感度 | 加入随机噪声变量   | ATE 不变                |
| **数据子集**      | 检验结论稳定性           | 随机删 20% 数据    | 效应变化不大            |
| **合成控制**      | 构造虚拟对照组           | 加权多个对照单位   | 干预前贴合 + 干预后偏离 |

!!! tip "Refutation 的 P 值怎么看？(反直觉！)"
    在稳健性检验中，**P 值越高越好**，逻辑是反的——你**希望** P > 0.05（即"没事"），因为你想证明的是"虚假干预没有效果"。

### DoWhy 稳健性检验代码速查

```python
# 1. 随机共因 (敏感性)
model.refute_estimate(estimand, estimate, method_name="random_common_cause")

# 2. 安慰剂干预 (假干预)
model.refute_estimate(estimand, estimate, method_name="placebo_treatment_refuter", placebo_type="permute")

# 3. 数据子集 (稳定性)
model.refute_estimate(estimand, estimate, method_name="data_subset_refuter", subset_fraction=0.8)
```

---

## 🏗️ 1. 合成控制法 (Synthetic Control Method)

### 1.1 什么是合成控制？解决什么问题？
**痛点**: 当我们只有一个“干预组”（例如某一个城市开启了打车补贴），且在剩余的城市中**找不到任何一个城市**能在干预前与干预城市的趋势完美平行（即**平行趋势假设破裂**）。
**解法**: 既然找不到一个完美的对照城市，那我们就把所有未受干预的城市按**不同权重**“拼凑”出一个虚拟的“合成城市”。让这个合成城市在干预前的趋势与真实干预城市尽可能一致。

> [!TIP]
> **数学原理核心**: 
> 寻找一个权重向量 $W = (w_1, w_2, ..., w_J)$，使得合成对照组在干预前的特征 $X_0 \times W$ 尽可能接近干预组的特征 $X_1$。
> 约束条件：权重大于等于 0，且权重之和为 1 ($\sum w_i = 1$)。这本质上是一个**受约束的最优化问题（二次规划）**。

### 1.2 Python 代码框架 (借助 `scipy.optimize`)

在 Python 中，通常我们通过 `scipy.optimize.minimize` 手动实现，或者使用第三方的 `pysynth`。这里演示最核心的手写逻辑（体现 Senior DA 的底层推演能力）。

```python
import numpy as np
import pandas as pd
from scipy.optimize import minimize
import matplotlib.pyplot as plt

def synthetic_control_optimize(X_treated, X_controls):
    """
    计算合成控制的权重
    :param X_treated: 干预组干预前的数据特征序列 (1D Array)
    :param X_controls: 对照组(Donor Pool)干预前的数据特征矩阵 (2D Array, 列为各个对照单位)
    """
    n_controls = X_controls.shape[1]
    
    # 定义目标函数：最小化合成组与干预组的均方误差 (MSE)
    def objective_fn(W):
        synthetic_X = X_controls.dot(W)
        return np.mean((X_treated - synthetic_X)**2)
    
    # 约束条件：权重和为 1
    cons = ({'type': 'eq', 'fun': lambda W: np.sum(W) - 1})
    # 边界条件：权重在 0 到 1 之间（禁止做空/外推）
    bounds = [(0, 1) for _ in range(n_controls)]
    # 初始猜测：均分权重
    initial_W = np.ones(n_controls) / n_controls
    
    # 求解最优权重
    res = minimize(objective_fn, initial_W, bounds=bounds, constraints=cons, method='SLSQP')
    
    return res.x # 返回最优权重向量

# --- 模拟使用场景 ---
# 假设前 20 天为干预前时期
treated_pre = df[df['city']=='A']['sales'][:20].values
controls_pre = df[df['city']!='A'].pivot(columns='city', values='sales')[:20].values

# 1. 拟合权重
optimal_weights = synthetic_control_optimize(treated_pre, controls_pre)
print("最优对照权重:", optimal_weights)

# 2. 构造整个时间段的合成控制组
controls_all = df[df['city']!='A'].pivot(columns='city', values='sales').values
synthetic_city_A = controls_all.dot(optimal_weights)

# 3. 绘制对比图评估效应
plt.plot(df[df['city']=='A']['sales'].values, label='真实城市 A')
plt.plot(synthetic_city_A, label='合成城市 A (Synthetic)', linestyle='--')
plt.axvline(x=20, color='red', label='干预时间点')
plt.legend()
plt.title("合成控制法评估干预效应")
plt.show()
```

---

## 🧪 2. 安慰剂检验 (Placebo Test)

### 2.1 什么是安慰剂检验？解决什么问题？
**痛点**: 你用 DID 或 PSM 算出了一个显著的提升（比如策略带来 +5% 销量）。业务方问：“这个 +5% 是不是因为那段时间整体大盘自然波动导致的？或者是因为其他未知因素的巧合？”
**解法**: **“证伪”逻辑**。如果你声称效应是“特有的干预”带来的，那我把它**嫁接到一个根本没有受干预的时空上**，如果还能算出显著效应，就说明你的模型是错的（有其他混杂因素在起作用或模型本身结构不稳定）。只有当“虚假干预”算不出效应时，我们才敢相信你的结论。

> [!IMPORTANT]
> **面试黄金句型**: “为了回答业务方对于『混杂因素导致巧合』的质疑，我在汇报前一定会跑一遍安慰剂检验。如果虚假检验同样算出了显著正收益，说明这是由不可观测的全局趋势带来的噪声，我就会拒绝这个策略有效。”

### 2.2 两大核心 SOP 流程

#### 👉 方案 A：在“时间”上做手脚 (Time Placebo)
**核心思想**: 假设干预时间**提前**发生。
1. 真实干预时间是 Day 30。
2. 我们假设干预时间在 Day 15（此时其实并没有任何策略）。
3. 使用同一套模型（DID/SC）去比较 Day 1 ~ 15（干预前）和 Day 16 ~ 30（**虚假干预后**）的差异。
4. **预期结果**: 回归算出来的交互项系数 (Treatment Effect) 应该**不显著** ($p > 0.05$)。如果显著，说明你的平行趋势早就破裂了。

#### 👉 方案 B：在“空间/人群”上做手脚 (In-Space Placebo / Permutation Test)
**核心思想**: 假设干预发生在了**并未受干预的群体**上。这在合成控制法中尤为重要。
1. 真实的干预施加在了城市 A。
2. 我们从剩余未受干预的对照城市 (B, C, D...) 中，**随机抽取一个城市（比如 B）作为“虚假干预城市”**，把真实的城市 A 作为一个普通的对照城市放回大盘。
3. 运行模型，计算出城市 B 的“虚拟干预效应”。
4. 对所有对照城市（C, D, E...）重复步骤 2-3，得到一个**虚假效应分布**。
5. **预期结果**: 你最初为真实的城市 A 计算出的干预效应，应该远大于这堆“虚假效应”（统计学上，真实效应应落在随机虚假效应分布的 95% 置信区间之外），从而证明城市 A 的爆发极小众、极不偶然。

### 2.3 Placebo Test (人群置换) 代码实战

```python
import statsmodels.formula.api as smf
import numpy as np

# 假设 df 为面板数据: columns = ['user_id', 'post_period', 'treatment', 'sales']
# real_did_model = smf.ols("sales ~ treatment * post_period", data=df).fit()
# real_effect = real_did_model.params['treatment:post_period']

def run_space_placebo(df, num_permutations=1000):
    placebo_effects = []
    
    # 获取所有的对照组 user_id
    control_users = df[df['treatment'] == 0]['user_id'].unique()
    num_treated_users = df[df['treatment'] == 1]['user_id'].nunique()
    
    for i in range(num_permutations):
        # 1. 随机打乱：从全量样本中随机抽取 N 个人假装他们是 "tretament组"
        fake_treated_ids = np.random.choice(df['user_id'].unique(), size=num_treated_users, replace=False)
        
        # 2. 构造含有虚假 treatment 标签的 df
        df_fake = df.copy()
        df_fake['fake_treatment'] = df_fake['user_id'].isin(fake_treated_ids).astype(int)
        
        # 3. 运行 DID 模型
        model = smf.ols("sales ~ fake_treatment * post_period", data=df_fake).fit()
        
        # 4. 记录虚假的交互项系数 (Treatment Effect)
        placebo_effects.append(model.params['fake_treatment:post_period'])
        
    return placebo_effects

# 运行检验
placebo_dist = run_space_placebo(df, 500)

# 可视化评判
import matplotlib.pyplot as plt
import seaborn as sns

sns.histplot(placebo_dist, kde=True)
plt.axvline(x=real_effect, color='red', linestyle='--', label=f'真实效应: {real_effect:.2f}')
plt.title("安慰剂检验：虚假干预效应的分布")
plt.legend()
plt.show()

# 计算 P-Value (真实效应落在虚假分布极端右侧的概率)
p_value = np.mean([abs(fake_eff) >= abs(real_effect) for fake_eff in placebo_dist])
print(f"安慰剂检验 P-Value: {p_value:.4f}")
# 若 P-Value < 0.05，则证明显著，效应并非巧合。
```
