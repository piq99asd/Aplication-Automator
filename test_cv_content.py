from cv_parser import extract_cv_text
from summary_generator import generate_summary
from matcher import match_keywords
from jd_parser import extract_text_from_jd, extract_keywords_from_jd
from summary_replacer import replace_summary_section

# Extract original CV text
cv_text = extract_cv_text("samples/DINU_CV_ENGLISH.pdf")
print("=== ORIGINAL CV TEXT (first 1000 chars) ===")
print(cv_text[:1000])
print("\n" + "="*50 + "\n")

# Extract job description and keywords
jd_text = extract_text_from_jd("samples/job_description.txt")
jd_keywords = extract_keywords_from_jd(jd_text)

# Match skills
matched, missing = match_keywords(cv_text, jd_keywords)

# Generate tailored summary
summary = generate_summary(matched, missing)
print("=== GENERATED SUMMARY ===")
print(summary)
print("\n" + "="*50 + "\n")

# Replace summary in CV
updated_cv_text = replace_summary_section(cv_text, summary)
print("=== UPDATED CV TEXT (first 1000 chars) ===")
print(updated_cv_text[:1000])
print("\n" + "="*50 + "\n")

print("=== MATCHED SKILLS ===")
print("Matched:", matched)
print("\n=== MISSING SKILLS ===")
print("Missing:", missing) 