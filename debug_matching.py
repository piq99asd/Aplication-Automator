from jd_parser import extract_keywords_with_ai, extract_keywords_from_jd
from cv_parser import extract_cv_text
from matcher import match_keywords

# Your job description
jd_text = """
About the job
Company Description

Technology is our how. And people are our why. For over two decades, we have been harnessing technology to drive meaningful change.

By combining world-class engineering, industry expertise and a people-centric mindset, we consult and partner with leading brands from various industries to create dynamic platforms and intelligent digital experiences that drive innovation and transform businesses.

From prototype to real-world impact - be part of a global shift by doing work that matters.

Job Description

Your main responsibilities would be:

Actively participate in team meetings
Take part in all application development life cycle phases
Perform requirements analysis
Develop automation test cases scenarios
Execute functional tests and report the results
Ensure defects are clearly and concisely documented
Ensure the quality of testing deliverables
Defect reporting and tracking
Work closely with the Product Owner, Developers, and Testers to deliver the tasks in time and with the expected quality

Qualifications

We are looking to expand our team with open, thoughtful, and adaptable colleagues who have:

2+ years of experience working in Python
3+ years of experience in testing
Automation experience in both frontend and backend testing
Good knowledge of Selenium and/or Playwright is required
Experience in Web Services/API automated testing
Good knowledge of BDD - Cucumber/Python Behave
"""

# Extract keywords using AI
print("=== AI EXTRACTED KEYWORDS ===")
ai_keywords = extract_keywords_with_ai(jd_text)
print(ai_keywords)
print()

# Check if we have a CV file to test with
try:
    cv_text = extract_cv_text("samples/DINU_CV_ENGLISH.docx")  # Adjust path if needed
    print("=== CV TEXT SAMPLE (first 500 chars) ===")
    print(cv_text[:500] + "...")
    print()
    
    # Check matching
    matched, missing = match_keywords(cv_text, ai_keywords)
    print("=== MATCHING RESULTS ===")
    print(f"MATCHED ({len(matched)}): {matched}")
    print(f"MISSING ({len(missing)}): {missing}")
    print()
    
    # Check specifically for playwright
    playwright_in_cv = "playwright" in cv_text.lower()
    print(f"=== PLAYWRIGHT CHECK ===")
    print(f"'playwright' in CV text: {playwright_in_cv}")
    print(f"'playwright' in matched list: {'playwright' in matched}")
    print(f"'playwright' in missing list: {'playwright' in missing}")
    
except Exception as e:
    print(f"Could not load CV: {e}")
    print("Please update the CV path in this script")