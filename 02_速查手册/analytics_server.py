"""
知识库搜索分析 - 数据持久化 + AI 分析微服务
Flask 服务，接收搜索事件、持久化到 JSON、提供 AI 学习建议。

启动方式：python analytics_server.py
默认端口：5112
"""

import json
import os
import urllib.request
import urllib.error
from datetime import datetime, timedelta
from collections import Counter
from flask import Flask, request, jsonify
from flask_cors import CORS

# ========== 常量定义 ==========
DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data')
LOG_FILE = os.path.join(DATA_DIR, 'search_log.json')
SERVER_PORT = 5112
OLLAMA_API_URL = 'http://localhost:11434/api/generate'
DEFAULT_MODEL = 'deepseek-v3.1:671b-cloud'

# 知识库模块映射（页面名 → 模块信息）
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
    '11_clustering': '🎯 聚类分析',
    '12_time_series': '📈 时序预测',
    '13_business_analysis': '💰 业务分析',
    '14_nlp': '🗣️ NLP 文本分析',
}

# 常见函数 → 官方文档映射：(完整函数名, 文档URL, 用法摘要)
DOCS_MAP = {
    'groupby': ('pandas.DataFrame.groupby',
        'https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.groupby.html',
        '按列分组聚合。\ndf.groupby("col").agg({"val": ["mean", "sum"]})'),
    'merge': ('pandas.DataFrame.merge',
        'https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.merge.html',
        '合并 DataFrame（类似 SQL JOIN）。\npd.merge(df1, df2, on="key", how="left")'),
    'pivot_table': ('pandas.pivot_table',
        'https://pandas.pydata.org/docs/reference/api/pandas.pivot_table.html',
        '创建数据透视表。\ndf.pivot_table(values="sales", index="region", columns="year", aggfunc="sum")'),
    'drop_duplicates': ('pandas.DataFrame.drop_duplicates',
        'https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.drop_duplicates.html',
        '去除重复行。\ndf.drop_duplicates(subset=["uid"], keep="first")'),
    'duplicated': ('pandas.DataFrame.duplicated',
        'https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.duplicated.html',
        '标记重复行（返回布尔 Series）。\ndf[df.duplicated(subset=["uid"])]'),
    'fillna': ('pandas.DataFrame.fillna',
        'https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.fillna.html',
        '填充缺失值。\ndf["col"].fillna(df["col"].median(), inplace=True)'),
    'dropna': ('pandas.DataFrame.dropna',
        'https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.dropna.html',
        '删除含缺失值的行/列。\ndf.dropna(subset=["important_col"])'),
    'apply': ('pandas.DataFrame.apply',
        'https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.apply.html',
        '对行/列应用函数。\ndf["new"] = df["col"].apply(lambda x: x * 2)'),
    'value_counts': ('pandas.Series.value_counts',
        'https://pandas.pydata.org/docs/reference/api/pandas.Series.value_counts.html',
        '统计各值出现次数。\ndf["category"].value_counts(normalize=True)'),
    'melt': ('pandas.melt',
        'https://pandas.pydata.org/docs/reference/api/pandas.melt.html',
        '宽表转长表（unpivot）。\npd.melt(df, id_vars=["id"], value_vars=["col1","col2"])'),
    'concat': ('pandas.concat',
        'https://pandas.pydata.org/docs/reference/api/pandas.concat.html',
        '拼接多个 DataFrame。\npd.concat([df1, df2], axis=0, ignore_index=True)'),
    'sort_values': ('pandas.DataFrame.sort_values',
        'https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.sort_values.html',
        '按值排序。\ndf.sort_values("col", ascending=False)'),
    'reset_index': ('pandas.DataFrame.reset_index',
        'https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.reset_index.html',
        '重置索引为默认整数。\ndf.reset_index(drop=True)'),
    'loc': ('pandas.DataFrame.loc',
        'https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.loc.html',
        '按标签选择行/列。\ndf.loc[df["age"] > 30, ["name", "salary"]]'),
    'iloc': ('pandas.DataFrame.iloc',
        'https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.iloc.html',
        '按位置选择行/列。\ndf.iloc[0:5, [0, 2]]'),
    'astype': ('pandas.DataFrame.astype',
        'https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.astype.html',
        '类型转换。\ndf["id"] = df["id"].astype(str)'),
    'map': ('pandas.Series.map',
        'https://pandas.pydata.org/docs/reference/api/pandas.Series.map.html',
        '映射替换值。\ndf["level"] = df["score"].map({1: "低", 2: "中", 3: "高"})'),
    'cut': ('pandas.cut',
        'https://pandas.pydata.org/docs/reference/api/pandas.cut.html',
        '连续值分桶。\npd.cut(df["age"], bins=[0,18,35,60,100], labels=["少年","青年","中年","老年"])'),
    'qcut': ('pandas.qcut',
        'https://pandas.pydata.org/docs/reference/api/pandas.qcut.html',
        '等频分桶。\npd.qcut(df["salary"], q=4, labels=["Q1","Q2","Q3","Q4"])'),
    'reshape': ('numpy.ndarray.reshape',
        'https://numpy.org/doc/stable/reference/generated/numpy.ndarray.reshape.html',
        '改变数组形状。\narr.reshape(3, 4) 或 arr.reshape(-1, 1)'),
    'arange': ('numpy.arange',
        'https://numpy.org/doc/stable/reference/generated/numpy.arange.html',
        '创建等差数组。\nnp.arange(0, 10, 0.5)'),
    'train_test_split': ('sklearn.model_selection.train_test_split',
        'https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.train_test_split.html',
        '划分训练/测试集。\nX_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)'),
    'heatmap': ('seaborn.heatmap',
        'https://seaborn.pydata.org/generated/seaborn.heatmap.html',
        '热力图。\nsns.heatmap(corr_matrix, annot=True, cmap="coolwarm", fmt=".2f")'),
    'countplot': ('seaborn.countplot',
        'https://seaborn.pydata.org/generated/seaborn.countplot.html',
        '计数柱状图。\nsns.countplot(data=df, x="category", hue="target")'),
    'boxplot': ('seaborn.boxplot',
        'https://seaborn.pydata.org/generated/seaborn.boxplot.html',
        '箱线图。\nsns.boxplot(data=df, x="group", y="value")'),
    'describe': ('pandas.DataFrame.describe',
        'https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.describe.html',
        '描述性统计。\ndf.describe(include="all")'),
    'info': ('pandas.DataFrame.info',
        'https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.info.html',
        '查看 DataFrame 结构。\ndf.info()'),
    'crosstab': ('pandas.crosstab',
        'https://pandas.pydata.org/docs/reference/api/pandas.crosstab.html',
        '交叉表。\npd.crosstab(df["A"], df["B"], normalize="index")'),
}


# ========== Flask 应用 ==========
app = Flask(__name__)
CORS(app, origins=['http://127.0.0.1:8001', 'http://localhost:8001'])


def ensure_data_dir():
    """确保 data 目录存在"""
    os.makedirs(DATA_DIR, exist_ok=True)


def read_log():
    """读取日志文件"""
    ensure_data_dir()
    if not os.path.exists(LOG_FILE):
        return []
    try:
        with open(LOG_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        return []


def write_log(data):
    """写入日志文件"""
    ensure_data_dir()
    with open(LOG_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def filter_by_period(log, period):
    """按时间段过滤日志"""
    now = datetime.now()
    days = 1 if period == 'day' else 7
    cutoff = now - timedelta(days=days)
    filtered = []
    for entry in log:
        try:
            ts_str = entry.get('timestamp', '')
            ts = datetime.fromisoformat(ts_str.replace('Z', '+00:00')).replace(tzinfo=None)
            if ts >= cutoff:
                filtered.append(entry)
        except (ValueError, TypeError):
            continue
    return filtered


def match_docs(query):
    """匹配查询词到官方文档"""
    q = query.lower().strip()
    if q in DOCS_MAP:
        return DOCS_MAP[q]
    for key, info in DOCS_MAP.items():
        if key in q or q in key:
            return info
    return None


def call_ollama(prompt, model=DEFAULT_MODEL):
    """调用本地 Ollama API"""
    payload = json.dumps({
        'model': model,
        'prompt': prompt,
        'stream': False,
        'options': {'temperature': 0.7, 'num_predict': 1500}
    }).encode('utf-8')
    req = urllib.request.Request(
        OLLAMA_API_URL, data=payload,
        headers={'Content-Type': 'application/json'}
    )
    try:
        with urllib.request.urlopen(req, timeout=120) as resp:
            result = json.loads(resp.read().decode('utf-8'))
            return result.get('response', '')
    except Exception:
        return None


# ========== API 路由 ==========

@app.route('/api/log', methods=['POST'])
def log_event():
    """接收并持久化搜索/访问事件"""
    try:
        event = request.get_json()
        if not event or 'type' not in event:
            return jsonify({'error': '无效的事件数据'}), 400
        if 'timestamp' not in event:
            event['timestamp'] = datetime.now().isoformat()
        log = read_log()
        log.append(event)
        write_log(log)
        return jsonify({'status': 'ok', 'count': len(log)})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/data', methods=['GET'])
def get_data():
    """返回完整日志数据"""
    return jsonify(read_log())


@app.route('/api/summary', methods=['GET'])
def get_summary():
    """返回聚合统计"""
    period = request.args.get('period', 'day')
    log = read_log()
    filtered = filter_by_period(log, period)

    search_counts = {}
    page_counts = {}
    for entry in filtered:
        if entry.get('type') == 'search':
            q = entry.get('query', '')
            search_counts[q] = search_counts.get(q, 0) + 1
        elif entry.get('type') == 'visit':
            p = entry.get('page', '')
            page_counts[p] = page_counts.get(p, 0) + 1

    top_searches = sorted(search_counts.items(), key=lambda x: x[1], reverse=True)[:10]
    top_pages = sorted(page_counts.items(), key=lambda x: x[1], reverse=True)[:10]

    return jsonify({
        'period': period,
        'total_searches': sum(1 for e in filtered if e.get('type') == 'search'),
        'total_visits': sum(1 for e in filtered if e.get('type') == 'visit'),
        'top_searches': [{'query': q, 'count': c} for q, c in top_searches],
        'top_pages': [{'page': p, 'count': c} for p, c in top_pages],
    })


@app.route('/api/analyze', methods=['GET'])
def analyze():
    """AI 学习分析：官方文档用法 + 薄弱点 + 练习建议"""
    period = request.args.get('period', 'day')
    use_ai = request.args.get('ai', 'false').lower() == 'true'
    model = request.args.get('model', DEFAULT_MODEL)

    log = read_log()
    filtered = filter_by_period(log, period)

    # 统计
    searches = [e for e in filtered if e.get('type') == 'search']
    visits = [e for e in filtered if e.get('type') == 'visit']
    query_counts = Counter(e.get('query', '') for e in searches)
    page_counts = Counter(e.get('page', '') for e in visits)

    # 1. 高频函数 + 官方文档用法
    func_docs = []
    for query, count in query_counts.most_common(10):
        doc = match_docs(query)
        if doc:
            func_name, url, usage = doc
            func_docs.append({
                'query': query,
                'count': count,
                'func_name': func_name,
                'doc_url': url,
                'usage': usage,
            })
        else:
            func_docs.append({
                'query': query,
                'count': count,
                'func_name': None,
                'doc_url': None,
                'usage': None,
            })

    # 2. 薄弱模块定位
    module_scores = {}
    for page, count in page_counts.items():
        for key, name in MODULE_MAP.items():
            if key in page:
                module_scores[name] = module_scores.get(name, 0) + count
                break
    weak_modules = sorted(module_scores.items(), key=lambda x: x[1], reverse=True)[:5]

    # 3. 生成练习 prompt
    top_queries = [q for q, _ in query_counts.most_common(5)]
    top_module = weak_modules[0][0] if weak_modules else 'Python 数据分析'
    queries_text = '、'.join(top_queries) if top_queries else '常用函数'

    prompt_10 = (
        f'请给我生成 10 道 {top_module} 专项练习题，\n'
        f'重点覆盖以下函数/概念：{queries_text}，\n'
        f'要求：\n'
        f'1. 难度从基础到进阶递增\n'
        f'2. 每道题包含场景描述 + 参考答案 + 解题思路\n'
        f'3. 至少 3 道题使用真实业务场景（电商/用户分析/金融）'
    )
    prompt_50 = (
        f'请给我生成 50 道 {top_module} 强化练习题，\n'
        f'重点覆盖：{queries_text}，\n'
        f'要求：\n'
        f'1. 分为 5 个级别（入门/基础/中级/进阶/综合），每级 10 题\n'
        f'2. 每道题包含场景描述 + 参考答案 + 解题思路 + 常见错误提示\n'
        f'3. 综合级别需要组合使用多个函数\n'
        f'4. 使用真实业务数据集场景'
    )

    # 4. AI 分析（可选）
    ai_insight = None
    if use_ai and top_queries:
        queries_str = ', '.join(f'{q}({c}次)' for q, c in query_counts.most_common(10))
        ai_prompt = (
            f'你是资深数据科学导师。学生{"今日" if period == "day" else "本周"}查询记录：\n'
            f'{queries_str}\n\n'
            f'请用中文简短分析（3-5 句话）：\n'
            f'1. 查询模式特征\n'
            f'2. 薄弱点判断\n'
            f'3. 具体的下一步学习建议'
        )
        ai_insight = call_ollama(ai_prompt, model)

    return jsonify({
        'period': period,
        'total_searches': len(searches),
        'total_visits': len(visits),
        'func_docs': func_docs,
        'weak_modules': [{'module': m, 'score': s} for m, s in weak_modules],
        'exercise_prompt_10': prompt_10,
        'exercise_prompt_50': prompt_50,
        'ai_insight': ai_insight,
    })


@app.route('/api/clear', methods=['POST'])
def clear_data():
    """清空所有日志数据"""
    write_log([])
    return jsonify({'status': 'ok', 'message': '数据已清空'})


# ========== 思维导图 API ==========
MINDMAP_DIR = os.path.join(DATA_DIR, 'mindmaps')


@app.route('/api/mindmaps', methods=['GET'])
def list_mindmaps():
    """列出所有可用的思维导图"""
    os.makedirs(MINDMAP_DIR, exist_ok=True)
    maps = []
    for f in sorted(os.listdir(MINDMAP_DIR)):
        if f.endswith('.json'):
            name = f[:-5]  # 去掉 .json 后缀
            maps.append({'id': name, 'filename': f})
    return jsonify(maps)


@app.route('/api/mindmaps/<map_id>', methods=['GET'])
def get_mindmap(map_id):
    """加载指定思维导图的 JSON 数据"""
    filepath = os.path.join(MINDMAP_DIR, f'{map_id}.json')
    if not os.path.exists(filepath):
        return jsonify({'error': f'思维导图 {map_id} 不存在'}), 404
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return jsonify(data)
    except (json.JSONDecodeError, IOError) as e:
        return jsonify({'error': f'读取失败: {str(e)}'}), 500


@app.route('/api/mindmaps/<map_id>', methods=['PUT'])
def save_mindmap(map_id):
    """保存思维导图（新建或覆盖）"""
    os.makedirs(MINDMAP_DIR, exist_ok=True)
    filepath = os.path.join(MINDMAP_DIR, f'{map_id}.json')
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': '无效的 JSON 数据'}), 400
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        return jsonify({'status': 'ok', 'message': f'思维导图 {map_id} 已保存'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--port', type=int, default=SERVER_PORT)
    args = parser.parse_args()
    ensure_data_dir()
    print(f'📊 搜索分析服务启动: http://127.0.0.1:{args.port}')
    print(f'📁 数据文件: {LOG_FILE}')
    app.run(host='127.0.0.1', port=args.port, debug=False)
