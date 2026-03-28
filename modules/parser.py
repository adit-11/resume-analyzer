import fitz
import re

def extract_text_from_pdf(uploaded_file) -> str:
    raw_bytes = uploaded_file.read()
    doc = fitz.open(stream=raw_bytes, filetype="pdf")
    text = ""
    for page in doc:
        text += page.get_text()
    return clean_text(text)

def clean_text(text: str) -> str:
    text = re.sub(r'\s+', ' ', text)
    text = re.sub(r'[^\x00-\x7F]+', ' ', text)
    return text.strip()

def extract_text_from_jd(raw_text: str) -> str:
    return clean_text(raw_text)