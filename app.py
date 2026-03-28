import streamlit as st
from modules.parser import extract_text_from_pdf, extract_text_from_jd
from modules.scorer import score_resume
from modules.ui_components import (
    load_css, render_header, render_score,
    render_keywords, render_stats
)

st.set_page_config(
    page_title="Resume Analyzer",
    page_icon="📄",
    layout="wide"
)

load_css("assets/style.css")
render_header()

col1, col2 = st.columns([1, 1], gap="large")

with col1:
    st.markdown("### 📋 Job Description")
    jd_input = st.text_area(
        label="Paste the job description here",
        height=300,
        placeholder="Paste the full job description here..."
    )

with col2:
    st.markdown("### 📄 Your Resume")
    uploaded_file = st.file_uploader(
        label="Upload your resume",
        type=["pdf"],
        help="Only PDF format supported"
    )

st.markdown("---")

if st.button("🔍 Analyze Resume", use_container_width=True):
    if not jd_input.strip():
        st.warning("Please paste a job description.")
    elif uploaded_file is None:
        st.warning("Please upload your resume PDF.")
    else:
        with st.spinner("Analyzing your resume..."):
            resume_text = extract_text_from_pdf(uploaded_file)
            jd_text = extract_text_from_jd(jd_input)
            result = score_resume(resume_text, jd_text)

        render_stats(result)
        st.markdown("<br>", unsafe_allow_html=True)

        col3, col4 = st.columns([1, 2])
        with col3:
            render_score(result["score"])
        with col4:
            render_keywords(result["matched"], result["missing"])