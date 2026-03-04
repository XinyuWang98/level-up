# 📦 模型落地 (Model Deployment)
*不想每次预测都重新训练？把模型存成文件！*

## 核心概念：Input / Output 🔄

在生产环境中，**训练**和**预测**是两个完全分离的流程 (Pipeline)。

### 1. 训练流程 (Training Pipeline) - 频率低 (周/月)
*   **输入**: 历史数据 (History Data)
*   **动作**: `fit()` → 学习参数 (Weights, Mean, Variance)
*   **输出**: **模型文件** (`.pkl`)
*   **代码**:
    ```python
    # 训练并保存整个 Pipeline (包含预处理+模型)
    pipeline = Pipeline([
        ('scaler', StandardScaler()),
        ('model', XGBClassifier())
    ])
    pipeline.fit(X_train, y_train)
    joblib.dump(pipeline, 'model_v1.pkl') # -> 生成文件
    ```

### 2. 预测流程 (Inference Pipeline) - 频率高 (实时/天)
*   **输入**: 新数据 (New Data) + **模型文件** (`.pkl`)
*   **动作**: `load()` → `predict()` (注意：这里**绝对不运行** `fit`)
*   **输出**: 预测结果 (Predictions)
*   **代码**:
    ```python
    # 加载模型 (只读)
    model = joblib.load('model_v1.pkl')
    # 预测 (直接用，不要再 fit！)
    predictions = model.predict(X_new)
    ```

---

## 常见误区 (Myth Busting) 🛑

### Q: 我需要把"更新参数"和"不更新参数"拆成两个文件吗？
**A: 不需要！也不建议！**
*   **最佳实践**: 将预处理(`Scaler`)和模型(`Model`)打包成一个 `Pipeline` 对象保存。
*   **原因**: 预测时的 `StandardScaler` 必须用训练时的 `Mean/Std` (保存在对象里了)。如果你拆开了，很容易搞丢或者不匹配。
*   **更新方式**: 如果要更新参数，就**重新运行训练流程**，覆盖旧的 `.pkl` 文件即可。

---

## 代码实战: Joblib 💾

```python
import joblib

# 1. 保存模型 (Dump)
# 💡 Pro Tip: 文件名带上日期/版本号，防止覆盖！
joblib.dump(model, 'churn_model_20231027.pkl') 

# 2. 加载模型 (Load)
loaded_model = joblib.load('churn_model_20231027.pkl')

# 3. 验证 (Verify)
# 确保加载后的模型预测结果和原模型一致
assert (model.predict(X_test) == loaded_model.predict(X_test)).all()
print("✅ 模型加载成功，可以直接上线！")
```

## 为什么选 joblib 而不是 pickle？
*   `joblib` 对 **NumPy 数组** (矩阵) 做了专门的压缩优化。
## 进阶：时间序列预测的陷阱 (Lookback Window) 🕰️

如果你的模型用了 `Lag Feature` (例如 `sales_lag_7`)，**你就不能只给模型当天的 Input**。

### 示意图：预测 11月1日 (T+1) 的销量

你必须在数据库里**回溯**至少 7 天的历史数据，才能算出来 `11月1日` 这一行的特征。

```text
[Database (History)]               [Feature Engineering]           [Model Input (X_new)]        [Output]
--------------------               ---------------------           ---------------------        --------
10-25: 销量=100  (Lag 7)  ──┐
...                         │  👉  Rolling/Shift 计算   👉      Date: 11-01                  预测值: 108
10-31: 销量=105  (Lag 1)  ──┘                                  Lag_1: 105
                                                               Lag_7: 100
```
### 结论
*   **Cold Start**: 如果你是新店，没有 `10-25` 的数据，`Lag_7` 就是 `NaN` → 模型报错。
*   **Data Pipeline**: 你的预测脚本必须有权限**读取历史数据**，而不仅仅是接收当前的请求。
