import openai
import os
from dotenv import load_dotenv
from jd_parser import extract_job_title_from_jd

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("OPENAI_API_KEY environment variable not set.")
openai.api_key = api_key


def generate_summary(matched, missing, jd_text, tone=None, custom_instructions=None):
    job_title = extract_job_title_from_jd(jd_text)
    # Build AI prompt with specific instructions to only mention actual skills
    prompt = f"""
You are an assistant that writes tailored CV summaries for job applications.

CRITICAL RULES - MUST FOLLOW EXACTLY:
1. ONLY mention skills from the ALLOWED list
2. NEVER mention skills from the FORBIDDEN list
3. If you mention ANY forbidden skill, the summary will be rejected
4. DO NOT claim fluency or proficiency in languages unless explicitly verified

ALLOWED skills (the candidate HAS these): {', '.join(matched) if matched else 'testing, python'}
FORBIDDEN skills (the candidate does NOT have these): {', '.join(missing)}

Write a 1-paragraph CV summary for a candidate applying to the position of "{job_title}". 
Write the summary in the first person (using 'I', 'my', etc.).
Only refer to the finished studies as "engineer".
Keep the language professional but not overly elevated - make it sound realistic and human.

EXAMPLES OF WHAT NOT TO SAY:
- Do NOT say "I have experience with {', '.join(missing[:3]) if missing else 'forbidden technologies'}"
- Do NOT imply knowledge of any forbidden technologies
- Do NOT mention learning/developing forbidden skills unless explicitly requested
- Do NOT claim fluency, proficiency, or advanced skills in languages from the FORBIDDEN list
- Do NOT say "multilingual" or "proficient in X languages" unless explicitly verified

You may mention eagerness to learn new technologies in general terms, but do not specifically name forbidden skills.
"""
    if tone and tone != "Default":
        prompt += f"\n\nUse a {tone.lower()} tone."
    else:
        prompt += "\n\nUse a confident, professional tone. Mention technical and soft skills when relevant. Keep it concise and realistic."
    if custom_instructions:
        prompt += f"\n\nAdditional instructions: {custom_instructions.strip()}"

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7,
        max_tokens=200
    )

    return response.choices[0].message["content"].strip()


def generate_cover_letter(matched, missing, job_title="Job Title", candidate_name="Candidate", company_name="the company", tone=None, custom_instructions=None):
    prompt = f"""
You are an assistant that writes tailored cover letters for job applications.

Write a professional, realistic, and concise cover letter for a candidate named {candidate_name} applying to the position of "{job_title}" at {company_name}.
Use the first person (using 'I', 'my', etc.).
Only mention as current skills and experience those found in this list: {', '.join(matched)}.
If no skills are found in the list, always mention that the candidate has experience in the field of testing and also Python.
Only refer to the finished studies as "engineer".
Do NOT claim the candidate has any skills or experience from this list: {', '.join(missing)}.
Optionally, you may mention the candidate's eagerness to develop in the missing areas, but do not state or imply they already possess them.

The letter should:
- Start with a brief introduction and the reason for applying
- Highlight relevant skills and experience
- Express enthusiasm for the role and company
- Mention willingness to grow in missing areas
- End with a polite closing
"""
    if tone and tone != "Default":
        prompt += f"\n\nUse a {tone.lower()} tone."
    else:
        prompt += "\n\nKeep the tone confident and professional, but not overly formal or exaggerated. Limit to 3-4 paragraphs."
    if custom_instructions:
        prompt += f"\n\nAdditional instructions: {custom_instructions.strip()}"

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7,
        max_tokens=400
    )

    return response.choices[0].message["content"].strip()
