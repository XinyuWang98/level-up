# 🎯 聚类分析 (Clustering)

## K-Means 聚类 🎯
*物以类聚，人以群分。*

??? example "K-Means 完整流程 (Elbow + Silhouette + Profiling + 可视化)"

    ```python
    from sklearn.cluster import KMeans

    # 1. 肘部法则选 K (Elbow Method) & 自动找拐点 📉
    # 需安装: !pip install kneed

    from kneed import KneeLocator

    sse = []
    K_range = range(1, 10)

    # 1.1 计算 SSE
    for k in K_range:
        kmeans = KMeans(n_clusters=k, random_state=42)
        kmeans.fit(X_scaled)
        sse.append(kmeans.inertia_)

    # 1.2 自动寻找 "手肘点" (Elbow Point)
    # curve='convex' (凸), direction='decreasing' (下降)
    kl = KneeLocator(K_range, sse, curve="convex", direction="decreasing")

    print(f"🏆 最佳 K 值 (Elbow Point) 是: {kl.elbow}")

    # 1.3 可视化让老板信服
    kl.plot_knee()

    # 1.4 轮廓系数验证 (Silhouette Score) 👤
    # 辅助验证: 越大越好 (接近1最好, 0说明分不开, -1说明分错了)
    from sklearn.metrics import silhouette_score
    score = silhouette_score(X_scaled, kmeans.labels_)
    print(f"Silhouette Score: {score:.3f}")
    # > 0.5: 坚实 (Solid)
    # 0.2 ~ 0.5: 一般 (Average)
    # < 0.2: 也没啥别的办法了 (Weak)

    # 2. 聚类 & 打标 (Fit & Predict)
    kmeans = KMeans(n_clusters=3, random_state=42)
    df['cluster'] = kmeans.fit_predict(X_scaled) # 记得要先 StandardScale!

    # 3. 结果业务解读 (Profiling) 🗣️
    # 这一步最重要！告诉老板每一类人是谁。
    # 注意：看均值要用原始数据 (df)，不要用 Log/Scaled 后的数据！

    cluster_profile = df.groupby('cluster')[['Amount', 'Frequency', 'Recency']].mean()
    cluster_profile['count'] = df.groupby('cluster')['CustomerID'].count()
    print(cluster_profile)

    # 4. 可视化 (Pairplot & Snake Plot) 📊
    # (1) Pairplot: 两两变量对比，看聚类分得开不开
    sns.pairplot(df_scaled, hue='cluster', palette='viridis')

    # (2) Snake Plot (线图): 看每一组的特征差异
    # 需将数据 Melt 成长表
    df_melt = pd.melt(df_scaled.reset_index(), id_vars=['cluster'], value_vars=['Recency', 'Frequency', 'Monetary'])
    sns.lineplot(data=df_melt, x='variable', y='value', hue='cluster')
    plt.title("Snake Plot: Cluster Feature Comparison")
    ```

## Senior 秘籍: 规则派 vs 算法派 🥊
*有时候，简单的规则比算法更管用。*

**K-Means (算法派)**: 适合**探索**未知群体 (Unsupervised)。
**RFM Scoring (规则派)**: 适合**运营**会员体系 (Rule-based)。

??? example "RFM Scoring 代码实战 (绝杀面试题)"

    ```python
    # --- RFM Scoring 代码实战 (绝杀面试题) ---

    # 1. 自动打分 (1-5分)
    # R越小越好 (labels=[5,4,3,2,1]), F/M越大越好
    df['R_Score'] = pd.qcut(df['Recency'], 5, labels=[5, 4, 3, 2, 1])
    df['F_Score'] = pd.qcut(df['Frequency'].rank(method='first'), 5, labels=[1, 2, 3, 4, 5])
    df['M_Score'] = pd.qcut(df['Monetary'], 5, labels=[1, 2, 3, 4, 5])

    # 2. 算总分 (3-15分)
    df['Total_Score'] = df[['R_Score', 'F_Score', 'M_Score']].sum(axis=1)

    # 3. 业务解读
    # 满分用户 (555) -> SVIP
    # 流失用户 (111) -> 召回对象
    print(df.groupby('Total_Score')['Monetary'].mean())
    ```

## 密度聚类 (DBSCAN) 🕵️‍♂️
*不强行归类，专门抓异常值 (Outliers) & 团伙识别 (Gang Detection)。*

*   **适用场景**: 地理位置聚类 (外卖站点)、风控团伙挖掘 (黑产设备关联)。

??? example "DBSCAN 完整流程"

    ```python
    from sklearn.cluster import DBSCAN

    # 1. 训练 (无需指定 K，要调 eps 和 min_samples)
    # eps: 邻域半径 (多远算邻居?)
    # min_samples: 最小样本数 (几个人凑一堆才算组织?)
    # 💡 调参心法: 
    #   - eps 难定? 用 K-Distance Graph 找"手肘点".
    #   - min_samples 难定? 默认 5, 数据量大时调大.
    dbscan = DBSCAN(eps=0.5, min_samples=5)
    X_scaled = StandardScaler().fit_transform(X) # 必须标准化!
    clusters = dbscan.fit_predict(X_scaled)

    # 2. 结果分析 - 自动识别 -1 (噪音/异常值)
    n_outliers = list(clusters).count(-1)
    print(f"发现异常值数量: {n_outliers}")

    df['cluster_dbscan'] = clusters

    # 3. 结果业务解读 🗣️
    # (1) 看均值: 既然归为一类，肯定有共性
    print(df.groupby('cluster_dbscan').agg(['mean', 'median']))

    # (2) 重点分析异常值 (-1): 它们到底哪里怪?
    normal = df[df['cluster_dbscan'] != -1]
    noise = df[df['cluster_dbscan'] == -1]
    print("异常点特征差异:\n", noise.mean() - normal.mean())

    # 3. 可视化 (噪音点标红) 📊
    plt.scatter(X[clusters!=-1, 0], X[clusters!=-1, 1], c=clusters[clusters!=-1], cmap='viridis', label='Normal')
    plt.scatter(X[clusters==-1, 0], X[clusters==-1, 1], c='red', marker='x', s=100, label='Noise')
    plt.legend()
    plt.title("DBSCAN with Noise Detection")
    ```

## 降维打击 (PCA) 📉
*把高维数据压扁成 2D/3D，方便画图或去噪。*

??? example "PCA 降维代码模板"

    ```python
    from sklearn.decomposition import PCA

    # 1. 实例化 (n_components=2 降到2维)
    pca = PCA(n_components=2) 

    # 2. 拟合 & 转换
    X_pca = pca.fit_transform(X_scaled) # 记得先标准化!

    # 3. 这一刀砍下去损失了多少信息?
    print(pca.explained_variance_ratio_) 
    # [0.4, 0.3] -> 第1主成分40%，第2主成分30% -> 总共保留了 70%

    # 4. 可视化
    plt.scatter(X_pca[:, 0], X_pca[:, 1], c=y, alpha=0.7)
    plt.xlabel('Principal Component 1')
    plt.ylabel('Principal Component 2')
    ```
