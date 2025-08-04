from cv_parser import extract_cv_text
from jd_parser import extract_keywords_from_jd, extract_text_from_jd


def match_keywords(cv_text, jd_keywords):
    matched = []
    missing = []

    cv_text_lower = cv_text.lower()

    for keyword in jd_keywords:
        if keyword in cv_text_lower:
            # Special handling for language skills
            if keyword in ['english', 'french', 'german', 'spanish', 'italian', 'portuguese', 'dutch', 'russian', 'chinese', 'japanese', 'korean', 'arabic']:
                # Check the proficiency level context around the language
                import re
                pattern = rf'.{{0,50}}{keyword}.{{0,50}}'
                match = re.search(pattern, cv_text_lower)
                if match:
                    context = match.group()
                    # Check for beginner/basic proficiency indicators
                    if any(level in context for level in ['a1', 'a2', 'basic', 'beginner', 'elementary']):
                        # Don't add basic level languages to matched - they go to missing
                        missing.append(keyword)
                    else:
                        matched.append(keyword)
                else:
                    matched.append(keyword)
            else:
                matched.append(keyword)
        else:
            missing.append(keyword)

    return matched, missing
