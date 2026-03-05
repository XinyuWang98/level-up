# 🎓 Level Up — AI Agent-Assisted Learning System (Real Case Study)

> **[中文](README.md) | [English](README_EN.md)**

A zero-cost learning methodology framework powered by **AI Agent + IDE**. This repository documents [你的姓名]'s real learning journey, demonstrating how to build an AI-assisted learning system covering the entire lifecycle: **Learn → Practice → Job Hunt**.

---

## ✨ What Makes This Different?

|                 | Traditional Courses     | Level Up                                                 |
| :-------------- | :---------------------- | :------------------------------------------------------- |
| **Deliverable** | Pre-packaged content    | **Methodology framework + reusable Agent configs**       |
| **AI Role**     | Q&A assistant (passive) | **Mentor (proactive challenges, progress tracking)**     |
| **Lifecycle**   | Ends with course        | **Learn → Practice → Job Hunt → Reuse after onboarding** |
| **Cost**        | $100s to $1000s         | **$0**                                                   |

---

## 🏗️ Eight-Module Architecture

```
1. Benchmark      → AI-powered skill assessment & Gap Analysis
2. Knowledge Base → AI-curated cheat sheets (MkDocs)
3. Hands-on Labs  → AI-generated graded practice Notebooks
4. Video Bridge   → AI-recommended learning videos
5. Interview Prep → AI-simulated multi-round technical interviews
6. Resume Builder → AI-customized resumes per job description
7. App Tracker    → AI-assisted application tracking
8. Knowledge Reuse → Continuously growing knowledge base post-hire
```

---

## 📂 Project Structure

```
level-up/
├── 00_教学课件/     → Agent-generated graded Notebooks + daily reviews
├── 01_专项专栏/     → Deep-dive practice by domain (A/B Testing, ML, Causal Inference)
├── 02_速查手册/     → MkDocs-powered knowledge base (43 cheat sheets)
├── 03_职业规划/     → Gap Analysis + Resume + Application Tracker (including cv folder)
├── 04_面试练习/     → AI mock interview summary reports
├── 05_笔试模拟/     → Agent-generated customized exam questions
├── 06_复盘与日志示例/ → De-sensitized daily reviews and learning logs
├── data/            → Practice datasets
└── .agent/          → Agent's "brain" (rules + workflows)
```

> Each directory contains a `README.md` with detailed usage instructions.

---

## 🚀 Core Workflows: The 8-Stage Interaction Lifecycle (Quick Start)

This system works with any IDE that supports AI Agent features (Cursor, Windsurf, VS Code + Copilot). After cloning the project, **follow these steps to interact with your AI Mentor using the built-in workflows**:

### Stage 1: Benchmark & Gap Analysis
- **Set Your Target**: Find a job description (JD) matching your dream role.
- **Trigger**: Run `/generate_gap_analysis` and provide the JD. The Agent will assess your current skills and generate an objective Gap Analysis matrix, saved in `03_职业规划/`.

### Stages 2 & 3: Hands-on Labs & Knowledge Base
- **Generate Practice**: Enter `/generate_notebook`. The Agent will ask for your Kaggle API token and dynamically download real-world business datasets matching your target role to generate practice questions.
- **Bridge Knowledge Gaps**: If stuck, trigger `/recommend_resources`. The Agent will actively search the web for high-quality, verified YouTube/Bilibili tutorial videos (with timestamps) without hallucinating links.
- **Consolidate Knowledge**: Type `/update_cheatsheet` to summarize newly learned concepts into `02_速查手册/` (your MkDocs knowledge base).
- **Daily Review**: Before finishing for the day, run `/daily_progress` and `/daily_review` to generate a de-sensitized learning log in `06_复盘与日志示例/`.

### Stages 4 & 5: Interview Prep & Resume Builder
- **Customized Mock Exams**: Type `/generate_exam`. The Agent will search for your target company's historical exam questions and create a complex, business-scenario mock exam (saved in `05_笔试模拟/`).
- **Stress-Test Mock Interviews**: Use `/mock_interview` with your resume and JD. Rather than chatting in text, the Agent will architect a strict Interviewer Persona Prompt meant for external Voice-Interactive AIs (like Doubao or ChatGPT Voice). After practicing verbally with the external AI, feed its feedback back to this Agent for a study plan (reports saved in `04_面试练习/`).
- **Tailor Resumes**: Use `/generate_resume` to quickly adapt your generic resume to highlight the specific skills demanded by different JDs.

### Stage 6: Application Tracker
- **Pipeline Management**: Use `/update_applications` to record interview rounds, technical questions asked, and feedback, enabling a systematic review of your job hunting funnel.

---

## 📜 License

MIT License

---

*Built with ❤️ and AI by [你的姓名]*
