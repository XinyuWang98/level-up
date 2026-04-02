# 🧠 Agent 配置 (Job Search Operating System)

> Agent 的"大脑"——定义 Mentor 角色设定和标准化工作流

## 📖 这个模块做什么？

这是整个学习系统的核心配置。通过 `rules/` 和 `workflows/` 两个子目录，定义了 AI Agent 如何扮演你的学习导师。

## 📂 文件说明

### `rules/learning.md` — 导师设定 (Mentor Persona)

定义了 Agent 的角色和核心行为准则：
- **角色定位**: 资深数据分析专家 + AI 开发者 Mentor
- **核心叙事**: 强调方法论迁移、因果推断深度及 AI 提效工具开发。
- **反馈纪律**: 严格执行 **Rule 0 (中文优先)**，拒绝过度夸大的 AI 虚词，保持专业且平等的对话口吻。
- **单一事实来源 (SSOT)**：所有求职状态追踪统一归口至 `02_速查手册/docs/Resume_Tracker.md`。

### `workflows/` — 标准化操作流 (Operating SOPs)

| Workflow                   | 触发命令                 | 功能                                      |
| :------------------------- | :----------------------- | :---------------------------------------- |
| `cold_start.md`            | `/cold_start`            | **[NEW]** 初始化用户背景、叙事映射与导师设定 |
| `create_doc.md`            | `/create_doc`            | 创建或更新文档，遵循 Rule 0 中文优先规则    |
| `daily_progress.md`        | `/daily_progress`        | 总结今日学习进度，整合搜索分析与 Gap 报告   |
| `daily_review.md`          | `/daily_review`          | 每日复盘工作流，从导师与学员两个维度对谈   |
| `generate_boss_greeting.md`| `/generate_boss_greeting`| 生成高转化率的 BOSS 直聘打招呼话术          |
| `generate_exam.md`         | `/generate_exam`         | 结合岗位 JD 个性化生成高频考点笔试题        |
| `generate_gap_analysis.md` | `/generate_gap_analysis` | 评估技能差距，生成标准化的分析矩阵          |
| `generate_notebook.md`     | `/generate_notebook`     | 生成特定学习模块的标准化 Jupyter Notebook    |
| `generate_resume.md`       | `/generate_resume`       | 根据岗位 JD 生成定制化简历 (含去客服化逻辑)   |
| `mock_interview.md`        | `/mock_interview`        | 输出结构化面试模拟框架和提示词              |
| `recommend_resources.md`   | `/recommend_resources`   | 推荐真实核验的学习视频或资源                |
| `review_cheatsheet.md`     | `/review_cheatsheet`     | 审查速查手册内容、Mermaid 及样式规范        |
| `update_applications.md`   | `/update_applications`   | 更新投递进度及其关联的所有列表与 Tracker    |
| `update_cheatsheet.md`     | `/update_cheatsheet`     | 使用新知识点或案例更新 MkDocs 知识库        |
| `update_senior_gap.md`     | `/update_gap`            | 动态更新资深数分能力 Gap 分析进度           |

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
