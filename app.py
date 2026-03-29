import streamlit as st
import time

from modules.parser import extract_text_from_pdf, extract_features
from modules.scorer import (
    predict_resume_score,
    generate_feedback,
    jd_match_score,
    keyword_gap_analysis,
    shortlist_decision,
    skill_gap_suggestions
)
from modules.ui_components import (
    render_upload_screen,
    render_loading_screen,
    render_results_screen,
    render_jd_section
)

st.set_page_config(
    page_title="Resume Roaster — ML Feedback",
    page_icon="🔥",
    layout="centered",
)

# =========================
# SESSION STATE
# =========================
keys = [
    "stage", "selected_role", "result", "pdf_file",
    "resume_text", "jd_text", "jd_score",
    "matched_keywords", "missing_keywords",
    "shortlist", "confidence", "skill_suggestions"
]

for key in keys:
    if key not in st.session_state:
        st.session_state[key] = None if key != "stage" else "upload"

ROLES = [
    "💻 Software Engineer", "📊 Data Analyst", "🎨 Frontend Dev",
    "🤖 ML Intern", "📱 Product Manager", "📈 Business Analyst",
    "☁️ DevOps / Cloud", "🔐 Cybersecurity"
]

# =========================
# SCREEN 1 — UPLOAD
# =========================
if st.session_state.stage == "upload":

    uploaded, go_clicked = render_upload_screen(ROLES)

    jd_text = render_jd_section()
    st.session_state.jd_text = jd_text

    if uploaded:
        st.session_state.pdf_file = uploaded

    if go_clicked and uploaded:
        st.session_state.stage = "loading"
        st.rerun()

# =========================
# SCREEN 2 — LOADING
# =========================
elif st.session_state.stage == "loading":

    render_loading_screen()

    try:
        time.sleep(1)

        # Extract resume text
        text = extract_text_from_pdf(st.session_state.pdf_file)
        st.session_state.resume_text = text

        jd_score = None
        matched_keywords, missing_keywords = [], []

        if st.session_state.jd_text:
            jd_score = jd_match_score(text, st.session_state.jd_text)

            matched_keywords, missing_keywords = keyword_gap_analysis(
                text,
                st.session_state.jd_text
            )

        st.session_state.jd_score = jd_score
        st.session_state.matched_keywords = matched_keywords
        st.session_state.missing_keywords = missing_keywords

        # Score calculation
        features = extract_features(text)
        score = predict_resume_score(features)

        result = generate_feedback(
            text,
            score,
            st.session_state.selected_role
        )
        result["score"] = score

        # =========================
        # NEW FEATURES (IMPORTANT 🔥)
        # =========================

        # Shortlist decision
        decision, confidence = shortlist_decision(score, jd_score)

        # Skill suggestions
        skill_suggestions = skill_gap_suggestions(
            missing_keywords,
            st.session_state.selected_role
        )

        # Save to session
        st.session_state.shortlist = decision
        st.session_state.confidence = confidence
        st.session_state.skill_suggestions = skill_suggestions

        st.session_state.result = result
        st.session_state.stage = "results"
        st.rerun()

    except Exception as e:
        st.error(f"Error: {e}")
        if st.button("Retry"):
            st.session_state.stage = "upload"
            st.rerun()

# =========================
# SCREEN 3 — RESULTS
# =========================
elif st.session_state.stage == "results":

    restart = render_results_screen(
        st.session_state.result,
        st.session_state.selected_role,
        st.session_state.jd_score,
        st.session_state.matched_keywords,
        st.session_state.missing_keywords,
        st.session_state.shortlist,
        st.session_state.confidence,
        st.session_state.skill_suggestions
    )

    if restart:
        for key in keys:
            st.session_state[key] = None if key != "stage" else "upload"
        st.rerun()