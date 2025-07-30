from cv_parser import extract_cv_text
from jd_parser import extract_keywords_from_jd, extract_text_from_jd


def match_keywords(cv_text, jd_keywords):
    matched = []
    missing = []

    cv_text_lower = cv_text.lower()

    for keyword in jd_keywords:
        if keyword in cv_text_lower:
            matched.append(keyword)
        else:
            missing.append(keyword)

    return matched, missing
