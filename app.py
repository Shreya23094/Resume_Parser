import streamlit as st
from parser import extract_email, extract_name, extract_phone, extract_skills
from utils import get_file_text
import json
import time

# Page config
st.set_page_config(
    page_title="Smart Resume Parser",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for polished look + simple animations
st.markdown("""
<style>
body, .stApp {
    background: #f5f7fa;
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    color: #323232;
}
main > div.block-container {
    max-width: 960px;
    padding-top: 2rem;
    padding-bottom: 4rem;
}
h1.title {
    font-weight: 700;
    font-size: 3rem;
    color: #2a3f5f;
    text-align: center;
    margin-bottom: 0.5rem;
    letter-spacing: 1.1px;
    user-select:none;
}
h3.section-title {
    font-weight: 600;
    color: #336699;
    margin-top: 2rem;
    margin-bottom: 1rem;
    border-bottom: 2px solid #336699;
    padding-bottom: 0.25rem;
    user-select:none;
}
.stFileUploader > div {
    border: 2px dashed #336699 !important;
    border-radius: 12px !important;
    padding: 2rem !important;
    background: #e6f0ff;
    transition: background-color 0.3s ease;
}
.stFileUploader:hover > div {
    background: #d0e2ff;
}
.info-card {
    background: #fff;
    padding: 1.5rem 2rem;
    border-radius: 14px;
    box-shadow: 0 5px 15px rgba(0,0,0,0.1);
    margin-bottom: 1.5rem;
    transition: transform 0.3s ease;
}
.info-card:hover {
    transform: translateY(-5px);
}
.label-icon {
    font-size: 1.3rem;
    margin-right: 0.6rem;
    color: #336699;
}
.badge-missing {
    background-color: #f44336;
    color: white;
    padding: 2px 8px;
    border-radius: 12px;
    font-size: 0.8rem;
    vertical-align: middle;
    margin-left: 6px;
}
.stButton > button {
    background: linear-gradient(90deg, #3a8dff, #0055cc);
    color: white;
    font-weight: 600;
    padding: 0.6rem 1.4rem;
    border-radius: 8px;
    border: none;
    transition: background 0.3s ease;
}
.stButton > button:hover {
    background: linear-gradient(90deg, #0055cc, #003d99);
}
.stSuccess {
    font-size: 1.1rem;
    font-weight: 600;
    margin-top: 1rem;
    color: #28a745 !important;
}
.stExpander > div:first-child {
    font-weight: 600;
    color: #0055cc;
}
.resume-snippet {
    font-family: 'Courier New', monospace;
    background: #e9f0ff;
    border-left: 4px solid #336699;
    padding: 0.75rem 1rem;
    margin-top: 1rem;
    white-space: pre-wrap;
    font-size: 0.9rem;
    color: #23395b;
    user-select:none;
}
@media (max-width: 768px) {
    h1.title {
        font-size: 2rem;
    }
    main > div.block-container {
        padding: 1rem;
    }
}
</style>
""", unsafe_allow_html=True)

# Sidebar for instructions + skill filters
st.sidebar.title("👩‍💼 HR Controls")
st.sidebar.markdown("""
**How to use:**

1. Upload a PDF or DOCX resume file.
2. Parsed candidate info will display instantly.
3. Download extracted data as JSON.
4. Use skill filter to highlight relevant skills.

---
""")

skill_options = ["Python", "Java", "SQL", "AWS", "Data Analysis", "C++", "Excel", "Machine Learning", "Docker", "Kubernetes"]
selected_skills = st.sidebar.multiselect("Select skills to highlight:", skill_options, default=skill_options[:5])

def highlight_skills(skills, highlight):
    if not skills:
        return "Not found"
    return ", ".join([f"**{s}**" if s in highlight else s for s in skills])

def main():
    st.markdown('<h1 class="title">📄 Smart Resume Parser</h1>', unsafe_allow_html=True)
    st.markdown("<p style='text-align:center; color:#555;'>Upload a resume (PDF/DOCX) to extract key information instantly.</p>", unsafe_allow_html=True)

    uploaded_file = st.file_uploader("Upload resume file", type=["pdf", "docx"], help="Supported formats: PDF, DOCX")

    if uploaded_file:
        # Progress bar simulation
        progress_text = "Extracting information from resume..."
        my_bar = st.progress(0, text=progress_text)
        for percent_complete in range(100):
            time.sleep(0.008)
            my_bar.progress(percent_complete + 1, text=progress_text)

        text = get_file_text(uploaded_file)
        name = extract_name(text)
        email = extract_email(text)
        phone = extract_phone(text)
        skills = extract_skills(text, skill_options)

        st.markdown('<h3 class="section-title">Candidate Information</h3>', unsafe_allow_html=True)

        cols = st.columns(2)
        with cols[0]:
            st.markdown(f"""
            <div class="info-card">
                <span class="label-icon">👤</span><strong>Name:</strong> {name if name else '<span class="badge-missing">Missing</span>'}
            </div>
            """, unsafe_allow_html=True)
            st.markdown(f"""
            <div class="info-card">
                <span class="label-icon">📧</span><strong>Email:</strong> {email if email else '<span class="badge-missing">Missing</span>'}
            </div>
            """, unsafe_allow_html=True)
        with cols[1]:
            st.markdown(f"""
            <div class="info-card">
                <span class="label-icon">📞</span><strong>Phone:</strong> {phone if phone else '<span class="badge-missing">Missing</span>'}
            </div>
            """, unsafe_allow_html=True)
            highlighted_skills = highlight_skills(skills, selected_skills)
            st.markdown(f"""
            <div class="info-card">
                <span class="label-icon">💼</span><strong>Skills:</strong> {highlighted_skills}
            </div>
            """, unsafe_allow_html=True)
        parsed_data = {
            "name": name,
            "email": email,
            "phone": phone,
            "skills": skills
        }

        with st.expander("📥 Download Parsed Data as JSON"):
            st.download_button(
                label="Download JSON",
                data=json.dumps(parsed_data, indent=4),
                file_name="resume_data.json",
                mime="application/json",
            )

        st.success("🎉 Resume parsed successfully! You can download the data above.")

    else:
        st.info("Please upload a resume file to get started.")

if __name__ == "__main__":
    main()
