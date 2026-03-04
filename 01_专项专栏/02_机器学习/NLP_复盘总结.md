# 🧠 NLP 核心复盘：从 "玄学" 到 "科学"
> *Learning is not about memorizing code, but understanding the flow.*

## 1. 核心世界观 (The Core Idea)
NLP 的本质就一件事：**把"人话" (Unstructured Text) 变成"数学" (Numerical Vectors)**，让机器能算。

## 2. 只有三步 (The Standard Workflow)
不管多么复杂的任务，其实都逃不过这三步：

### Step 1: 洗菜 (Preprocessing) 🥬
*   **动作**:去标点、去停用词、转小写、**分词 (Tokenization)**。
*   **工具**: `jieba` (中文), `re` (正则)。
*   **核心**: **垃圾进，垃圾出 (Garbage In, Garbage Out)**。如果不洗干净，"Refund!" 和 "refund..." 会被当成两个词。

### Step 2: 翻译 (Vectorization) 📐 **(最关键！)**
*   **把词变成向量**。这是机器理解语言的唯一桥梁。
*   **工具**: `TfidfVectorizer` (统计特征), `Word2Vec`/`BERT` (语义特征)。
*   **痛点 (我们遇到的坑)**:
    *   **TF-IDF 是个"脸盲"**：它只认单词拼写 (Spelling)。
    *   **Implication**: 英文的 "Money" 和 西班牙语的 "Dinero" 在它眼里毫无关系 (正交)。
    *   **Result**: 所以 K-Means 聚类时，**语言差异 > 意图差异**，导致聚出来的类全是按语言分的。

### Step 3: 算命 (Modeling) 🔮
根据有没有"标准答案" (Label)，选择不同的算法：

#### A. 有答案吗？(Supervised Learning)
*   **任务**: **分类 (Classification)**。
*   **例子**: 给评论打标签 (好评/差评/咨询)。
*   **算法**:
    *   **Naive Bayes**: 简单快，适合做 Baseline。
    *   **Logistic Regression**: 稳健，可解释 (知道哪个词权重高)。
    *   **XGBoost**: 精度之王 (**注意：必须把 String Label 转成 0/1/2 数字！**)。

#### B. 没答案吗？(Unsupervised Learning)
*   **任务**: **聚类 (Clustering)**。
*   **例子**: 这堆评论到底在聊啥？(Topic Discovery)。
*   **算法**:
    *   **K-Means**: 根据距离分堆 (适合圆球状分布)。
    *   **LDA**: 根据概率分主题 (Doc-Topic-Word)。
    *   **DBSCAN**: 根据密度找异常 (Anomaly Detection)。

## 3. 我们学到的 "血泪史" (Lessons Learned)
1.  **XGBoost 不认字**: 如果 Label 是 'refund'，它直接报错。必须用 `LabelEncoder` 把 'refund' 变成 `0`。
2.  **K-Means 也是 "文盲"**: 它是根据 TF-IDF 向量算距离的。如果多语言混在一起，它是分不出语义的。**这也是为什么我们最后那个测试 (只跑英语数据) 成功了！**
3.  **降维可视化 (PCA)**: 高维向量 (2000维) 人眼看不见，必须用 PCA 压扁成 2D 才能画图 (Scatter Plot)。

## 4. 下一步 (Next Steps)
不要纠结算法细节，记得 **Input (Text)** -> **Vector (TF-IDF)** -> **Output (Label/Cluster)** 这个流转链条即可。
当你下次遇到文本数据，脑子里只要有这三步，你就知道该怎么下手了。🚀
