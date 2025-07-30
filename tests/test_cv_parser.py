from cv_parser import extract_cv_text

cv_path = "samples/DINU_CV_ENGLISH.pdf"
text = extract_cv_text(cv_path)
print(text[:3000])
