# Smart Resume Parser

A simple NLP-based resume parser and visualizer built with Python and Streamlit.

## 🔍 Features
- Upload resumes in PDF or DOCX format
- Extract:
  - Name
  - Email
  - Phone number
  - Skills
- Download extracted data as JSON

## ⚙️ Setup Instructions

### 1. Install Dependencies
```bash
pip install -r requirements.txt
python -m spacy download en_core_web_sm
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
.\venv\Scripts\Activate.ps1
streamlit run app.py

