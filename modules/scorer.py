import spacy
import re
from collections import Counter

nlp = spacy.load("en_core_web_sm")

TECH_KEYWORDS = {
    "python", "java", "javascript", "typescript", "c++", "c#", "sql", "nosql",
    "react", "node", "nodejs", "express", "fastapi", "flask", "django",
    "machine learning", "deep learning", "nlp", "computer vision",
    "pandas", "numpy", "scikit-learn", "tensorflow", "pytorch", "keras",
    "streamlit", "docker", "kubernetes", "aws", "gcp", "azure",
    "git", "github", "linux", "mongodb", "postgresql", "mysql",
    "rest", "api", "html", "css", "tailwind", "bootstrap",
    "data structures", "algorithms", "object oriented", "agile", "scrum"
}

def extract_keywords(text: str) -> set:
    text_lower = text.lower()
    found = set()

    # match multi-word tech terms first
    for keyword in TECH_KEYWORDS:
        if keyword in text_lower:
            found.add(keyword)

    # then use spacy for single important nouns and proper nouns
    doc = nlp(text_lower)
    for token in doc:
        if token.pos_ in ("NOUN", "PROPN") and not token.is_stop:
            if len(token.text) > 2:
                found.add(token.text)

    return found


def score_resume(resume_text: str, jd_text: str) -> dict:
    resume_keywords = extract_keywords(resume_text)
    jd_keywords = extract_keywords(jd_text)

    matched = resume_keywords & jd_keywords
    missing = jd_keywords - resume_keywords

    if len(jd_keywords) == 0:
        score = 0
    else:
        score = round((len(matched) / len(jd_keywords)) * 100, 1)

    # cap at 98 — nothing is perfect
    score = min(score, 98)

    return {
        "score": score,
        "matched": sorted(list(matched)),
        "missing": sorted(list(missing)),
        "total_jd_keywords": len(jd_keywords),
        "total_matched": len(matched),
    }