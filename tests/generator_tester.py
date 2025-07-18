from matcher import match_keywords
from cv_parser import extract_cv_text
from jd_parser import extract_text_from_jd, extract_keywords_from_jd
from summary_generator import generate_summary

cv_text = extract_cv_text("samples/DINU_CV_ENGLISH.pdf")
jd_text = extract_text_from_jd("samples/job_description.txt")
jd_keywords = extract_keywords_from_jd(jd_text)

matched, missing = match_keywords(cv_text, jd_keywords)

summary = generate_summary(matched, missing)
print(summary)
