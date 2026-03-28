import streamlit as st

def load_css(path: str):
    with open(path) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

def render_header():
    st.markdown("""
        <p class="main-title">Resume Analyzer</p>
        <p class="subtitle">Paste a job description, upload your resume — get your ATS match score instantly.</p>
    """, unsafe_allow_html=True)

def render_score(score: float):
    if score >= 70:
        emoji = "🟢"
        verdict = "Strong Match"
    elif score >= 45:
        emoji = "🟡"
        verdict = "Moderate Match"
    else:
        emoji = "🔴"
        verdict = "Needs Work"

    st.markdown(f"""
        <div class="score-box">
            <div class="score-number">{score}%</div>
            <div class="score-label">{emoji} {verdict}</div>
        </div>
    """, unsafe_allow_html=True)

def render_keywords(matched: list, missing: list):
    st.markdown("#### ✅ Keywords Found in Your Resume")
    if matched:
        pills = " ".join([f'<span class="pill-match">{k}</span>' for k in matched])
        st.markdown(f'<div>{pills}</div>', unsafe_allow_html=True)
    else:
        st.info("No matching keywords found.")

    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown("#### ❌ Missing Keywords — Add These to Your Resume")
    if missing:
        pills = " ".join([f'<span class="pill-missing">{k}</span>' for k in missing])
        st.markdown(f'<div>{pills}</div>', unsafe_allow_html=True)
    else:
        st.success("Your resume covers all keywords from this job description!")

def render_stats(result: dict):
    col1, col2, col3 = st.columns(3)
    col1.metric("ATS Score", f"{result['score']}%")
    col2.metric("Keywords Matched", result['total_matched'])
    col3.metric("Keywords in JD", result['total_jd_keywords'])