# 🗣️ NLP 文本分析 (Natural Language Processing)
*让机器读懂"人话" (Text Mining)。*

## 1. 文本预处理 (Preprocessing) 🧹
*垃圾进，垃圾出 (Garbage In, Garbage Out)。文本清洗决定了分析上限。*

| 步骤 (Step)     | 动作 (Action)                | 核心代码 (Code Snippet)                     | 目的 (Why?)                                              |
| :-------------- | :--------------------------- | :------------------------------------------ | :------------------------------------------------------- |
| **1. 清洗**     | **正则去噪** (Regex)         | `re.sub(r'[^\u4e00-\u9fa5]', '', text)`     | 只留中文，去掉表情包/标点/乱码。                         |
| **2. 分词**     | **切词** (Tokenization)      | `jieba.lcut(text)`                          | 中文没有空格，必须切分 ("我爱北京" → "我", "爱", "北京") |
| **3. 去停用词** | **过滤** (Stopwords Removal) | `[w for w in words if w not in stop_words]` | 去掉 "的/了/呢" 这种没意义的词。                         |

### 🐍 标准起手式 (Jieba Boilerplate):
??? example "🐍 Jieba 标准起手式"

    ```python
    import jieba
    import re

    def clean_text(text):
        # 1. 正则去噪 (只留中文 + 英文 + 数字)
        text = re.sub(r"[^a-zA-Z0-9\u4e00-\u9fa5]", "", str(text))
        # 2. 分词
        words = jieba.lcut(text)
        # 3. 去停用词 (假设 stop_words 已定义)
        return " ".join([w for w in words if w not in stop_words])

    df['clean_text'] = df['content'].apply(clean_text)
    ```

### 🔤 英文文本预处理 (NLTK Boilerplate)

??? example "🔤 NLTK 英文标准起手式"

    ```python
    import re
    import nltk
    from nltk.corpus import stopwords
    from nltk.tokenize import word_tokenize
    from nltk.stem import WordNetLemmatizer

    # Step 1: 初始化工具
    lemmatizer = WordNetLemmatizer()          # 词形还原器 (running → run)
    stop_words = set(stopwords.words('english'))  # 英文停用词表

    # Step 2: 业务自定义停用词 (根据场景添加)
    CUSTOM_STOPWORDS = {'order', 'product', 'item', 'please', 'thank', 'service'}
    stop_words = stop_words.union(CUSTOM_STOPWORDS)

    # Step 3: 预处理函数
    def preprocess_text(text: str) -> str:
        if pd.isna(text):
            return ''
        text = text.lower()                          # 小写化
        text = re.sub(r'[^a-zA-Z\s]', ' ', text)     # 正则去噪: 只保留字母+空格
        tokens = word_tokenize(text)                  # 分词
        tokens = [
            lemmatizer.lemmatize(token)               # 词形还原
            for token in tokens
            if token.isalpha()         # 过滤非纯字母 token
            and token not in stop_words  # 去停用词
            and len(token) > 2           # 去短词
        ]
        return ' '.join(tokens)

    df['clean_text'] = df['remarks'].apply(preprocess_text)
    ```

### 🧩 字符串类型检查方法速查

| 方法         | 作用        | 示例                        | NLP 场景                |
| :----------- | :---------- | :-------------------------- | :---------------------- |
| `.isalpha()` | 全是字母?   | `'hello'.isalpha()` → True  | **过滤数字/标点 token** |
| `.isdigit()` | 全是数字?   | `'123'.isdigit()` → True    | 提取数字实体            |
| `.isalnum()` | 字母或数字? | `'abc123'.isalnum()` → True | 宽松过滤                |
| `.isspace()` | 全是空白?   | `'  '.isspace()` → True     | 跳过空白 token          |

## 2. 向量化 (Vectorization) 📐
*把文本变成数学向量，机器才能算。*

### 核心对比: Count vs TF-IDF

| 方法 (Method)       | 原理 (Concept)            | 结果示例 (Example)     | 适用场景 (Scenario)                 |
| :------------------ | :------------------------ | :--------------------- | :---------------------------------- |
| **CountVectorizer** | **词频统计** (数人头)     | `[2, 0, 1]` (整数)     | **LDA 主题模型** (概率模型只认整数) |
| **TfidfVectorizer** | **权重计算** (物以稀为贵) | `[0.1, 0, 0.9]` (小数) | **分类/聚类** (XGBoost/K-Means)     |

### 🔑 什么时候用 TF-IDF，什么时候用 LDA?

| 场景                        | 用什么                    | 为什么                     |
| :-------------------------- | :------------------------ | :------------------------- |
| **有主题标签** (算法已打标) | TF-IDF → GroupBy 标签     | 主题已知，只需下钻找痛点词 |
| **无标签** (冷启动探索)     | CountVectorizer → LDA     | 要机器帮你“猜”出主题       |
| **做分类/预测**             | TfidfVectorizer → XGBoost | 权重特征更适合监督学习     |

### 🔥 全集 TF-IDF → 按标签 GroupBy 提取痛点词 (用户行为轨迹 SOP)
*当业务已有主题标签时，不需要 LDA，直接用这套流程。*

??? example "🔥 TF-IDF GroupBy 主题痛点词提取 SOP"

    ```python
    from sklearn.feature_extraction.text import TfidfVectorizer

    # === Step 1: 全集统一跑 TF-IDF (保证 IDF 基准一致) ===
    TFIDF_MAX_FEATURES = 500   # 保留前 500 个高频词
    TFIDF_MIN_DF = 5           # 至少出现 5 次的词才保留
    TFIDF_NGRAM_RANGE = (1, 2) # 包含二元组捕捉短语

    tfidf = TfidfVectorizer(
        max_features=TFIDF_MAX_FEATURES,
        min_df=TFIDF_MIN_DF,
        ngram_range=TFIDF_NGRAM_RANGE
    )
    X_tfidf = tfidf.fit_transform(df_text['clean_text'])

    # === Step 2: 转 DataFrame，附上主题标签列 ===
    df_tfidf = pd.DataFrame(
        X_tfidf.toarray(),
        columns=tfidf.get_feature_names_out(),
        index=df_text.index
    )
    df_tfidf['category'] = df_text['category'].values

    # === Step 3: 按主题 GroupBy → 每个主题取 Top N 高权重词 ===
    topic_keywords = df_tfidf.groupby('category').mean(numeric_only=True)
    for topic in topic_keywords.index:
        top_words = topic_keywords.loc[topic].nlargest(10)
        print(f'--- {topic} ---')
        print(top_words.to_string())

    # === Step 4 (进阶): 差评独有痛点词 = 差评权重 - 好评权重 ===
    df_tfidf['is_negative'] = df_text['is_negative'].values
    word_cols = tfidf.get_feature_names_out()
    neg_avg = df_tfidf.loc[df_tfidf['is_negative']==1, word_cols].mean()
    pos_avg = df_tfidf.loc[df_tfidf['is_negative']==0, word_cols].mean()
    pain_points = (neg_avg - pos_avg).nlargest(10)  # 差值最大 = 差评独有词
    ```

### 🐍 TF-IDF 核心逻辑:
*   **TF (Term Frequency)**: 词频。这个词在这篇文章里出现的次数。
*   **IDF (Inverse Document Frequency)**: 逆文档频率。出现次数越少，IDF 越大 (权重越高)。

??? example "TF-IDF 向量化代码模板"

    ```python
    from sklearn.feature_extraction.text import TfidfVectorizer

    # 1. 实例化 (max_features=1000 抓大放小)
    tfidf = TfidfVectorizer(max_features=1000, min_df=2)

    # 2. 拟合 & 转换
    X_vec = tfidf.fit_transform(df['clean_text'])

    # 3. 变成 DataFrame (给人看)
    df_vec = pd.DataFrame(X_vec.toarray(), columns=tfidf.get_feature_names_out())
    ```

## 3. 主题模型 (LDA Topic Modeling) 🎭
*无监督学习：从一堆乱七八糟的评论里，自动总结出 K 个讨论主题。*

*   **输入**: Count Vector (整数词频矩阵)。
*   **输出**:
    1.  **Topic-Word 分布**: 每个主题由哪些词组成？
    2.  **Doc-Topic 分布**: 每篇文章属于哪个主题？

??? example "LDA 主题模型代码模板"

    ```python
    from sklearn.decomposition import LatentDirichletAllocation

    # 1. 必须用 CountVectorizer!
    cv = CountVectorizer(max_features=1000, min_df=5)
    X_count = cv.fit_transform(df['clean_text'])

    # 2. 训练 LDA (n_components = 主题数)
    lda = LatentDirichletAllocation(n_components=3, random_state=42)
    lda.fit(X_count)

    # 3. 打印每个主题的核心词 (Top 10 Words)
    feature_names = cv.get_feature_names_out()
    for topic_idx, topic in enumerate(lda.components_):
        top_words = [feature_names[i] for i in topic.argsort()[:-11:-1]]
        print(f"Topic {topic_idx}: {top_words}")

    # 4. 给每篇文章打标签
    topic_values = lda.transform(X_count)
    df['topic'] = topic_values.argmax(axis=1)
    ```

## 4. 监督学习 (Classification) 🏷️
*让机器学会区分好评/差评。*

| 模型 (Model)            | 场景 (Scenario)           | 优点 (Pros)                     | 缺点 (Cons)            |
| :---------------------- | :------------------------ | :------------------------------ | :--------------------- |
| **Naive Bayes**         | **Baseline (基准线)**     | **极快**，适合文本分类          | 假设特征独立，精度一般 |
| **Logistic Regression** | **Industrial (工业标准)** | **可解释性强** (Feature Weight) | 无法捕捉非线性关系     |

### 🐍 文本分类黄金模板:

??? example "🐍 文本分类黄金模板 (Naive Bayes / LR)"

    ```python
    from sklearn.model_selection import train_test_split
    from sklearn.naive_bayes import MultinomialNB
    from sklearn.linear_model import LogisticRegression
    from sklearn.metrics import classification_report

    # 1. 切分 (详见 [✂️ 06b_data_splitting](06b_data_splitting.md))
    X_train, X_test, y_train, y_test = train_test_split(X_vec, df['label'], test_size=0.2, random_state=42)

    # 2. 训练
    model = LogisticRegression()
    model.fit(X_train, y_train)

    # 3. 评估
    y_pred = model.predict(X_test)
    print(classification_report(y_test, y_pred))

    # 4. 解释 (LR Only) - 看哪些词决定了分类
    import numpy as np
    feature_names = np.array(tfidf.get_feature_names_out())
    for i, label in enumerate(model.classes_):
        top10 = np.argsort(model.coef_[i])[-10:]
        print(f"{label}: {feature_names[top10]}")
    ```

### 🌲 进阶：树模型 (XGBoost) - 精度之王:
*注意：XGBoost 不支持字符串标签，必须先 LabelEncoder！*

??? example "🌲 XGBoost 文本分类模板"

    ```python
    from xgboost import XGBClassifier
    from sklearn.preprocessing import LabelEncoder

    # 1. 标签编码 (必须做！)
    le = LabelEncoder()
    y_train_enc = le.fit_transform(y_train)
    y_test_enc = le.transform(y_test)

    # 2. 定义模型
    model = XGBClassifier(
        n_estimators=100, learning_rate=0.1,
        max_depth=6, subsample=0.8,
        colsample_bytree=0.8, n_jobs=-1, random_state=42
    )

    # 3. 训练与预测
    model.fit(X_train_vec, y_train_enc)
    y_pred_enc = model.predict(X_test_vec)

    # 4. 转回字符串标签
    y_pred = le.inverse_transform(y_pred_enc)
    print(classification_report(y_test, y_pred))
    ```

### 评估指标详解 (Classification Metrics) 📊

| 指标 (Metric)             | 含义 (Meaning)                   | 业务场景 (Business Scenario)   | 口诀 (Mnemonic) |
| :------------------------ | :------------------------------- | :----------------------------- | :-------------- |
| **Precision**<br>(精确率) | 抓到的坏人里，有多少是真的坏人？ | 垃圾邮件拦截 / 贷款审批        | 查准率          |
| **Recall**<br>(召回率)    | 真正的坏人里，你抓到了多少？     | 癌症筛查 / 欺诈检测 / 流失预警 | 查全率          |
| **F1-Score**              | Precision 和 Recall 的平衡点     | 通用场景 / 数据不平衡          | 端水大师        |
| **Support**               | 该类别的真实样本数               | 数据不平衡时注意               | 样本量          |

!!! important "黄金法则"

    Precision 和 Recall 往往是**此消彼长**的。
    **Senior DA 的价值**: 根据业务成本来决定**阈值 (Threshold)**。

## 5. 无监督学习 (Clustering) 🧩

| 模型 (Model) | 场景 (Scenario)       | 优点 (Pros)                  | 缺点 (Cons)                  |
| :----------- | :-------------------- | :--------------------------- | :--------------------------- |
| **K-Means**  | **通用聚类**          | 简单、直观、快               | 需要指定 K 值；对异常值敏感  |
| **DBSCAN**   | **密度聚类/异常检测** | 不需要指定 K；能发现任意形状 | 参数 (eps, min_samples) 难调 |

**⚠️ 关键坑点 (The "Language Trap"):**

*   多语言数据用 TF-IDF + K-Means 聚类，结果往往是 **按语言聚类**，而不是按话题。
*   **解法**: 分而治之 或 使用多语言 Embeddings (BERT, LaBSE)。

### 🐍 K-Means 文本聚类模板:

??? example "K-Means 文本聚类模板"

    ```python
    from sklearn.cluster import KMeans
    from sklearn.decomposition import PCA
    import matplotlib.pyplot as plt
    import seaborn as sns

    # 1. 训练
    kmeans = KMeans(n_clusters=4, random_state=42)
    clusters = kmeans.fit_predict(X_vec)

    # 2. 降维可视化 (PCA 2000维 → 2维)
    pca = PCA(n_components=2)
    coords = pca.fit_transform(X_vec.toarray())

    # 3. 画图
    plt.figure(figsize=(10, 6))
    sns.scatterplot(x=coords[:, 0], y=coords[:, 1], hue=clusters, palette='viridis')
    plt.title('K-Means Clustering Visualization')
    plt.show()
    ```
