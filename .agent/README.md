# 🧠 Agent 配置

> Agent 的"大脑"——定义 Mentor 角色设定和标准化工作流

## 📖 这个模块做什么？

这是整个学习系统的核心配置。通过 `rules/` 和 `workflows/` 两个子目录，定义了 AI Agent 如何扮演你的学习导师。

## 📂 文件说明

### `rules/learning.md` — Mentor 角色设定

定义了 Agent 的角色和行为准则：
- **角色**: 资深数据科学家 Mentor
- **交互模式**: Gap Driven（所有学习关联差距分析）+ Challenge Mode（主动挑战低级方案）
- **代码规范**: PEP 8、Type Hints、向量化思维
- **反馈纪律**: 客观诚恳，禁止安慰式反馈

### `workflows/` — 标准化工作流

| Workflow                   | 触发命令                 | 功能                  |
| :------------------------- | :----------------------- | :-------------------- |
| `generate_notebook.md`     | `/generate_notebook`     | 生成分级练习 Notebook |
| `generate_gap_analysis.md` | `/generate_gap_analysis` | 根据 JD 生成差距分析  |
| `recommend_resources.md`   | `/recommend_resources`   | 推荐视频教程与搜索词  |
| `generate_exam.md`         | `/generate_exam`         | 生成企业定制化笔试题  |
| `mock_interview.md`        | `/mock_interview`        | 生成外接语音面试模板  |
| `update_cheatsheet.md`     | `/update_cheatsheet`     | 更新 MkDocs 知识库    |
| `review_cheatsheet.md`     | `/review_cheatsheet`     | 审查知识库质量        |
| `daily_progress.md`        | `/daily_progress`        | 总结每日学习进度      |
| `daily_review.md`          | `/daily_review`          | 每日双视角客观复盘    |
| `generate_resume.md`       | `/generate_resume`       | 根据 JD 定制简历      |
| `update_applications.md`   | `/update_applications`   | 更新投递进度          |
| `update_senior_gap.md`     | `/update_gap`            | 更新 Gap Analysis     |
| `create_doc.md`            | `/create_doc`            | 创建/更新文档         |

## 🚀 如何自定义？

### 修改 Mentor 角色

编辑 `rules/learning.md`，修改以下字段：
- **User**: 你的角色（如"前端开发初学者"）
- **Agent**: Agent 扮演的角色（如"全栈工程师 Mentor"）
- **目标公司**: 你的目标（如"Google/Meta"）

### 添加新 Workflow

在 `workflows/` 下创建 `.md` 文件，格式：

```markdown
---
description: 一句话说明这个 workflow 做什么
---

## 步骤

1. 第一步...
2. 第二步...
```

## 💡 来自作者的经验

- **反馈纪律是关键**：如果 Agent 总是说"你做得很好"，你不会真正进步
- **Workflow 要越具体越好**：模糊的 workflow 产出质量不稳定
- **定期迭代 rules**：随着你的水平提升，Agent 的要求也应该提升
