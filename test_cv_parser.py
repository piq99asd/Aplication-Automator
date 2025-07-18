# test_cv_parser.py
from cv_parser import extract_cv_text

cv_path = "samples/DINU_CV_ENGLISH.pdf"  # or my_cv.docx
text = extract_cv_text(cv_path)
print(text[:3000])  # Just show the first 1000 chars
