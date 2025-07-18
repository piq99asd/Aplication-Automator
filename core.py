import os
from cv_parser import extract_cv_text
from jd_parser import extract_text_from_jd, extract_keywords_from_jd, extract_job_title_from_jd, extract_company_from_jd
from matcher import match_keywords
from summary_generator import generate_summary, generate_cover_letter
from cv_editor import replace_summary_section_docx
from pdf_rewriter import preserve_original_formatting


def parse_cv(cv_path):
    return extract_cv_text(cv_path)

def parse_jd(jd_path):
    text = extract_text_from_jd(jd_path)
    keywords = extract_keywords_from_jd(text)
    job_title = extract_job_title_from_jd(text)
    company = extract_company_from_jd(text)
    return text, keywords, job_title, company

def match_cv_to_jd(cv_text, jd_keywords):
    return match_keywords(cv_text, jd_keywords)

def generate_cv_summary(matched, missing, job_title, tone="Default", custom_instructions=""):
    return generate_summary(matched, missing, job_title=job_title, tone=tone, custom_instructions=custom_instructions)

def generate_cv_cover_letter(matched, missing, job_title, candidate_name, company_name, tone="Default", custom_instructions=""):
    return generate_cover_letter(matched, missing, job_title, candidate_name, company_name, tone=tone, custom_instructions=custom_instructions)

def update_docx_summary(cv_path, summary, output_path):
    replace_summary_section_docx(cv_path, summary, output_path)

def update_pdf_summary(cv_path, summary, output_path):
    preserve_original_formatting(cv_path, summary, output_path)

def skill_gap_recommendation(skill):
    import openai
    prompt = f"Suggest a concise, practical way for a job seeker to address the following skill gap: '{skill}'. Recommend a course, resource, or learning path."
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.5,
        max_tokens=100
    )
    return response.choices[0].message["content"].strip() 