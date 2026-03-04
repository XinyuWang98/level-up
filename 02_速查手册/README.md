# 📖 速查手册（MkDocs 知识库）

> 用 AI Agent 持续沉淀的知识库，学一个知识点就沉淀一个

## 📖 这个模块做什么？

这是一个基于 MkDocs 的本地知识库站点，包含 43 篇按主题分类的速查文档。每次学到新知识，用 Agent 的 `/update_cheatsheet` workflow 自动格式化并归档。

## 📂 核心文件

| 文件/目录    | 说明                        |
| :----------- | :-------------------------- |
| `docs/`      | 43 篇速查文档（按主题分类） |
| `mkdocs.yml` | 站点配置文件                |
| `start.sh`   | 一键启动脚本                |
| `data/`      | 思维导图等辅助数据          |

### 速查文档索引

| 编号 | 主题         | 文件                     |
| :--- | :----------- | :----------------------- |
| 01   | Python 基础  | `01_python_basics.md`    |
| 03   | Pandas       | `03_pandas.md`           |
| 05   | 统计学       | `05_statistics.md`       |
| 05a  | A/B 测试高阶 | `05a_ab_advanced.md`     |
| 05b  | A/B 测试基础 | `05b_ab_testing.md`      |
| 07   | ML 模型      | `07_ml_models.md`        |
| 12   | 时序预测     | `12_time_series.md`      |
| 14   | NLP          | `14_nlp.md`              |
| 15   | 因果推断     | `15_causal_inference.md` |
| 17   | 面试准备     | `17_interview_prep.md`   |
| ...  | ...          | 完整列表见 `mkdocs.yml`  |

## 🚀 如何使用？

### 启动本地知识库

```bash
# 安装依赖
pip install mkdocs mkdocs-material

# 启动服务
bash start.sh
# 或手动启动
mkdocs serve
```

访问 `http://localhost:8000` 即可浏览。

### 沉淀新知识

对 Agent 说：
```
/update_cheatsheet
我刚学了 CUPED 方差缩减方法，请帮我更新到速查手册。
```

Agent 会自动：
1. 找到对应的目标文件（`05a_ab_advanced.md`）
2. 格式化内容（表格、代码块、admonition）
3. 插入到正确的章节位置
4. 重启本地服务

## 💡 来自作者的经验

- **知识库的价值在面试前一刻爆发**：面试前 30 分钟速览自己的速查手册，比翻教科书有用 10 倍
- **写给未来的自己看**：每个知识点都要写得像"3 个月后忘了再看也能立刻回忆起来"
- **别怕重复**：同一个知识点从不同角度整理多次，理解会更深
