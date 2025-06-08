import re
import spacy

# Load English NLP model
nlp = spacy.load("en_core_web_sm")

def extract_email(text):
    emails = re.findall(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}", text)
    return emails[0] if emails else "Not found"

def extract_phone(text):
    phones = re.findall(r"\+?\d[\d\s\-]{8,}\d", text)
    return phones[0] if phones else "Not found"

def extract_name(text):
    doc = nlp(text)
    for ent in doc.ents:
        if ent.label_ == "PERSON":
            return ent.text
    return "Not found"

def extract_skills(text, skill_list):
    text = text.lower()
    found = [skill for skill in skill_list if skill.lower() in text]
    return list(set(found))
