<div align="center">

```
██████╗ ███████╗███████╗██╗   ██╗███╗   ███╗███████╗
██╔══██╗██╔════╝██╔════╝██║   ██║████╗ ████║██╔════╝
██████╔╝█████╗  ███████╗██║   ██║██╔████╔██║█████╗  
██╔══██╗██╔══╝  ╚════██║██║   ██║██║╚██╔╝██║██╔══╝  
██║  ██║███████╗███████║╚██████╔╝██║ ╚═╝ ██║███████╗
╚═╝  ╚═╝╚══════╝╚══════╝ ╚═════╝ ╚═╝     ╚═╝╚══════╝
██████╗  ██████╗  █████╗ ███████╗████████╗███████╗██████╗ 
██╔══██╗██╔═══██╗██╔══██╗██╔════╝╚══██╔══╝██╔════╝██╔══██╗
██████╔╝██║   ██║███████║███████╗   ██║   █████╗  ██████╔╝
██╔══██╗██║   ██║██╔══██║╚════██║   ██║   ██╔══╝  ██╔══██╗
██║  ██║╚██████╔╝██║  ██║███████║   ██║   ███████╗██║  ██║
╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═╝╚══════╝   ╚═╝   ╚══════╝╚═╝  ╚═╝
```



<br/>

[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)](https://streamlit.io)
[![NLP](https://img.shields.io/badge/NLP-TF--IDF%20%7C%20Cosine-blueviolet?style=for-the-badge)](https://scikit-learn.org)
[![ML](https://img.shields.io/badge/ML-Scoring%20Engine-orange?style=for-the-badge)](https://github.com)
[![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)](LICENSE)

<br/>

> **Resume Roaster** is a fully functional ATS (Applicant Tracking System) simulator that tears apart your resume, matches it against real job descriptions, finds the gaps, and tells you exactly why you're getting ghosted — before a recruiter does.

<br/>

[🚀 Demo](#-demo) · [📦 Installation](#-installation) · [🧠 How It Works](#-how-it-works) · [⚙️ Architecture](#%EF%B8%8F-system-architecture) · [📊 Features](#-features) · [🤝 Contributing](#-contributing)

</div>

---

## 🎯 The Problem

Every year, millions of qualified candidates get **rejected before a human ever sees their resume** — filtered out silently by ATS systems they don't understand.

Students and early-career professionals face a brutal reality:

- 📭 Applied to 100+ jobs, heard back from 3?
- 🤷 Don't know *why* you're getting rejected?
- 🧩 Not sure what keywords or skills are missing?
- 🕵️ Never seen the inside of an ATS before?

**Resume Roaster** changes that. It puts you on the other side of the system.

---

## 💡 What It Does

Resume Roaster simulates a real ATS pipeline end-to-end:

| Step | What Happens |
|------|-------------|
| 📄 **Parse** | Extracts structured data from your PDF resume |
| 🧹 **Clean** | Normalizes and preprocesses raw text |
| 🔢 **Score** | Runs a weighted ML-inspired scoring engine |
| 🧠 **Match** | Compares your resume to a job description using TF-IDF + Cosine Similarity |
| 🔍 **Gap Analysis** | Identifies matched vs. missing keywords |
| 🎯 **Decide** | Simulates a recruiter's shortlisting decision |
| 💬 **Feedback** | Gives actionable, human-readable suggestions |
| 📥 **Report** | Generates a downloadable analysis report |

---

## ⚙️ System Architecture

```
                        ┌─────────────────────┐
                        │     PDF Resume       │
                        └─────────┬───────────┘
                                  │
                        ┌─────────▼───────────┐
                        │   Parser Module      │  ← PyPDF2 + Regex + Section Detection
                        └─────────┬───────────┘
                                  │
                        ┌─────────▼───────────┐
                        │  Feature Engineering │  ← Projects, Skills, Experience, etc.
                        └─────────┬───────────┘
                                  │
               ┌──────────────────┼──────────────────┐
               │                  │                  │
    ┌──────────▼────────┐ ┌───────▼────────┐ ┌──────▼──────────┐
    │  ML Scoring Engine│ │ NLP JD Matcher  │ │ Keyword Gap     │
    │  (Weighted Score) │ │ (TF-IDF +       │ │ Analyzer        │
    │                   │ │  Cosine Sim)    │ │ (Set Ops)       │
    └──────────┬────────┘ └───────┬────────┘ └──────┬──────────┘
               │                  │                  │
               └──────────────────▼──────────────────┘
                                  │
                        ┌─────────▼───────────┐
                        │  Decision Engine     │  ← Shortlist: YES / MAYBE / NO
                        └─────────┬───────────┘
                                  │
                        ┌─────────▼───────────┐
                        │  Feedback + Report   │  ← Strengths, Gaps, Suggestions
                        └─────────┬───────────┘
                                  │
                        ┌─────────▼───────────┐
                        │   Streamlit UI       │  ← Interactive Web Interface
                        └─────────────────────┘
```

---

## 📊 Features

### 🧩 Core Modules

<details>
<summary><strong>📁 parser.py — Resume Parser</strong></summary>

- Extracts raw text from PDF using `PyPDF2`
- Cleans and normalizes text (lowercasing, punctuation, whitespace)
- Detects resume sections (Projects, Skills, Experience, Education, etc.)
- Extracts structured features via regex and keyword detection

**Extracted Feature Set:**
```python
{
  "projects":        [...],
  "skills":          [...],
  "links":           [...],
  "achievements":    [...],
  "experience":      [...],
  "certifications":  [...]
}
```
</details>

<details>
<summary><strong>📊 scorer.py — ML Scoring Engine</strong></summary>

Simulates ATS scoring with a weighted model that penalizes fake inflation.

| Feature | Weight |
|---------|--------|
| Projects | 30% |
| Experience | 25% |
| Skills | 20% |
| Achievements | 15% |
| Certifications/Links | 10% |

- Strict penalty system — no inflated scores
- Score normalization
- Capped final score to prevent false positives
</details>

<details>
<summary><strong>🧠 nlp_matcher.py — JD Matching</strong></summary>

Uses classical NLP to compare your resume against a job description:

```
TF-IDF Vectorization → Cosine Similarity → Match %
```

- Handles varied JD formats
- Language-agnostic keyword weighting
- Outputs similarity percentage (0–100%)
</details>

<details>
<summary><strong>🔍 gap_analyzer.py — Keyword Gap Analyzer</strong></summary>

```python
matched  = resume_keywords ∩ jd_keywords   # ✅ You have these
missing  = jd_keywords - resume_keywords   # ❌ You're missing these
```

Pinpoints exactly which skills/tools to add to pass the ATS filter.
</details>

<details>
<summary><strong>🎯 decision_engine.py — Recruiter Simulation</strong></summary>

```
Resume Score (60%) + JD Match (40%) → Shortlist Decision

Result:
  ✅ Shortlisted: YES     → Score ≥ 75 & Match ≥ 70
  ⚠️ Shortlisted: MAYBE  → Borderline signals
  ❌ Shortlisted: NO      → Below threshold
```
</details>

<details>
<summary><strong>🧠 skill_recommender.py — Skill Gap Recommender</strong></summary>

Maps missing keywords to actionable learning suggestions:

```
Missing: docker   →  "Learn Docker for containerized deployments"
Missing: aws      →  "Get AWS Cloud Practitioner certified"
Missing: sql      →  "Practice SQL on LeetCode / HackerRank"
```
</details>

<details>
<summary><strong>📊 visualizer.py — Visual Analytics</strong></summary>

Generates Matplotlib charts showing:
- Resume strength breakdown (bar chart by feature)
- ATS score vs. JD match comparison
- Keyword coverage heatmap
</details>

---

## 🖥️ UI Preview

```
┌─────────────────────────────────────────────────────┐
│  🔥 RESUME ROASTER                          v1.0     │
├─────────────────────────────────────────────────────┤
│  📄 Upload Resume (PDF)     🎯 Select Target Role    │
│  ┌─────────────────────┐    ┌─────────────────────┐  │
│  │  resume.pdf  ✅      │    │  Backend Engineer ▾ │  │
│  └─────────────────────┘    └─────────────────────┘  │
│                                                       │
│  📋 Paste Job Description                            │
│  ┌─────────────────────────────────────────────────┐ │
│  │  We are looking for a Python developer with...  │ │
│  └─────────────────────────────────────────────────┘ │
│                                                       │
│              [ 🔥 ROAST MY RESUME ]                  │
├─────────────────────────────────────────────────────┤
│  RESUME SCORE: ████████░░  78%                       │
│  JD MATCH:     ██████░░░░  65%                       │
│  DECISION:     ⚠️  MAYBE  (Confidence: 70%)           │
│                                                       │
│  ✅ python  ✅ backend   ❌ docker  ❌ aws            │
└─────────────────────────────────────────────────────┘
```

---

## 📦 Installation

### Prerequisites
- Python 3.10+
- pip

### Setup

```bash
# 1. Clone the repository
git clone https://github.com/yourusername/resume-roaster.git
cd resume-roaster

# 2. Create a virtual environment
python -m venv venv
source venv/bin/activate        # On Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run the app
streamlit run app.py
```

### Dependencies

```txt
streamlit
PyPDF2
scikit-learn
matplotlib
pandas
numpy
re
```

---

## 🚀 Demo

### Sample Output

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
        🔥 RESUME ROAST RESULTS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📊 RESUME SCORE     :  78 / 100
🎯 JD MATCH         :  65%
🤖 ATS DECISION     :  ⚠️  MAYBE
📈 CONFIDENCE       :  70%

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ MATCHED KEYWORDS
   ✔ python   ✔ backend   ✔ rest api

❌ MISSING KEYWORDS
   ✘ docker   ✘ aws   ✘ kubernetes

💡 SKILL SUGGESTIONS
   → Learn Docker for containerized apps
   → Get AWS Cloud Practitioner certified
   → Explore Kubernetes basics on KodeKloud

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
💬 FEEDBACK
   ✔ Strong project section
   ✔ Good use of technical keywords
   ⚠ Add internship / work experience
   ⚠ Include deployment-related skills
   💥 Power-up: Add a GitHub projects link
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## 🧠 Concepts Demonstrated

| Domain | Concepts |
|--------|----------|
| 🤖 **Machine Learning** | Feature engineering, weighted scoring, model-based thinking |
| 📚 **NLP** | TF-IDF vectorization, cosine similarity, keyword extraction |
| 🔍 **Information Retrieval** | Keyword matching, relevance scoring, document similarity |
| ⚙️ **Software Engineering** | Modular architecture, separation of concerns, reusable components |
| 📊 **Data Science** | Feature normalization, score distribution, visualization |
| 🧠 **System Design** | End-to-end pipeline design, ATS simulation, decision logic |

---

## 🗂️ Project Structure

```
resume-roaster/
│
├── app.py                  # Streamlit entry point
│
├── modules/
│   ├── parser.py           # PDF text extraction + feature engineering
│   ├── scorer.py           # Weighted ML scoring engine
│   ├── nlp_matcher.py      # TF-IDF + Cosine Similarity JD matcher
│   ├── gap_analyzer.py     # Keyword gap detection
│   ├── decision_engine.py  # Recruiter shortlist simulation
│   ├── skill_recommender.py# Skill gap → learning suggestions
│   ├── visualizer.py       # Matplotlib charts
│   ├── feedback_engine.py  # Human-readable feedback generator
│   └── report_generator.py # Downloadable report export
│
├── data/
│   └── skill_map.json      # Skill → suggestion mapping
│
├── assets/
│   └── sample_resume.pdf   # Test resume
│
├── requirements.txt
├── LICENSE
└── README.md
```

---

## ⚠️ Limitations & Future Work

### Current Limitations
- Rule-based feature extraction (no deep semantic parsing)
- Synthetic scoring model (not trained on real recruiter data)
- Basic keyword matching (no synonym/contextual awareness)
- No deep ML model training

### 🔭 Roadmap

- [ ] 🤗 BERT/Sentence-Transformers for semantic JD matching
- [ ] 🧠 Train on real recruiter feedback data
- [ ] 🌍 Multi-language resume support
- [ ] 📊 Dashboard analytics across multiple resumes
- [ ] 🔗 LinkedIn profile import
- [ ] 🧾 LaTeX resume generation from feedback

---

## 🤝 Contributing

Contributions are welcome! Here's how:

```bash
# Fork the repo, then:
git checkout -b feature/your-feature-name
git commit -m "feat: add your feature"
git push origin feature/your-feature-name
# Open a Pull Request 🎉
```

Please follow the [Contributor Guidelines](CONTRIBUTING.md) and ensure all new modules include docstrings and unit tests.

---

## 📄 License

This project is licensed under the MIT License — see [LICENSE](LICENSE) for details.

---

## 🙌 Acknowledgements

- [Streamlit](https://streamlit.io) — for the rapid UI layer
- [scikit-learn](https://scikit-learn.org) — TF-IDF and vectorization tools
- [PyPDF2](https://pypdf2.readthedocs.io) — PDF parsing
- [Matplotlib](https://matplotlib.org) — visualization

---

<div align="center">

**Built with 🔥 to help students stop getting ghosted.**

*If this helped you land an interview — drop a ⭐ on the repo.*

[![GitHub stars](https://img.shields.io/github/stars/adit-11/resume-analyzer?style=social)](https://github.com/adit-11/resume-analyzer)

</div>
