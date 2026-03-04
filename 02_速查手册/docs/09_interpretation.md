# 🕵️ SHAP 模型解释

## 模型解释 (Interpretation with SHAP) 🕵️‍♀️
*不再是黑盒！告诉业务方**为什么**模型做这个预测。*

```python
import shap

# 1. 创建解释器 (TreeExplainer for XGBoost/RandomForest)
explainer = shap.TreeExplainer(model)

# 2. 计算 SHAP 值 (虽然慢，但从不让你失望)
shap_values = explainer.shap_values(X_test)

# 3. 核心可视化 (Global Importance)
# 颜色越红=值越大，点越右=正向影响越强
shap.summary_plot(shap_values[1], X_test) # [1] 代表关注 "流失/正例"

# 4. 🔥 个人归因 (Local Explanation - Waterfall)
# 为什么【这个】用户会被预测流失？(老板最爱看的图)
# 注意：新版 SHAP 写法变了，千万别用旧版 list 写法！
explanation = explainer(X_test) # 生成智能对象
idx = 0 # 挑一个高风险用户
shap.plots.waterfall(explanation[idx]) 
# 解读: 红色条=推高流失概率，蓝色条=拉低流失概率
```

## 面试怎么讲 SHAP？

**全局 (Global) - Summary Plot:**
> "我用 SHAP 分析了模型的全局特征重要性，发现 `合同类型` 和 `月费` 是影响客户流失的最大因子。月费越高的客户流失概率越大。"

**个体 (Local) - Waterfall Plot:**
> "对于这个具体的高风险用户，SHAP 瀑布图显示：他的 `合同=月付` 把流失概率往上推了 15%，而他的 `在网时长=2年` 又概率拉回了 8%。综合来看，最大的风险因素是他的月付合同。"

!!! warning "SHAP 不是因果推断 (Correlation ≠ Causation)"
    *   SHAP 解释的是 **"模型是怎么想的"** (Model Interpretation)，而不是 **"世界的真相"** (Causal Inference)。
    *   **例子**: 模型发现 "买冰淇淋的人更容易溺水" (SHAP > 0)，是因为夏天两者都多 (共线性)。
    *   **真相**: 禁止卖冰淇淋**不能**减少溺水！(干预无效)。
    *   要回答 "如果我干预 X，Y 会怎么变？"，请出门左转找 **[15_causal_inference.md](15_causal_inference.md)**。
