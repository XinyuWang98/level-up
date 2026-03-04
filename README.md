# 🎓 Level Up — AI Agent 辅助学习系统（真实案例）

> **[中文](README.md) | [English](README_EN.md)**

一套基于 **AI Agent + IDE** 的零成本学习方法论框架。这个仓库是作者 XinyuWang 的真实学习历程，展示如何用 AI Agent 搭建覆盖 **学习 → 实战 → 求职** 全生命周期的辅助学习系统。

---

## ✨ 这个项目有什么不同？

|              | 传统在线课程         | Level Up                                        |
| :----------- | :------------------- | :---------------------------------------------- |
| **交付物**   | 别人沉淀好的知识内容 | **方法论框架 + 可复用的 Agent 配置**            |
| **AI 角色**  | 答疑助手（被动）     | **Mentor 导师（主动挑战、追踪进度、生成内容）** |
| **生命周期** | 课程结束即废弃       | **学习 → 实战 → 求职 → 入职后持续复用**         |
| **成本**     | 数千到数万           | **$0**                                          |

---

## 🏗️ 八大模块架构

```
1. Benchmark      → 用 AI 做能力体检，生成 Gap Analysis
2. Knowledge Base → 用 AI 沉淀知识到速查手册（MkDocs）
3. Hands-on Labs  → 用 AI 生成分级练习 Notebook
4. Video Bridge   → 用 AI 精准推荐学习视频
5. Interview Prep → 用 AI 模拟多轮技术面试
6. Resume Builder → 用 AI 根据 JD 定制简历
7. App Tracker    → 用 AI 追踪和优化投递
8. Knowledge Reuse → 入职后知识库持续增长
```

---

## 📂 项目结构

```
level-up/
├── 00_教学课件/     → Agent 生成的分级练习 Notebook + 每日复盘
├── 01_专项专栏/     → 按知识域分类的深度练习（AB测试/ML/因果推断）
├── 02_速查手册/     → MkDocs 驱动的知识库（43 篇速查文档）
├── 03_职业规划/     → Gap Analysis + 简历 + 投递追踪 (cv 模板在内)
├── 04_面试练习/     → AI 模拟面试的总结报告
├── 05_笔试模拟/     → Agent 生成的笔试题（Pandas/SQL/统计/AB）
├── data/            → 练习用数据集
└── .agent/          → Agent 的"大脑"（rules + workflows）
```

> 每个目录内的 `README.md` 都有详细的使用指引。

---

## 🚀 快速开始

### 第 1 步：配置你的 AI Agent

本系统适用于任何支持 Agent 功能的 IDE（如 Cursor、Windsurf、VS Code + Copilot、JetBrains AI 等）。

1. Fork 或下载本仓库
2. 在你的 IDE 中打开项目
3. 查看 `.agent/rules/learning.md` — 这是 Agent 的 Mentor 角色设定
4. 查看 `.agent/workflows/` — 这是标准化操作流程

### 第 2 步：做 Benchmark（能力体检）

1. 找到你的目标岗位 JD
2. 让 Agent 帮你做 Gap Analysis：

```
请根据以下 JD，分析我的当前技能和目标岗位的差距，生成 Gap Analysis 矩阵。
[粘贴 JD]
```

3. 产出会保存在 `03_职业规划/Gap_Analysis_Example.md`（参考示例）

### 第 3 步：开始学习

- 用 `/generate_notebook` 让 Agent 出题练习
- 用 `/update_cheatsheet` 把学到的知识沉淀到速查手册
- 用 `/daily_progress` 总结每日学习进度

---

## 🤖 使用的 AI 工具

| AI 工具      | 角色                            | 成本   |
| :----------- | :------------------------------ | :----- |
| DeepSeek     | 主力 Mentor（推理强、中文优秀） | 免费   |
| Gemini Flash | 大上下文分析（1M token）        | 免费层 |
| Grok         | 新知识获取                      | 免费   |

> **核心理念**: 框架不绑定任何特定 AI，你可以用任何你喜欢的模型。

---

## 📊 作者的学习成果

- ⏱️ **学习周期**: 约 4 周
- 📓 **产出 Notebook**: 84 个深度练习
- 📖 **知识库**: 43 篇速查文档，覆盖 Python/Pandas/统计学/ML/因果推断/NLP
- 🎯 **技能覆盖**: 从基础 Pandas 到高级因果推断（PSM/DID/RDD/IV）

---

## 📜 License

MIT License — 自由使用、修改、分发。

---

## 🙋 FAQ

**Q: 这个系统适合什么水平的人？**
A: 适合有一定编程基础、想系统提升数据分析/数据科学技能的人。完全零基础的建议先学完 Python 基础语法。

**Q: 必须用特定的 IDE 吗？**
A: 不必。任何支持 AI Agent 功能的 IDE 都可以。核心在于 `.agent/` 下的规则和工作流配置。

**Q: 我不是做数据分析的，这套系统对我有用吗？**
A: 有。方法论是通用的 — Benchmark → 学习 → 沉淀 → 实战 → 求职。你只需要修改 `.agent/rules/` 中的角色设定和目标即可。
