import os
import fitz  # for PDF
import spacy
import re
from spacy.lang.en.stop_words import STOP_WORDS

nlp = spacy.load("en_core_web_sm")

def extract_text_from_jd(file_path):
    ext = os.path.splitext(file_path)[1].lower()
    if ext == ".pdf":
        text = ""
        with fitz.open(file_path) as doc:
            for page in doc:
                text += page.get_text()
        return text
    elif ext == ".txt":
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()
    else:
        raise ValueError("Unsupported JD format. Use .txt or .pdf")

def extract_keywords_from_jd(jd_text):
    jd_text = jd_text.lower()
    jd_text = re.sub(r"[\/\n]", " ", jd_text)  # remove slashes and newlines
    jd_text = re.sub(r"[^a-z0-9\s]", "", jd_text)  # remove punctuation

    doc = nlp(jd_text)
    keywords = set()

    for token in doc:
        word = token.text.strip().lower()
        if (
            token.pos_ in ["NOUN", "PROPN"]
            and len(word) > 2
            and word not in STOP_WORDS
            and word.isalpha()
        ):
            keywords.add(word)

    # Manual cleanup of irrelevant or duplicate words
    junk_words = {
        "team", "position", "members", "division", "impact", "importance", "perspective",
        "names", "times", "activities", "customers", "industry", "solutions", "confidence"
    }

    keywords = {kw for kw in keywords if kw not in junk_words}

    return sorted(keywords)


def extract_job_title_from_jd(jd_text):
    # Look for 'About the Role:' or similar, then next non-empty line
    lines = jd_text.splitlines()
    for i, line in enumerate(lines):
        if re.search(r"about the role", line, re.IGNORECASE):
            # Look for next non-empty line
            for j in range(i+1, min(i+4, len(lines))):
                candidate = lines[j].strip()
                if candidate:
                    # Heuristic: job title often contains 'engineer', 'developer', 'manager', etc.
                    if re.search(r"engineer|developer|manager|lead|analyst|tester|designer|architect|specialist|consultant|administrator|officer|director|qa|devops", candidate, re.IGNORECASE):
                        return candidate
                    return candidate  # fallback
    # Fallback: look for first line with typical job title words
    for line in lines:
        if re.search(r"engineer|developer|manager|lead|analyst|tester|designer|architect|specialist|consultant|administrator|officer|director|qa|devops", line, re.IGNORECASE):
            return line.strip()
    return "Job Title"

def extract_company_from_jd(jd_text):
    # Look for 'About the job' or 'About [Company]' or first company-like name
    lines = jd_text.splitlines()
    for i, line in enumerate(lines):
        if re.search(r"about the job", line, re.IGNORECASE):
            # Look for next non-empty line
            for j in range(i+1, min(i+4, len(lines))):
                candidate = lines[j].strip()
                if candidate and len(candidate.split()) <= 10 and not candidate.lower().startswith("as a "):
                    # Heuristic: company name is often a short phrase, not a sentence
                    return candidate
    # Fallback: look for first capitalized word/phrase in first 10 lines
    for line in lines[:10]:
        candidate = line.strip()
        if candidate and candidate[0].isupper() and len(candidate.split()) <= 6:
            return candidate
    return "the company"
