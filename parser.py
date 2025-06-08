import re
from collections import Counter
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
    raw_names = []

    for ent in doc.ents:
        if ent.label_ == "PERSON":
            # Clean name: strip whitespace and trailing punctuation
            cleaned_name = ent.text.strip()
            cleaned_name = re.sub(r'[^\w\s\-]', '', cleaned_name)  # Remove punctuation except hyphen
            # Filter out too short names (e.g., single characters or initials)
            if len(cleaned_name) < 3:
                continue
            # Prefer names with at least two words (e.g., first and last)
            if len(cleaned_name.split()) < 2:
                continue
            raw_names.append(cleaned_name)

    if not raw_names:
        return None

    # Count frequency ignoring case to find the most common name
    name_counter = Counter(name.lower() for name in raw_names)

    # Get the most common name (case-insensitive)
    most_common_name_lower, _ = name_counter.most_common(1)[0]

    # Return the original casing name that matches the most common lowercase version
    for name in raw_names:
        if name.lower() == most_common_name_lower:
            return name

    # Fallback: longest name if no frequency difference
    return max(raw_names, key=len)


def extract_skills(text, skill_list):
    text = text.lower()
    found = [skill for skill in skill_list if skill.lower() in text]
    return list(set(found))
