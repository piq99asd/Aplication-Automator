from jd_parser import extract_keywords_with_ai
from cv_parser import extract_cv_text
from matcher import match_keywords
from summary_generator import generate_summary

# Your problematic job description
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

print("=== TESTING IMPROVED PROMPT ===")

# Extract keywords
ai_keywords = extract_keywords_with_ai(jd_text)
print(f"AI Keywords: {ai_keywords}")

# Load CV and match
try:
    cv_text = extract_cv_text("samples/DINU_CV_ENGLISH.docx")
    matched, missing = match_keywords(cv_text, ai_keywords)
    
    print(f"\nMATCHED: {matched}")
    print(f"MISSING: {missing}")
    print(f"\nPlaywright in missing: {'playwright' in missing}")
    
    # Generate summary with improved prompt
    summary = generate_summary(matched, missing, jd_text)
    
    print(f"\n=== GENERATED SUMMARY ===")
    print(summary)
    
    # Check if it mentions forbidden skills
    print(f"\n=== HALLUCINATION CHECK ===")
    summary_lower = summary.lower()
    for forbidden_skill in missing:
        if forbidden_skill in summary_lower:
            print(f"❌ HALLUCINATION DETECTED: '{forbidden_skill}' mentioned in summary!")
        else:
            print(f"✅ Good: '{forbidden_skill}' not mentioned")
            
except Exception as e:
    print(f"Error: {e}")