"""
知识库搜索分析 - AI 学习报告生成器
读取搜索日志 → 调用本地 Ollama → 生成 Markdown 学习报告。

功能：
1. 按天/周汇总高频查询，附带官方文档用法摘要 + 链接
2. 薄弱点定位，生成可复制的 Agent Chat 练习 prompt
3. 趋势洞察与学习建议

使用方式：
  python analyze.py --period day
  python analyze.py --period week --model qwen2.5:7b
"""

import json
import os
import sys
import argparse
from datetime import datetime, timedelta
from collections import Counter
import urllib.request
import urllib.error

# ========== 常量定义 ==========
DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data')
LOG_FILE = os.path.join(DATA_DIR, 'search_log.json')
REPORTS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'reports')

OLLAMA_API_URL = 'http://localhost:11434/api/generate'
DEFAULT_MODEL = 'deepseek-v3.1:671b-cloud'

# 知识库模块映射（页面名 → 模块名）
MODULE_MAP = {
    '01_python_basics': '🐍 Python 基础 & 心法',
    '02_numpy': '🔢 NumPy 数值计算',
    '03_pandas': '🐼 Pandas 数据分析',
    '04_visualization': '📊 可视化 Seaborn',
    '05_statistics': '📐 假设检验 & A/B Test',
    '06_feature_engineering': '🔧 特征工程 & Sklearn',
    '07_ml_models': '🤖 建模 (LGB/CatBoost)',
    '08_evaluation': '📏 评估指标 & 调优',
    '09_interpretation': '🕵️ SHAP 模型解释',
    '10_deployment': '📦 模型落地',
    '11_clustering': '🎯 聚类分析',
    '12_time_series': '📈 时序预测',
    '13_business_analysis': '💰 业务分析',
    '14_nlp': '🗣️ NLP 文本分析',
    '15_causal_inference': '🔬 因果推断',
    '16_data_engineering': '🏗️ 数据工程',
    '17_interview_prep': '🎤 面试准备',
}

# 常见函数 → 官方文档链接映射
# 格式：查询关键词 → (完整函数名, 文档URL, 简要用法说明)
DOCS_MAP = {
    # Pandas
    'groupby': (
        'pandas.DataFrame.groupby',
        'https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.groupby.html',
        '按列分组聚合。\n`df.groupby("col").agg({"val": ["mean", "sum"]})`'
    ),
    'merge': (
        'pandas.DataFrame.merge',
        'https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.merge.html',
        '合并两个 DataFrame（类似 SQL JOIN）。\n`pd.merge(df1, df2, on="key", how="left")`'
    ),
    'pivot_table': (
        'pandas.pivot_table',
        'https://pandas.pydata.org/docs/reference/api/pandas.pivot_table.html',
        '创建数据透视表。\n`df.pivot_table(values="sales", index="region", columns="year", aggfunc="sum")`'
    ),
    'drop_duplicates': (
        'pandas.DataFrame.drop_duplicates',
        'https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.drop_duplicates.html',
        '去除重复行。\n`df.drop_duplicates(subset=["uid"], keep="first")`'
    ),
    'duplicated': (
        'pandas.DataFrame.duplicated',
        'https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.duplicated.html',
        '返回布尔 Series 标记重复行。\n`df[df.duplicated(subset=["uid"])]`'
    ),
    'fillna': (
        'pandas.DataFrame.fillna',
        'https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.fillna.html',
        '填充缺失值。\n`df["col"].fillna(df["col"].median(), inplace=True)`'
    ),
    'dropna': (
        'pandas.DataFrame.dropna',
        'https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.dropna.html',
        '删除含缺失值的行/列。\n`df.dropna(subset=["important_col"])`'
    ),
    'apply': (
        'pandas.DataFrame.apply',
        'https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.apply.html',
        '对行/列应用函数。\n`df["new"] = df["col"].apply(lambda x: x * 2)`'
    ),
    'value_counts': (
        'pandas.Series.value_counts',
        'https://pandas.pydata.org/docs/reference/api/pandas.Series.value_counts.html',
        '统计各值出现次数。\n`df["category"].value_counts(normalize=True)`'
    ),
    'melt': (
        'pandas.melt',
        'https://pandas.pydata.org/docs/reference/api/pandas.melt.html',
        '宽表转长表（unpivot）。\n`pd.melt(df, id_vars=["id"], value_vars=["col1","col2"])`'
    ),
    'concat': (
        'pandas.concat',
        'https://pandas.pydata.org/docs/reference/api/pandas.concat.html',
        '拼接多个 DataFrame。\n`pd.concat([df1, df2], axis=0, ignore_index=True)`'
    ),
    'sort_values': (
        'pandas.DataFrame.sort_values',
        'https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.sort_values.html',
        '按值排序。\n`df.sort_values("col", ascending=False)`'
    ),
    'reset_index': (
        'pandas.DataFrame.reset_index',
        'https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.reset_index.html',
        '重置索引为默认整数。\n`df.reset_index(drop=True)`'
    ),
    'set_index': (
        'pandas.DataFrame.set_index',
        'https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.set_index.html',
        '设置某列为索引。\n`df.set_index("date", inplace=True)`'
    ),
    'loc': (
        'pandas.DataFrame.loc',
        'https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.loc.html',
        '按标签选择行/列。\n`df.loc[df["age"] > 30, ["name", "salary"]]`'
    ),
    'iloc': (
        'pandas.DataFrame.iloc',
        'https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.iloc.html',
        '按位置选择行/列。\n`df.iloc[0:5, [0, 2]]`'
    ),
    'astype': (
        'pandas.DataFrame.astype',
        'https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.astype.html',
        '类型转换。\n`df["id"] = df["id"].astype(str)`'
    ),
    'map': (
        'pandas.Series.map',
        'https://pandas.pydata.org/docs/reference/api/pandas.Series.map.html',
        '映射替换值。\n`df["level"] = df["score"].map({1: "低", 2: "中", 3: "高"})`'
    ),
    'cut': (
        'pandas.cut',
        'https://pandas.pydata.org/docs/reference/api/pandas.cut.html',
        '连续值分桶。\n`pd.cut(df["age"], bins=[0,18,35,60,100], labels=["少年","青年","中年","老年"])`'
    ),
    'qcut': (
        'pandas.qcut',
        'https://pandas.pydata.org/docs/reference/api/pandas.qcut.html',
        '等频分桶。\n`pd.qcut(df["salary"], q=4, labels=["Q1","Q2","Q3","Q4"])`'
    ),
    # NumPy
    'reshape': (
        'numpy.ndarray.reshape',
        'https://numpy.org/doc/stable/reference/generated/numpy.ndarray.reshape.html',
        '改变数组形状。\n`arr.reshape(3, 4)` 或 `arr.reshape(-1, 1)`'
    ),
    'arange': (
        'numpy.arange',
        'https://numpy.org/doc/stable/reference/generated/numpy.arange.html',
        '创建等差数组。\n`np.arange(0, 10, 0.5)`'
    ),
    'linspace': (
        'numpy.linspace',
        'https://numpy.org/doc/stable/reference/generated/numpy.linspace.html',
        '创建等间隔数组。\n`np.linspace(0, 1, 100)`'
    ),
    # Sklearn
    'train_test_split': (
        'sklearn.model_selection.train_test_split',
        'https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.train_test_split.html',
        '划分训练集和测试集。\n`X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)`'
    ),
    'cross_val_score': (
        'sklearn.model_selection.cross_val_score',
        'https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.cross_val_score.html',
        '交叉验证评估。\n`scores = cross_val_score(model, X, y, cv=5, scoring="accuracy")`'
    ),
    'standardscaler': (
        'sklearn.preprocessing.StandardScaler',
        'https://scikit-learn.org/stable/modules/generated/sklearn.preprocessing.StandardScaler.html',
        '标准化（Z-score）。\n`scaler = StandardScaler(); X_scaled = scaler.fit_transform(X)`'
    ),
    # Matplotlib / Seaborn
    'heatmap': (
        'seaborn.heatmap',
        'https://seaborn.pydata.org/generated/seaborn.heatmap.html',
        '热力图。\n`sns.heatmap(corr_matrix, annot=True, cmap="coolwarm", fmt=".2f")`'
    ),
    'countplot': (
        'seaborn.countplot',
        'https://seaborn.pydata.org/generated/seaborn.countplot.html',
        '计数柱状图。\n`sns.countplot(data=df, x="category", hue="target")`'
    ),
    'boxplot': (
        'seaborn.boxplot',
        'https://seaborn.pydata.org/generated/seaborn.boxplot.html',
        '箱线图。\n`sns.boxplot(data=df, x="group", y="value")`'
    ),
}


# ========== 工具函数 ==========

def read_log():
    """读取搜索日志"""
    if not os.path.exists(LOG_FILE):
        print('❌ 日志文件不存在，请先启动 analytics_server.py 并使用知识库搜索。')
        sys.exit(1)
    try:
        with open(LOG_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError) as e:
        print(f'❌ 读取日志失败: {e}')
        sys.exit(1)


def filter_by_period(log, period):
    """按时间段过滤日志"""
    now = datetime.now()
    days = 1 if period == 'day' else 7
    cutoff = now - timedelta(days=days)
    filtered = []
    for entry in log:
        try:
            ts_str = entry.get('timestamp', '')
            # 处理 ISO 格式时间戳
            ts = datetime.fromisoformat(ts_str.replace('Z', '+00:00')).replace(tzinfo=None)
            if ts >= cutoff:
                filtered.append(entry)
        except (ValueError, TypeError):
            continue
    return filtered


def get_search_stats(log):
    """计算搜索统计"""
    searches = [e for e in log if e.get('type') == 'search']
    visits = [e for e in log if e.get('type') == 'visit']

    query_counts = Counter(e.get('query', '') for e in searches)
    page_counts = Counter(e.get('page', '') for e in visits)

    return {
        'total_searches': len(searches),
        'total_visits': len(visits),
        'query_counts': query_counts.most_common(20),
        'page_counts': page_counts.most_common(10),
    }


def match_docs(query):
    """匹配查询词到官方文档，返回 (函数名, URL, 用法) 或 None"""
    q = query.lower().strip()
    # 精确匹配
    if q in DOCS_MAP:
        return DOCS_MAP[q]
    # 模糊匹配（查询词包含在键中，或键包含在查询词中）
    for key, info in DOCS_MAP.items():
        if key in q or q in key:
            return info
    return None


def identify_weak_modules(page_counts, query_counts):
    """根据页面访问和查询频次识别薄弱模块"""
    module_scores = {}
    # 根据页面访问频次
    for page, count in page_counts:
        for key, name in MODULE_MAP.items():
            if key in page:
                module_scores[name] = module_scores.get(name, 0) + count
                break
    return sorted(module_scores.items(), key=lambda x: x[1], reverse=True)


def call_ollama(prompt, model):
    """调用本地 Ollama API"""
    payload = json.dumps({
        'model': model,
        'prompt': prompt,
        'stream': False,
        'options': {
            'temperature': 0.7,
            'num_predict': 2000,
        }
    }).encode('utf-8')

    req = urllib.request.Request(
        OLLAMA_API_URL,
        data=payload,
        headers={'Content-Type': 'application/json'}
    )
    try:
        with urllib.request.urlopen(req, timeout=120) as resp:
            result = json.loads(resp.read().decode('utf-8'))
            return result.get('response', '')
    except urllib.error.URLError as e:
        print(f'⚠️ Ollama 调用失败: {e}')
        print('请确认 Ollama 已启动: ollama serve')
        return None
    except Exception as e:
        print(f'⚠️ Ollama 调用异常: {e}')
        return None


def generate_ai_analysis(stats, period, model):
    """调用 Ollama 生成 AI 分析"""
    period_name = '今日' if period == 'day' else '本周'
    queries_str = ', '.join(f'{q}({c}次)' for q, c in stats['query_counts'][:15])
    pages_str = ', '.join(f'{p}({c}次)' for p, c in stats['page_counts'][:10])

    prompt = f"""你是一位资深数据科学导师。请根据以下学生{period_name}的知识库查询记录，用中文给出学习分析和建议。

查询记录（函数/关键词及次数）：{queries_str}
页面访问（模块及次数）：{pages_str}
总搜索次数：{stats['total_searches']}
总页面访问：{stats['total_visits']}

请按以下格式输出：

1. 📊 查询模式总结（2-3 句话概括学习重点和特征）
2. 🎯 薄弱点分析（指出哪些模块反复查询说明不熟练，哪些函数需要重点强化）
3. 💡 学习建议（具体化的下一步行动，不超过 3 条）

注意：简洁、具体、可操作。不要空泛的建议。"""

    return call_ollama(prompt, model)


# ========== 报告生成 ==========

def generate_report(stats, period, model):
    """生成完整 Markdown 报告"""
    period_name = '每日' if period == 'day' else '每周'
    date_str = datetime.now().strftime('%Y-%m-%d')
    lines = []

    lines.append(f'# 📊 知识库学习分析报告 ({period_name})')
    lines.append(f'')
    lines.append(f'> 📅 生成时间: {datetime.now().strftime("%Y-%m-%d %H:%M")}')
    lines.append(f'> 🤖 分析模型: {model}')
    lines.append(f'')

    # ---- 概览 ----
    lines.append(f'## 📈 概览')
    lines.append(f'')
    lines.append(f'| 指标 | 数值 |')
    lines.append(f'|:--|:--|')
    lines.append(f'| 总搜索次数 | {stats["total_searches"]} |')
    lines.append(f'| 总页面访问 | {stats["total_visits"]} |')
    lines.append(f'| 不同查询词 | {len(stats["query_counts"])} |')
    lines.append(f'')

    # ---- 高频查询 + 官方文档 ----
    lines.append(f'## 🔥 高频查询函数')
    lines.append(f'')

    if stats['query_counts']:
        for query, count in stats['query_counts'][:10]:
            doc_info = match_docs(query)
            if doc_info:
                func_name, url, usage = doc_info
                lines.append(f'### `{func_name}` — 查询 {count} 次')
                lines.append(f'')
                lines.append(f'```python')
                lines.append(f'# {usage}')
                lines.append(f'```')
                lines.append(f'')
                lines.append(f'📖 <a href="{url}" target="_blank">查看官方文档 ↗</a>')
                lines.append(f'')
                lines.append(f'---')
                lines.append(f'')
            else:
                lines.append(f'- **`{query}`** — 查询 {count} 次')
                lines.append(f'')
    else:
        lines.append(f'暂无搜索记录。')
        lines.append(f'')

    # ---- 薄弱模块 ----
    weak_modules = identify_weak_modules(stats['page_counts'], stats['query_counts'])
    if weak_modules:
        lines.append(f'## 🎯 薄弱模块定位')
        lines.append(f'')
        lines.append(f'| 模块 | 查询/访问次数 | 建议 |')
        lines.append(f'|:--|:--|:--|')
        for module_name, score in weak_modules[:5]:
            lines.append(f'| {module_name} | {score} | 需要针对性强化练习 |')
        lines.append(f'')

        # 生成可复制的练习 prompt
        top_module = weak_modules[0][0] if weak_modules else ''
        top_queries = [q for q, _ in stats['query_counts'][:5]]
        queries_text = '、'.join(top_queries)

        lines.append(f'### 💪 专项练习 Prompt（复制到 Agent Chat）')
        lines.append(f'')
        lines.append(f'```text')
        lines.append(f'请给我生成 10 道 {top_module} 专项练习题，')
        lines.append(f'重点覆盖以下函数/概念：{queries_text}，')
        lines.append(f'要求：')
        lines.append(f'1. 难度从基础到进阶递增')
        lines.append(f'2. 每道题包含场景描述 + 参考答案 + 解题思路')
        lines.append(f'3. 至少 3 道题使用真实业务场景（电商/用户分析/金融）')
        lines.append(f'```')
        lines.append(f'')

        # 50 题版本
        lines.append(f'<details>')
        lines.append(f'<summary>📝 50 题强化版 Prompt（点击展开）</summary>')
        lines.append(f'')
        lines.append(f'```text')
        lines.append(f'请给我生成 50 道 {top_module} 强化练习题，')
        lines.append(f'重点覆盖：{queries_text}，')
        lines.append(f'要求：')
        lines.append(f'1. 分为 5 个级别（入门/基础/中级/进阶/综合），每级 10 题')
        lines.append(f'2. 每道题包含场景描述 + 参考答案 + 解题思路 + 常见错误提示')
        lines.append(f'3. 综合级别需要组合使用多个函数')
        lines.append(f'4. 使用真实业务数据集场景')
        lines.append(f'```')
        lines.append(f'')
        lines.append(f'</details>')
        lines.append(f'')

    # ---- AI 分析 ----
    lines.append(f'## 🤖 AI 学习分析')
    lines.append(f'')
    ai_analysis = generate_ai_analysis(stats, period, model)
    if ai_analysis:
        lines.append(ai_analysis)
    else:
        lines.append(f'⚠️ AI 分析生成失败，请确认 Ollama 已启动（`ollama serve`）。')
    lines.append(f'')

    # ---- 热门页面 ----
    if stats['page_counts']:
        lines.append(f'## 📄 热门页面')
        lines.append(f'')
        lines.append(f'| 页面 | 访问次数 |')
        lines.append(f'|:--|:--|')
        for page, count in stats['page_counts'][:10]:
            module_name = MODULE_MAP.get(page, page)
            lines.append(f'| {module_name} | {count} |')
        lines.append(f'')

    return '\n'.join(lines)


# ========== 主入口 ==========

def main():
    parser = argparse.ArgumentParser(description='知识库搜索分析报告生成器')
    parser.add_argument('--period', choices=['day', 'week'], default='day',
                        help='分析时间段：day=今日, week=本周')
    parser.add_argument('--model', default=DEFAULT_MODEL,
                        help=f'Ollama 模型名称（默认: {DEFAULT_MODEL}）')
    args = parser.parse_args()

    print(f'📊 知识库搜索分析')
    print(f'  时间段: {"今日" if args.period == "day" else "本周"}')
    print(f'  模型: {args.model}')
    print()

    # 读取并过滤日志
    log = read_log()
    filtered = filter_by_period(log, args.period)
    print(f'📝 找到 {len(filtered)} 条记录（总共 {len(log)} 条）')

    if not filtered:
        print('⚠️ 该时间段内没有搜索记录。请先使用知识库搜索。')
        sys.exit(0)

    # 计算统计
    stats = get_search_stats(filtered)

    # 生成报告
    print('🤖 正在生成 AI 分析...')
    report = generate_report(stats, args.period, args.model)

    # 保存报告
    os.makedirs(REPORTS_DIR, exist_ok=True)
    date_str = datetime.now().strftime('%Y-%m-%d')
    period_label = 'daily' if args.period == 'day' else 'weekly'
    report_file = os.path.join(REPORTS_DIR, f'{date_str}_{period_label}.md')
    with open(report_file, 'w', encoding='utf-8') as f:
        f.write(report)

    print(f'✅ 报告已生成: {report_file}')
    print()
    # 在终端也输出一份
    print('=' * 60)
    print(report)


if __name__ == '__main__':
    main()
