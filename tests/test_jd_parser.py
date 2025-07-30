from jd_parser import extract_text_from_jd, extract_keywords_from_jd

jd_path = "samples/job_description.txt"
jd_text = extract_text_from_jd(jd_path)
keywords = extract_keywords_from_jd(jd_text)

print("Extracted keywords:")
print(keywords)
