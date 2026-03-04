---
description: Update Senior Data Analyst Gap Analysis Progress
---

This workflow updates the `05_职业规划/Senior_DA_Gap_Analysis.md` document with your latest learning progress, identifying what gaps have been closed and what remains.

1.  **Read the Gap Analysis Document**:
    Check the current state of your skills assessment.
    // turbo
    Run command: `cat "./05_职业规划/Senior_DA_Gap_Analysis.md"`

2.  **Analyze Recent Progress** (Mental Step):
    Review what tasks or concepts you have recently completed (e.g., from `task.md` or recent conversation). Identify:
    *   **[+ New]**: New skills or concepts mastered.
    *   **[- Gap]**: Areas that still need work or were identified as weaknesses.

3.  **Update the Document**:
    Use `replace_file_content` or `write_to_file` (append mode logic) to add a new entry under `## 📝 历史进度追踪 (Progress Log)`.
    Format:
    ```markdown
    ### 📅 YYYY-MM-DD (Day X)
    *   **[+ New]** ...
    *   **[- Gap]** ...
    ```
    *Optionally update the "Current State" column in the table if a major milestone is reached.*

4.  **Notify User**:
    Inform the user that the Gap Analysis has been updated and summarize the key changes.
