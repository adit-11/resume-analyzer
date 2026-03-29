# modules/parser.py

import PyPDF2
import re


# =========================
# PDF TEXT EXTRACTION
# =========================
def extract_text_from_pdf(uploaded_file):
    """
    Extract text safely from PDF
    Handles corrupted files, empty pages, etc.
    """
    if uploaded_file is None:
        return ""

    try:
        pdf_reader = PyPDF2.PdfReader(uploaded_file)
        text = ""

        for page in pdf_reader.pages:
            try:
                extracted = page.extract_text()
                if extracted:
                    text += extracted + "\n"
            except:
                continue

        return text.lower().strip()

    except Exception:
        return ""


# =========================
# TEXT CLEANING
# =========================
def clean_text(text):
    """
    Normalize text for NLP processing
    """
    text = text.lower()

    # remove special characters
    text = re.sub(r"[^a-z0-9\s]", " ", text)

    # remove extra spaces
    text = re.sub(r"\s+", " ", text)

    return text.strip()


# =========================
# SECTION DETECTION
# =========================
def detect_sections(text):
    """
    Detect major resume sections
    """
    sections = {
        "projects": ["project", "projects"],
        "experience": ["experience", "intern", "work"],
        "skills": ["skills", "technical skills"],
        "education": ["education", "degree"],
        "achievements": ["achievement", "award", "honor"],
        "certifications": ["certificate", "certification"]
    }

    detected = {}

    for section, keywords in sections.items():
        detected[section] = any(k in text for k in keywords)

    return detected


# =========================
# SKILL EXTRACTION
# =========================
def extract_skills(text):
    """
    Extract unique technical skills
    """

    skill_keywords = [
        # languages
        "python", "java", "c++", "c", "javascript",

        # web
        "html", "css", "react", "node", "express",

        # data
        "sql", "pandas", "numpy", "tensorflow", "pytorch",

        # cloud/devops
        "aws", "docker", "kubernetes",

        # tools
        "git", "github", "linux"
    ]

    found_skills = set()

    for skill in skill_keywords:
        if skill in text:
            found_skills.add(skill)

    return list(found_skills)


# =========================
# PROJECT DETECTION
# =========================
def count_projects(text):
    """
    Detect number of projects using multiple signals
    """
    keywords = ["project", "developed", "built", "implemented"]

    count = 0
    for k in keywords:
        count += text.count(k)

    return min(4, count)


# =========================
# EXPERIENCE DETECTION
# =========================
def count_experience(text):
    """
    Detect internship / experience
    """
    keywords = ["intern", "experience", "developer", "worked"]

    count = 0
    for k in keywords:
        if k in text:
            count += 1

    return min(2, count)


# =========================
# ACHIEVEMENTS DETECTION
# =========================
def count_achievements(text):
    keywords = ["award", "winner", "rank", "dean", "scholarship"]

    count = 0
    for k in keywords:
        if k in text:
            count += 1

    return min(3, count)


# =========================
# CERTIFICATION DETECTION
# =========================
def count_certifications(text):
    keywords = ["certificate", "certification", "coursera", "udemy", "nptel"]

    count = 0
    for k in keywords:
        if k in text:
            count += 1

    return min(2, count)


# =========================
# LINK DETECTION
# =========================
def detect_links(text):
    if "github" in text or "linkedin" in text:
        return 1
    return 0


# =========================
# MAIN FEATURE ENGINEERING
# =========================
def extract_features(text):
    """
    Convert resume → structured ATS features
    Output:
    [projects, skills, links, achievements, experience, certifications]
    """

    if not text:
        return [0, 0, 0, 0, 0, 0]

    text = clean_text(text)

    # detect sections
    sections = detect_sections(text)

    # extract features
    skills_list = extract_skills(text)
    skills = min(8, len(skills_list))

    projects = count_projects(text)
    experience = count_experience(text)
    achievements = count_achievements(text)
    certifications = count_certifications(text)
    links = detect_links(text)

    return [
        projects,
        skills,
        links,
        achievements,
        experience,
        certifications
    ]


# =========================
# DEBUG HELPER (OPTIONAL)
# =========================
def debug_features(text):
    """
    Print detailed feature extraction (for testing)
    """
    features = extract_features(text)
    labels = [
        "Projects", "Skills", "Links",
        "Achievements", "Experience", "Certifications"
    ]

    return dict(zip(labels, features))