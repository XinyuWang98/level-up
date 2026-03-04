# 📊 可视化 (Visualization) - Seaborn 专场 🎨

## 1. 看分布 (Distribution)

| 图表       | 函数             | 典型场景                  | 关键参数                                                           |
| :--------- | :--------------- | :------------------------ | :----------------------------------------------------------------- |
| **直方图** | `sns.histplot`   | 任何数值分布 (年龄/收入)  | `kde=True` (密度线), `bins=30` (颗粒度), `hue='group'` (分组对比)  |
| **箱线图** | `sns.boxplot`    | 对比多组的"中位数/离群点" | `x='group', y='value'` (横向对比), `showfliers=False` (隐藏异常值) |
| **小提琴** | `sns.violinplot` | 箱线图 + 密度图 (看胖瘦)  | `split=True` (左右分边对比)                                        |

## 2. 看关系 (Relationship)

| 图表       | 函数              | 典型场景                      | 关键参数                                                            |
| :--------- | :---------------- | :---------------------------- | :------------------------------------------------------------------ |
| **散点图** | `sns.scatterplot` | 两个数值的相关性 (身高vs体重) | `hue='gender'` (颜色), `style='class'` (形状), `alpha=0.6` (透明度) |
| **折线图** | `sns.lineplot`    | 时间序列 / 趋势变化           | `hue='segment'` (多条线), `ci=None` (去阴影)                        |

## 3. 看分类 (Categorical)

| 图表       | 函数            | 典型场景                | 关键参数                                                   |
| :--------- | :-------------- | :---------------------- | :--------------------------------------------------------- |
| **柱状图** | `sns.barplot`   | 类别 vs 数值 (均值对比) | `ci=None` (不显示误差棒), `estimator=sum` (求和而不是均值) |
| **计数图** | `sns.countplot` | 既然是分类，有多少个？  | `x='class'` (横着数), `y='class'` (竖着数)                 |
| **横条图** | `df.plot.barh`  | **排名专用** (Top 10)   | `ax=axes[1]` (指定画板), `color='green'`                   |

## 4. 看占比与热力 (Composition & Heatmap)

| 图表       | 函数          | 典型场景                 | 关键参数                                                        |
| :--------- | :------------ | :----------------------- | :-------------------------------------------------------------- |
| **饼图**   | `plt.pie`     | **占比** (市场份额/男女) | `autopct='%1.1f%%'` (显示百分比), `explode=[0, 0.1]` (突出某块) |
| **热力图** | `sns.heatmap` | **相关性** / **缺失值**  | `annot=True` (显示数字), `cmap='coolwarm'` (红蓝配色)           |

!!! warning "审美警告 (Aesthetics Warning)"

    *   **饼图 (Pie Chart)** 在专业分析中**不受欢迎**（人眼对面积不敏感）。
    *   **推荐替代**: 用 **横向条形图 (Barh)** 代替饼图，更清晰、更专业。

!!! tip "批量体检 (Bulk Plotting) & 子图 (Subplots)"

    *   `plt.subplots(1, 2)`: 就像切蛋糕，切成 1行2列。
    *   `axes[0]`: 第1块蛋糕 (左图)。
    *   `axes[1]`: 第2块蛋糕 (右图)。

    ```python
    # 1. 准备画板 (1行2列)
    fig, axes = plt.subplots(1, 2, figsize=(15, 6))

    # 2. 画左边 (指定 ax=axes[0])
    sns.boxplot(data=df, x='label', y='age', ax=axes[0])
    axes[0].set_title('Age Distribution')

    # 3. 画右边 (指定 ax=axes[1])
    sns.countplot(data=df, x='gender', ax=axes[1])
    axes[1].set_title('Gender Count')

    plt.tight_layout() # 自动调整间距，防止重叠
    ```

    *   不想一个个敲？一个循环搞定所有数值列的对比！(eda_loop)

    ```python
    # 1. 自动筛选所有数值列 (排除掉 label)
    num_cols = df.select_dtypes(include=['number']).columns.tolist()
    if 'label' in num_cols: num_cols.remove('label')

    # 2. 循环画图 (subplot)
    plt.figure(figsize=(15, 10))
    for i, col in enumerate(num_cols):
        plt.subplot(3, 3, i+1) # 假设有9个变量，3x3排列
        sns.boxplot(data=df, x='label', y=col) # 对比 label=0/1 的分布差异
        plt.title(col)
    plt.tight_layout()
    ```


!!! tip "相关性热力图 (Correlation Heatmap)"

    *   **进阶版**: 加个 `mask` 只显示左下角 (因为矩阵是对称的，右上角是重复信息)。

    ```python
    plt.figure(figsize=(10, 8))
    corr = df.corr(numeric_only=True)
    # mask=np.triu(...) 用于遮挡上半三角，看起来更 Senior
    sns.heatmap(corr, annot=True, cmap='coolwarm', fmt='.2f', 
                mask=np.triu(np.ones_like(corr, dtype=bool)))
    ```

## 5. 性能优化 (Performance Tips) 🚀
*几百万行数据画图卡死？CPU没跑满？看这里。*

*   **核心原因**: Matplotlib/Seaborn 画图是单线程的，而且会尝试画出每一个点。
*   **解决方案**: **采样 (Sampling)**。画分布图看趋势，1万条和100万条是一样的。

```python
# 💡 别傻傻地画 50万个点！
# data=df -> data=df.sample(10000)
sns.histplot(data=df.sample(min(10000, len(df))), x='price', bins=50)

# 散点图同理
sns.scatterplot(data=df.sample(10000), x='age', y='income', alpha=0.3)
```
