import numpy as np
from sklearn.ensemble import RandomForestRegressor

# modules/scorer.py
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def train_model():
    """
    Train ML model on synthetic resume data
    """
    X = []
    y = []

    for p in range(0, 5):
        for s in range(0, 9):
            for e in range(0, 3):
                for a in range(0, 4):

                    score = (
                        p * 30 +
                        s * 10 +
                        e * 20 +
                        a * 10
                    ) / 2

                    score = max(10, min(100, score))

                    X.append([p, s, 1, a, e, 1])
                    y.append(score)

    model = RandomForestRegressor(n_estimators=200, random_state=42)
    model.fit(X, y)

    return model


MODEL = train_model()
def predict_resume_score(features):
    """
    STRICT ATS scoring (0–100)
    Only strong resumes get 85+
    """

    projects, skills, _, achievements, experience, _ = features

    # normalize
    p = min(projects / 4, 1)
    s = min(skills / 8, 1)
    e = min(experience / 2, 1)
    a = min(achievements / 3, 1)

    # base weighted score (lowered)
    score = (
        p * 30 +
        s * 20 +
        e * 25 +
        a * 15
    )

    # =========================
    # STRICT PENALTIES
    # =========================
    if projects < 2:
        score -= 20

    if experience == 0:
        score -= 15

    if skills < 4:
        score -= 15

    if achievements == 0:
        score -= 10

    # =========================
    # HARD CAPS (IMPORTANT 🔥)
    # =========================
    if projects < 2:
        score = min(score, 60)

    if experience == 0:
        score = min(score, 70)

    if skills < 3:
        score = min(score, 65)

    # =========================
    # FINAL CLAMP
    # =========================
    score = max(10, min(100, round(score)))

    return score

def generate_feedback(text, score, role=None):
    text = text.lower()

    strengths = []
    improve = []

    # projects
    project_count = text.count("project")
    if project_count >= 3:
        strengths.append("Excellent project depth with strong technical proof.")
    elif project_count >= 1:
        strengths.append("Projects section exists and adds credibility.")
    else:
        improve.append("Add 2–3 strong projects with measurable outcomes.")

    # experience
    if "intern" in text or "experience" in text:
        strengths.append("Experience section significantly boosts shortlist chances.")
    else:
        improve.append("Add internship, freelancing, or open-source proof.")

    # achievements
    if any(x in text for x in ["award", "winner", "rank", "dean"]):
        strengths.append("Achievements strongly differentiate your profile.")
    else:
        improve.append("Add coding ranks, Dean’s list, or hackathon wins.")

    # skills
    skill_hits = sum(
        1 for x in [
            "python", "java", "sql", "react",
            "node", "aws", "docker"
        ] if x in text
    )

    if skill_hits >= 5:
        strengths.append("Good technical skill diversity.")
    else:
        improve.append("Add stronger technical stack visibility.")

    quick_fixes = [
        "Use action verbs: Built, Automated, Optimized, Scaled.",
        "Add measurable metrics like 1K+ users or 95% accuracy.",
        "Move strongest project and internship to top.",
    ]

    power_ups = [
        f"Tailor keywords for {role}." if role else "Tailor resume for target role.",
        "Add one deployed live project.",
        "Show leadership or club responsibilities.",
    ]

    # recruiter verdict
    if score >= 90:
        verdict = "Elite shortlist-ready"
    elif score >= 80:
        verdict = "Excellent placement potential"
    elif score >= 65:
        verdict = "Strong resume with growth path"
    elif score >= 50:
        verdict = "Good base, needs polishing"
    else:
        verdict = "Needs stronger proof of work"

    return {
        "verdict": verdict,
        "impression": (
            "This score now focuses mainly on project depth, experience, "
            "skills, and achievements — just like real ATS shortlisting."
        ),
        "strengths": strengths[:4],
        "improve": improve[:4],
        "quick_fixes": quick_fixes,
        "power_ups": power_ups[:4],
        "motivation": (
            "Strong resumes win because of proof of work, not keyword stuffing."
        ),
    }

def jd_match_score(resume_text, jd_text):
    """
    Calculate similarity between resume and job description using TF-IDF
    """
    if not resume_text or not jd_text:
        return 0

    try:
        tfidf = TfidfVectorizer(stop_words='english')
        vectors = tfidf.fit_transform([resume_text, jd_text])

        score = cosine_similarity(vectors[0], vectors[1])[0][0]

        return round(score * 100)

    except:
        return 0


# =========================
# KEYWORD GAP ANALYZER (FIXED)
# =========================
def keyword_gap_analysis(resume_text, jd_text):
    """
    Find matched and missing keywords between resume and JD
    """

    if not resume_text or not jd_text:
        return [], []

    jd_words = set(jd_text.lower().split())
    resume_words = set(resume_text.lower().split())

    jd_keywords = set([w for w in jd_words if len(w) > 3])

    matched = jd_keywords.intersection(resume_words)
    missing = jd_keywords - resume_words

    return list(matched)[:15], list(missing)[:15]

def shortlist_decision(score, jd_score=None):
    """
    Simulate recruiter shortlist decision
    """

    # base decision
    if score >= 85:
        decision = "YES"
        confidence = score
    elif score >= 70:
        decision = "MAYBE"
        confidence = score - 10
    else:
        decision = "NO"
        confidence = score - 20

    # adjust with JD match
    if jd_score:
        if jd_score < 40:
            decision = "NO"
            confidence -= 10
        elif jd_score > 70:
            confidence += 5

    confidence = max(10, min(100, confidence))

    return decision, confidence

def skill_gap_suggestions(missing_keywords, role=None):
    """
    Suggest skills based on missing keywords
    """

    suggestions = []

    tech_map = {
        "python": "Learn Python for backend/ML roles",
        "docker": "Learn Docker for deployment",
        "aws": "Learn AWS cloud basics",
        "react": "Build frontend projects using React",
        "sql": "Practice SQL queries and DB design",
        "api": "Learn REST API development",
    }

    for word in missing_keywords:
        if word in tech_map:
            suggestions.append(tech_map[word])

    if role:
        suggestions.append(f"Focus on {role} core skills")

    return suggestions[:5]


def rewrite_bullet(line):
    """
    Improve weak resume bullet
    """

    line = line.strip()

    if not line:
        return ""

    verbs = {
        "made": "Developed",
        "created": "Engineered",
        "did": "Implemented",
        "worked on": "Contributed to",
        "built": "Designed and developed"
    }

    for k, v in verbs.items():
        if k in line.lower():
            return line.replace(k, v) + " with measurable impact"

    return "Optimized and enhanced: " + line