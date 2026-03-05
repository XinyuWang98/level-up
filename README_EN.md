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
├── 05_职业规划/     → Gap Analysis + Resume + Application Tracker
├── 06_面试练习/     → AI mock interview summary reports
├── 05_笔试模拟/     → Agent-generated exam questions (Pandas/SQL/Stats/A/B)
├── cv/              → Resume storage (with mock example)
├── data/            → Practice datasets
└── .agent/          → Agent's "brain" (rules + workflows)
```

> Each directory contains a `README.md` with detailed usage instructions.

---

## 🚀 Quick Start

### Step 1: Configure Your AI Agent

This system works with any IDE that supports AI Agent features (Cursor, Windsurf, VS Code + Copilot, JetBrains AI, etc.).

1. Fork or download this repository
2. Open the project in your IDE
3. Review `.agent/rules/learning.md` — the Agent's Mentor persona
4. Review `.agent/workflows/` — standardized operation procedures

### Step 2: Run Benchmark (Skill Assessment)

1. Find your target job description
2. Ask the Agent to generate a Gap Analysis:

```
Based on the following JD, analyze my current skills vs. the target role
and generate a Gap Analysis matrix.
[Paste JD here]
```

3. Output will be saved in `03_职业规划/Gap_Analysis_Example.md` (see example)

### Step 3: Start Learning

- Use `/generate_notebook` to have Agent create practice exercises
- Use `/update_cheatsheet` to consolidate knowledge into cheat sheets
- Use `/daily_progress` to summarize daily learning progress

---

## 📜 License

MIT License

---

*Built with ❤️ and AI by [你的姓名]*
