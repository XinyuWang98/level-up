---
description: 更新高级数据分析师差距分析进度 (Update Senior Data Analyst Gap Analysis Progress)
---

# /update_senior_gap 工作流

此工作流用于根据你最新的学习进度更新 `03_职业规划/[你的名字]_Gap_Analysis.md` 文档（如果是使用本仓库示例，即 `03_职业规划/Gap_Analysis_Example.md`），明确哪些差距已被弥补，哪些仍然存在。

## 1. 读取差距分析文档 (Read the Gap Analysis Document)
检查你当前的技能评估状态。
// turbo
Run command: `cat "./03_职业规划/Gap_Analysis_Example.md"`
*(注：请将上述文件名替换为你实际使用的 Gap Analysis 文件名)*

## 2. 分析近期进度 (Analyze Recent Progress)
回顾你近期完成的任务或掌握的概念（例如：参考 `task.md` 或近期的对话记录）。请明确指出以下两点：
*   **[+ New]**: 新掌握的技能或概念。
*   **[- Gap]**: 仍然需要努力或被识别为薄弱环节的领域。

## 3. 更新文档 (Update the Document)
使用 `replace_file_content` 或 `write_to_file` 在 `## 📝 历史进度追踪 (Progress Log)` 标题下添加一条新记录。
格式如下：
```markdown
### 📅 YYYY-MM-DD (Day X)
*   **[+ New]** ...
*   **[- Gap]** ...
```
*（如果达成了某个重要里程碑，可选择性地同步更新分析矩阵表格中的“你的当前现状”列）*

## 4. 通知用户 (Notify User)
通知用户差距分析文档已更新，并简要总结关键变化。
