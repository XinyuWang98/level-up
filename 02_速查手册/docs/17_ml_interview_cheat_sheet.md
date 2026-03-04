# 🎯 机器学习面试突击 & 核心代码速查 (ML Interview Cheat Sheet)

> **🎉 "明天就是除夕了，我只想躺着刷视频，别让我写代码"** (Designed for Lunar New Year Eve Review)

## 1. 灵魂拷问：这个函数从哪来？(Library Imports) 📚
*面试白板手写代码必备！不要只记得函数名，忘了库名！*

| 功能模块 (Functionality) | 函数/类名 (Class/Function)                    | 来源库 (Import Source)    | 备注 (Note)                                            |
| :----------------------- | :-------------------------------------------- | :------------------------ | :----------------------------------------------------- |
| **数据切分**             | `train_test_split`                            | `sklearn.model_selection` | 别写成 `sklearn.cross_validation` (那是一百年前的事了) |
| **交叉验证**             | `cross_val_score`, `KFold`                    | `sklearn.model_selection` |                                                        |
| **网格搜索**             | `GridSearchCV`, `RandomizedSearchCV`          | `sklearn.model_selection` | 调参神器                                               |
| **评估指标 (回归)**      | `mean_absolute_error`, `mean_squared_error`   | `sklearn.metrics`         | MAE, MSE                                               |
| **评估指标 (回归)**      | `mean_absolute_percentage_error`              | `sklearn.metrics`         | MAPE (注意分母为0)                                     |
| **评估指标 (分类)**      | `accuracy_score`, `roc_auc_score`, `f1_score` | `sklearn.metrics`         | 还有 `log_loss`                                        |
| **模型报告 (分类)**      | `classification_report`                       | `sklearn.metrics`         | 一次性打印 Precision/Recall/F1                         |
| **混淆矩阵**             | `confusion_matrix`                            | `sklearn.metrics`         |                                                        |
| **缺失值填补**           | `SimpleImputer`                               | `sklearn.impute`          | 别忘了 `strategy='mean'`                               |
| **标准化**               | `StandardScaler`, `MinMaxScaler`              | `sklearn.preprocessing`   | 比如把 [0, 1000] 缩放到 [0, 1]                         |
| **独热编码**             | `OneHotEncoder`                               | `sklearn.preprocessing`   |                                                        |
| **Label 编码**           | `LabelEncoder`                                | `sklearn.preprocessing`   | 把 ['Yes', 'No'] 变成 [1, 0]                           |
| **Pipeline**             | `Pipeline`, `make_pipeline`                   | `sklearn.pipeline`        | 把 Scaler 和 Model 串起来                              |
| **保存模型**             | `dump`, `load`                                | `joblib`                  | 别用 `pickle` 了，`joblib` 对 numpy 数组更快           |

---

## 2. 模型参数大比拼 (Reg vs Cls) ⚔️
*XGBoost 和 LightGBM 的参数几乎一样，但目标函数 (Objective) 不同。*

### 核心参数 (Common Hyperparameters)
这些参数是你调参时**必须知道**的：

| 参数名 (Param)     | 含义 (Meaning)                | 调大还是调小？(Tuning Direction)      | 备注                                     |
| :----------------- | :---------------------------- | :------------------------------------ | :--------------------------------------- |
| `n_estimators`     | **树的数量** (迭代次数)       | 越大越准，但越慢且容易过拟合          | 通常设 1000，配合 `early_stopping`       |
| `learning_rate`    | **学习率** (步长)             | 越小越稳 (0.01-0.05)，但需要更多的树  | 太大 (0.1+) 容易震荡                     |
| `max_depth`        | **树的最大深度**              | 越大越复杂 (拟合能力强)，越容易过拟合 | XGB 默认6，LGB 默认-1 (不限)。通常 3-10  |
| `subsample`        | **行采样比例** (Row Sampling) | < 1.0 (如 0.8) 可以防止过拟合         | 每次只用 80% 的数据训练一棵树            |
| `colsample_bytree` | **列采样比例** (Col Sampling) | < 1.0 (如 0.8) 可以防止过拟合         | 每次只选 80% 的特征 (类似 Random Forest) |
| `reg_alpha` (L1)   | **L1 正则化** (Lasso)         | 越大越稀疏 (特征选择)，防止过拟合     | 筛掉没用的特征                           |
| `reg_lambda` (L2)  | **L2 正则化** (Ridge)         | 越大越平滑 (权重变小)，防止过拟合     | 默认都有点 L2                            |

### 场景差异 (Task Specific)

| 场景                  | 关键参数 (Key Param) | 设置值 (Value)                                       | 解释 (Why?)              |
| :-------------------- | :------------------- | :--------------------------------------------------- | :----------------------- |
| **回归 (Regression)** | `objective`          | `'reg:squarederror'` (XGB) <br> `'regression'` (LGB) | 最小化均方误差           |
|                       | `eval_metric`        | `'rmse'`, `'mae'`, `'mape'`                          | 评估看什么？             |
| **二分类 (Binary)**   | `objective`          | `'binary:logistic'` (XGB) <br> `'binary'` (LGB)      | 输出概率 (0-1)           |
|                       | `eval_metric`        | `'auc'`, `'logloss'`, `'error'`                      | 评估看 AUC 还是 错误率？ |
| **多分类 (Multi)**    | `objective`          | `'multi:softmax'` (XGB) <br> `'multiclass'` (LGB)    | 输出类别 (0, 1, 2...)    |
|                       | `num_class`          | `3` (如果有3类)                                      | **必须指定类别数量！**   |

---

## 3. 面试突击题库 (Q&A) 🥊
*明天你在看电视的时候，脑子里过一遍这些问题。*

### Q1: 为什么要用 Validation Set (验证集)？为什么不能只分 Train/Test？
*   **A**: 因为我们需要**调参** (Tuning)。如果你用 `Test Set` 来调参，模型就会"偷看"考试答案 (Info Leakage)，导致上线后效果变差。Validation Set 是用来做模拟考的。
*   **Pro**: 最好用 Cross-Validation (交叉验证)，因为数据可能切得不巧。

### Q2: 什么是各种 "Encoder"？LabelEncoder vs OneHotEncoder?
*   **OneHot**: 适合**无序**类别 (颜色: 红/绿/蓝)。缺点：特征会变多 (稀疏)。
*   **Label**: 适合**有序**类别 (尺码: S/M/L) 或者树模型 (Tree Model)。树模型可以处理 Label Encoding (因为它能切分 `size > 1`)，不需要 OneHot。

### Q3: XGBoost 和 Random Forest 有什么区别？(必考)
*   **RF (Bagging)**: "臭皮匠开会"。大家**并行**训练，每棵树独立，最后投票。目的是**减少方差** (Variance)，不容易过拟合。
*   **XGB (Boosting)**: "接力赛"。大家**串行**训练，后一棵树专门**纠正**前一棵树的错误 (Residual)。目的是**减少偏差** (Bias)，拟合能力极强，但容易过拟合。

### Q4: 什么是 Data Leakage？给个例子？(必考)
*   **定义**: 训练时用到了**预测时拿不到**的信息。
*   **例子**: 预测"明天是否下雨"，特征里包含了"明天的降水量" (废话，都知道降水量了还需要预测吗？)。
*   **实战例子**: 预测"用户是否还会购买"，特征里用了"用户下一次购买时间"。

### Q5: 为什么分类任务要看 AUC 而不是 Accuracy？
*   **A**: 因为**样本不平衡** (Imbalanced)。
*   如果坏人只有 1%，我全部猜"好人"，Accuracy 也有 99%！但这模型是废物。AUC 能反映模型对"坏人"的排序能力，不受比例影响。

---

## 4. 推荐视频 (Video List for Holiday) 📺
*放松心情，不用动脑，在这个假期把这些概念"听"进去。*

1.  **StatQuest with Josh Starmer** (墙裂推荐！🔥)
    *   **Topic**: [Machine Learning Playlist](https://www.youtube.com/watch?v=Gv9_4yMHFhI&list=PLblh5JKOoLUICTaGLRoHQDuF_7q2GfuJF)
    *   **必看**:
        *   [Gradient Descent, Step-by-Step](https://www.youtube.com/watch?v=sDv4f4s2SB8) (搞懂梯度下降)
        *   [XGBoost Part 1: Regression](https://www.youtube.com/watch?v=OtD8wVaFm6E) (看它是怎么拟合残差的)
        *   [ROC and AUC, Clearly Explained](https://www.youtube.com/watch?v=4jRBRDbJemM) (最清晰的 AUC 解释)
    *   *特点*: "BAM!", "Double BAM!"，非常幽默，用简单的图解释复杂的数学。

2.  **3Blue1Brown** (硬核数学直观化)
    *   **Topic**: [Neural Networks](https://www.youtube.com/watch?v=aircAruvnKk)
    *   *特点*: 动画极其精美，看完你会对"权重"和"偏置"有深刻的几何理解。

3.  **Kaggle Grandmaster Interviews**
    *   在 YouTube 搜 "Kaggle Grandmaster Tip"，听听大神们怎么做 Feature Engineering。
