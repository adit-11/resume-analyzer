import streamlit as st
import matplotlib.pyplot as plt


# =========================
# JD INPUT
# =========================
def render_jd_section():
    st.markdown("### 📄 Paste Job Description (Optional)")
    
    jd = st.text_area(
        "Paste job description here",
        placeholder="Paste internship/job description to check match..."
    )
    
    return jd


# =========================
# UPLOAD SCREEN
# =========================
def render_upload_screen(roles):
    st.markdown(
        '''
        <div style="text-align:center;padding:1rem 0 2rem 0;">
            <h1 style="font-size:3rem;margin-bottom:0.2rem;">🔥 Resume Roaster</h1>
            <p style="font-size:1.1rem;color:#A1A1AA;">
                Upload your PDF and get <b>ML-powered placement feedback</b> in seconds.
            </p>
        </div>
        ''',
        unsafe_allow_html=True,
    )

    c1, c2, c3 = st.columns(3)
    c1.metric("⚡ Speed", "3 sec")
    c2.metric("🎯 Accuracy", "ML Based")
    c3.metric("💼 Use Case", "Placements")

    uploaded = st.file_uploader("Drop your PDF here", type=["pdf"])

    selected_role = st.selectbox("Choose target role", ["None"] + roles)
    if selected_role != "None":
        st.session_state.selected_role = selected_role

    go_clicked = st.button("🔥 Roast My Resume", use_container_width=True)

    return uploaded, go_clicked


# =========================
# LOADING SCREEN
# =========================
def render_loading_screen():
    st.markdown("## ⏳ Analyzing Resume...")

    progress = st.progress(0)
    steps = [
        "📄 Reading PDF",
        "🧠 Extracting features",
        "📊 Scoring",
        "🎯 Building ATS insights",
        "🚀 Final polish"
    ]

    for i, step in enumerate(steps):
        st.write(step)
        progress.progress((i + 1) * 20)


# =========================
# RESULTS SCREEN
# =========================
def render_results_screen(
    result,
    role=None,
    jd_score=None,
    matched=None,
    missing=None,
    shortlist=None,
    confidence=None,
    skills=None
):

    score = result["score"]

    # =========================
    # HEADER
    # =========================
    st.markdown(f"## 📊 Resume Score: {score}%")
    st.progress(score)
    st.write(result["verdict"])

    # =========================
    # RECRUITER DECISION
    # =========================
    if shortlist:
        st.markdown("## 🎯 Recruiter Decision")
        st.success(f"Shortlisted: {shortlist}")
        st.info(f"Confidence: {confidence}%")

    # =========================
    # CHART
    # =========================
    st.markdown("## 📊 Resume Analysis Chart")

    labels = ["Projects", "Skills", "Experience", "Achievements"]
    values = [
        max(0, score),
        max(0, score - 10),
        max(0, score - 15),
        max(0, score - 20),
    ]

    fig, ax = plt.subplots()
    ax.bar(labels, values)
    st.pyplot(fig)

    # =========================
    # JD MATCH
    # =========================
    if jd_score is not None:
        st.markdown(f"### 🎯 JD Match Score: {jd_score}%")
        st.progress(jd_score)

    # =========================
    # KEYWORD ANALYSIS
    # =========================
    if matched or missing:
        st.markdown("## 🧠 Keyword Analysis")

        col1, col2 = st.columns(2)

        with col1:
            st.markdown("### ✅ Matched")
            for word in matched:
                st.success(word)

        with col2:
            st.markdown("### ❌ Missing")
            for word in missing:
                st.error(word)

    # =========================
    # SKILL GAP
    # =========================
    if skills:
        st.markdown("## 🎯 Skill Gap Suggestions")
        for s in skills:
            st.warning(s)

    # =========================
    # FEEDBACK
    # =========================
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### ✅ Strengths")
        for item in result["strengths"]:
            st.success(item)

        st.markdown("### ⚠️ Improve")
        for item in result["improve"]:
            st.warning(item)

    with col2:
        st.markdown("### ⚡ Quick Fixes")
        for item in result["quick_fixes"]:
            st.info(item)

        st.markdown("### 🚀 Power Ups")
        for item in result["power_ups"]:
            st.write(f"⭐ {item}")

    st.markdown(f"> 💬 **{result['motivation']}**")

    # =========================
    # DOWNLOAD REPORT
    # =========================
    report = f"Resume Score: {score}%\n"
    report += f"Verdict: {result['verdict']}\n\n"
    report += "Strengths:\n- " + "\n- ".join(result["strengths"]) + "\n\n"
    report += "Improvements:\n- " + "\n- ".join(result["improve"]) + "\n\n"

    st.download_button(
        "📥 Download Report",
        data=report,
        file_name="resume_report.txt"
    )

    return st.button("↩ Analyze Another Resume")