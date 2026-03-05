# 📈 模块 D: 时序预测

> 📖 速查手册：[时序预测](12_time_series.md) | [评估指标](08_evaluation.md)
> 🎯 对应简历项目：**Story 2 — 大促仓储履约人力调度预测优化 (MAPE ≤ 8%)**

---

## 📺 第一步：看视频建立心智模型

|   #   | 视频                                                                           | 推荐度 & 食用指北                                                          |  时长  | 看完能理解什么                                          | 状态  |
| :---: | :----------------------------------------------------------------------------- | :------------------------------------------------------------------------- | :----: | :------------------------------------------------------ | :---: |
|   1   | [StatQuest: Time Series Concepts](https://www.youtube.com/watch?v=DeORzP0go5I) | ⭐⭐⭐⭐ **打底常识**<br>把 Autocorrelation 和 平稳性 讲得很透彻。不用记数学。 | ~15min | 平稳性、自相关的最直觉解释——为什么时间序列"不能乱洗牌"  |   ⬜   |
|   2   | [Krish Naik: Prophet Tutorial](https://www.youtube.com/watch?v=VtItg-J6-CI)    | ⭐⭐⭐⭐ **实战落地**<br>直接带你看代码和组件分解图，对你回答项目问题极有用。  | ~20min | Prophet 是如何自动分解 Trend + Seasonality + Holiday 的 |   ⬜   |
|   3   | [StatQuest: XGBoost (Part 1)](https://www.youtube.com/watch?v=OtD8wVaFm6E)     | ⭐⭐⭐⭐⭐ **一鱼两吃**<br>如果树模型模块看过了，这里当复习。残差预测是关键。   | ~25min | 理解残差拟合原理 → 这是 Prophet+XGBoost 组合的底层逻辑  |   ⬜   |

---

## 💡 第二步：核心概念卡片

!!! info "Prophet 原理：加法分解"
    $y(t) = trend(t) + seasonality(t) + holidays(t) + error(t)$
    **优势**：可解释性（分解后每个成分都能画出来）、自动检测趋势变化点、节假日用 dummy 变量。
    **劣势**：无法捕获复杂的非线性交互（促销强度×天气的联合效应）。

!!! info "Residual Learning（残差学习）"
    **Prophet 做基线** → 捕获大趋势和周期性。
    **XGBoost 做残差修正** → 引入外部特征（促销、天气、竞品活动），捕获 Prophet 漏掉的非线性信号。
    最终预测 = Prophet 预测 + XGBoost 对残差的预测。
    面试官最爱问"为什么不直接用 XGBoost？"→ 答案就是拆解线性趋势和非线性复杂因素。

!!! info "时序特征工程三件套"
    1. **Lag 特征**：`df['lag_7'] = df.groupby('store')['sales'].shift(7)` — 用 7 天前的销量预测今天
    2. **Rolling 特征**：`df['rolling_7d_mean'] = df.groupby('store')['sales'].transform(lambda x: x.rolling(7).mean())` — 近 7 天的移动平均
    3. **日期特征**：`dayofweek`, `is_weekend`, `is_month_end`, `is_holiday`

!!! info "Data Leakage 防线（时序最常犯的错误！）"
    **绝对不能**用标准 KFold CV → 必须用 **TimeSeriesSplit**（前向验证）。
    Rolling 特征如果在 split 前全局计算，测试集会包含未来信息 → 必须在每个 fold 内部单独计算。

!!! info "评估指标选型"
    | 指标            | 特点                     | 适用场景                             |
    | :-------------- | :----------------------- | :----------------------------------- |
    | **M[目标业务]** | 对大误差不敏感，直觉清晰 | 汇报人力偏差（"平均偏差 X 个人"）    |
    | **MAPE**        | 百分比，跨量级可比       | 汇报精度（"误差 8%"）                |
    | **RMSE**        | 对大误差极度敏感         | 惩罚极值预测（大促日偏差不可接受时） |

---

## ❓ 第三步：面试巩固题

### 基础题

??? note "Q1: Prophet 的原理？如何处理趋势、季节性和节假日？"
    **骨架**：加法分解 y = trend + seasonality + holidays + error → 自动检测变化点 → 节假日用 dummy 变量

??? note "Q2: XGBoost 建模时序时如何避免未来信息泄露？"
    **骨架**：TimeSeriesSplit → 特征只用历史窗口（lag/rolling）→ 禁止 shuffle → rolling 在每个 fold 内部计算

### 进阶题（来源：模拟面试）

??? warning "Q3: Prophet vs XGBoost 选型？为什么不直接用 XGBoost？ ⭐"
    **来源**：Gemini 模拟面试 Q5 + DeepSeek Q4
    **答法**：Prophet 擅长捕捉趋势和周期性，XGBoost 擅长特征交互。两者类似 **Residual Learning**。Prophet=基线，XGBoost=残差修正。

??? warning "Q4: 正常日 MAPE=15%，大促日 MAPE=45%。整体 25% 能上线吗？"
    **来源**：Antigravity 模拟面试 #2
    **答法**：不同意。整体指标掩盖了分布不均。大促日是业务最关键的时刻，误差 45% 不可接受 → 分层评估是核心

??? warning "Q5: 极值预测差之后你做了什么？"
    **来源**：Antigravity 模拟面试 Q7
    **答法**：三步闭环 → (1) 分析特征重要性，发现大促标记缺失 (2) 提议加入 is_promotion 特征 (3) 建议分段模型

??? warning "Q6: Prophet 和 XGBoost 预测结果矛盾，你信谁？"
    **来源**：Antigravity 模拟面试 Q8
    **答法**：取决于场景。日常信 Prophet（周期性更稳定），大促信 XGBoost（能利用促销特征）。实际做 Ensemble。

??? warning "Q7: 时间序列 Data Leakage 风险？"
    **来源**：Antigravity 模拟面试 Q9
    **答法**：绝对不能用 KFold → TimeSeriesSplit + rolling 特征在 fold 内部计算

??? warning "Q8: 手写时序特征工程代码（rolling/lag/月末）"
    **来源**：Antigravity 笔试 #1
    ```python
    # 7 天滚动均值
    df['rolling_7d_mean'] = df.groupby('store')['sales'].transform(
        lambda x: x.rolling(7).mean()
    )
    # 同比去年同日
    df['lag_365'] = df.groupby('store')['sales'].shift(365)
    # 月末最后 3 天
    df['is_month_end'] = df['date'].dt.day >= (
        df['date'].dt.days_in_month - 2
    )
    ```
