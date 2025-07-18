import os
from cv_parser import extract_cv_text
from summary_generator import generate_summary
from pdf_rewriter import preserve_original_formatting
from matcher import match_keywords
from jd_parser import extract_text_from_jd, extract_keywords_from_jd
import textwrap
from cv_editor import replace_summary_section_docx
from summary_replacer import replace_summary_section
import re

# 1. Load and parse
cv_text = extract_cv_text("samples/DINU_CV_ENGLISH.docx")
jd_text = extract_text_from_jd("samples/job_description.txt")
jd_keywords = extract_keywords_from_jd(jd_text)

# 2. Match skills
matched, missing = match_keywords(cv_text, jd_keywords)

# 3. Generate tailored summary
summary = generate_summary(matched, missing)

# 4. Replace in CV and generate new DOCX
cv_ext = os.path.splitext("samples/DINU_CV_ENGLISH.docx")[1].lower()
if cv_ext == ".pdf":
    updated_cv_text = replace_summary_section(cv_text, summary)
    preserve_original_formatting("samples/DINU_CV_ENGLISH.pdf", summary, "samples/updated_cv_formatted.pdf")
    print("✅ CV updated and saved as 'samples/updated_cv_formatted.pdf'")
elif cv_ext == ".docx":
    replace_summary_section_docx("samples/DINU_CV_ENGLISH.docx", summary, "samples/CV_DINU_ALEXANDRU_CRISTIAN_ENGLISH.docx")
    print("✅ CV updated and saved as 'samples/CV_DINU_ALEXANDRU_CRISTIAN_ENGLISH.docx'")
else:
    raise ValueError("Unsupported CV format. Use PDF or DOCX.")

print("Extracted CV text (first 3000 chars):")
print(cv_text[:3000])

if cv_ext == ".pdf":
    print("Updated CV text (first 3000 chars):")
    print(updated_cv_text[:3000])
elif cv_ext == ".docx":
    print("✅ CV updated successfully in DOCX format!")

