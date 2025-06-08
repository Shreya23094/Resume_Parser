import docx2txt
import PyPDF2
from io import BytesIO

def get_file_text(uploaded_file):
    file_type = uploaded_file.name.split(".")[-1].lower()
    if file_type == "pdf":
        return read_pdf(uploaded_file)
    elif file_type == "docx":
        return docx2txt.process(uploaded_file)
    else:
        return ""

def read_pdf(file):
    pdf = PyPDF2.PdfReader(file)
    text = ""
    for page in pdf.pages:
        text += page.extract_text() or ""
    return text.strip()
