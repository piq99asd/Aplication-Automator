import os
import fitz
import re

def extract_text_from_jd(file_path):
    ext = os.path.splitext(file_path)[1].lower()
    
    if ext == ".pdf":
        text = ""
        with fitz.open(file_path) as doc:
            for page in doc:
                text += page.get_text()
        return text
    
    elif ext == ".txt":
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()
    
    else:
        raise ValueError("Unsupported JD format. Use .txt or .pdf")

def extract_job_title_from_jd(jd_text):
    lines = jd_text.splitlines()
    
    # Look for job title after "About the job/role" section
    for i, line in enumerate(lines):
        if re.search(r"about the (job|role)", line, re.IGNORECASE):
            for j in range(i+1, min(i+8, len(lines))):
                candidate = lines[j].strip()
                if not candidate:
                    continue
                
                cleaned = clean_job_title(candidate)
                if cleaned:
                    return cleaned
    
    # Look for common job title patterns: "as a [Title]", "join as [Title]", etc.
    for line in lines:
        candidate = line.strip()
        if not candidate:
            continue
        
        # Pattern: "as a Senior Developer"
        as_pattern = re.search(r'as a\s+([A-Z][A-Za-z\s()&]+?)(?:\s*[,(]|$)', candidate, re.IGNORECASE)
        if as_pattern:
            job_title = as_pattern.group(1).strip()
            cleaned = clean_job_title(job_title)
            if cleaned:
                return cleaned
        
        # Pattern: "join as QA Engineer"
        join_pattern = re.search(r'join as\s+([A-Z][A-Za-z\s()&]+?)(?:\s*[,(]|$)', candidate, re.IGNORECASE)
        if join_pattern:
            job_title = join_pattern.group(1).strip()
            cleaned = clean_job_title(job_title)
            if cleaned:
                return cleaned
        
        # Pattern: "we are seeking a Software Developer"
        seeking_pattern = re.search(r'we are seeking a\s+([A-Z][A-Za-z\s()&]+?)(?:\s*[,(]|$)', candidate, re.IGNORECASE)
        if seeking_pattern:
            job_title = seeking_pattern.group(1).strip()
            cleaned = clean_job_title(job_title)
            if cleaned:
                return cleaned
        
        # Pattern: "we are seeking a skilled Python Developer to join"
        seeking_skilled_pattern = re.search(r'we are seeking a skilled\s+([A-Z][A-Za-z\s()&]+?)(?:\s+to\s+|\s*[,(]|$)', candidate, re.IGNORECASE)
        if seeking_skilled_pattern:
            job_title = seeking_skilled_pattern.group(1).strip()
            job_title = re.sub(r'\s+to\s+.*$', '', job_title, flags=re.IGNORECASE)  # Remove "to join..." part
            cleaned = clean_job_title(job_title)
            if cleaned:
                return cleaned
    
    # Look for job keywords in first 15 lines as fallback
    for line in lines[:15]:
        candidate = line.strip()
        if not candidate:
            continue
        
        if re.search(r"engineer|developer|manager|lead|analyst|tester|designer|architect|specialist|consultant|administrator|officer|director|qa|devops", candidate, re.IGNORECASE):
            cleaned = clean_job_title(candidate)
            if cleaned:
                return cleaned
    
    return "Job Title"

def clean_job_title(text):
    prefixes = [
        r"^we are (looking for|hiring)\s+",
        r"^we're (looking for|hiring)\s+",
        r"^we\s+",
        r"^our team is looking for\s+",
        r"^join us as\s+",
        r"^we are seeking\s+",
        r"^we're seeking\s+"
    ]
    
    cleaned = text
    for prefix in prefixes:
        cleaned = re.sub(prefix, "", cleaned, flags=re.IGNORECASE)
    
    cleaned = re.sub(r"\s+at\s+.*$", "", cleaned, flags=re.IGNORECASE)
    
    cleaned = re.sub(r"[.,\s]+$", "", cleaned.strip())
    
    cleaned = re.sub(r"^(a|an)\s+", "", cleaned, flags=re.IGNORECASE)
    
    if cleaned and len(cleaned.split()) <= 6:
        return cleaned
    
    return None

def extract_company_from_jd(jd_text):
    lines = jd_text.splitlines()
    
    # Look for company name patterns in first 20 lines
    for line in lines[:20]:
        candidate = line.strip()
        if not candidate:
            continue
        
        # Pattern: "at Google" or "at Microsoft Corporation"
        at_match = re.search(r'\bat\s+([A-Z][A-Za-z\s&.,]+?)(?:\s*[,.]|$)', candidate, re.IGNORECASE)
        if at_match:
            company_name = at_match.group(1).strip()
            company_name = re.sub(r'[.,\s]+$', '', company_name)  # Remove trailing punctuation
            if company_name and len(company_name.split()) <= 5:
                return company_name
        
        # Pattern: "3Pillar Global!" (company name with exclamation)
        exclamation_match = re.search(r'([A-Z0-9][A-Za-z0-9\s&.,]+?)\s*!', candidate)
        if exclamation_match:
            company_name = exclamation_match.group(1).strip()
            company_name = re.sub(r'[.,\s]+$', '', company_name)
            if company_name and len(company_name.split()) <= 5:
                # Exclude tech keywords that might be mistaken for company names
                tech_words = r'\b(cypress|playwright|selenium|jira|github|gitlab|docker|kubernetes|aws|azure|react|angular|vue|python|java|javascript|typescript|sql|git|linux|bash|rest|api|testing|agile|scrum|devops|jenkins|bitbucket|maven|gradle|npm|yarn|webpack|babel|eslint|prettier|jest|mocha|pytest|unittest|junit|mockito|sonarqube|sonar|terraform|ansible|chef|puppet|prometheus|grafana|elk|splunk|datadog|newrelic|apache|nginx|tomcat|spring|hibernate|jpa|jdbc|powermock|appium|cucumber|behave|robot|postman|swagger|openapi|graphql|soap|xml|json|yaml|html|css|sass|less|bootstrap|tailwind|material|figma|sketch|adobe|photoshop|illustrator|invision|zeplin|framer|protopie|principle|lottie|after|effects|premiere|final|cut|pro|logic|tools|mongodb|postgresql|mysql|redis|elasticsearch|kafka|node|express|django|flask)\b'
                if not re.search(tech_words, company_name, re.IGNORECASE):
                    return company_name
        
        # Pattern: "with TechCorp" or "with Amazing Startup"
        with_pattern = re.search(r'with\s+([A-Z0-9][A-Za-z0-9\s&.,]+?)(?:\s*[!.,]|$)', candidate)
        if with_pattern:
            company_name = with_pattern.group(1).strip()
            company_name = re.sub(r'[.,\s]+$', '', company_name)
            if company_name and len(company_name.split()) <= 5:
                # Exclude tech keywords that might be mistaken for company names
                tech_words = r'\b(cypress|playwright|selenium|jira|github|gitlab|docker|kubernetes|aws|azure|react|angular|vue|python|java|javascript|typescript|sql|git|linux|bash|rest|api|testing|agile|scrum|devops|jenkins|bitbucket|maven|gradle|npm|yarn|webpack|babel|eslint|prettier|jest|mocha|pytest|unittest|junit|mockito|sonarqube|sonar|terraform|ansible|chef|puppet|prometheus|grafana|elk|splunk|datadog|newrelic|apache|nginx|tomcat|spring|hibernate|jpa|jdbc|powermock|appium|cucumber|behave|robot|postman|swagger|openapi|graphql|soap|xml|json|yaml|html|css|sass|less|bootstrap|tailwind|material|figma|sketch|adobe|photoshop|illustrator|invision|zeplin|framer|protopie|principle|lottie|after|effects|premiere|final|cut|pro|logic|tools|mongodb|postgresql|mysql|redis|elasticsearch|kafka|node|express|django|flask)\b'
                if not re.search(tech_words, company_name, re.IGNORECASE):
                    return company_name
    
    company_patterns = [
        r'\b(?:at|with|join|working for)\s+([A-Z][A-Za-z\s&.,]+?)(?:\s*[,.]|$)',
        r'\b([A-Z][A-Za-z\s&.,]+?)\s+(?:company|corporation|inc|llc|ltd)\b',
        r'\b(?:opportunity to join|work with)\s+([A-Z][A-Za-z\s&.,]+?)(?:\s*[,.]|$)',
        r'\b(?:join|work at)\s+([A-Z][A-Za-z\s&.,]+?)(?:\s*[,.]|$)',
        r'\b(?:we are a|we are)\s+([A-Z][A-Za-z\s&.,]+?)(?:\s*[,.]|$)',
        r'\b(?:leading|fast growing)\s+([A-Z][A-Za-z\s&.,]+?)(?:\s*[,.]|$)'
    ]
    
    for line in lines[:20]:
        candidate = line.strip()
        if not candidate:
            continue
        
        for pattern in company_patterns:
            match = re.search(pattern, candidate, re.IGNORECASE)
            if match:
                company_name = match.group(1).strip()
                company_name = re.sub(r'[.,\s]+$', '', company_name)
                if company_name and len(company_name.split()) <= 5:
                    tech_words = r'\b(cypress|playwright|selenium|jira|github|gitlab|docker|kubernetes|aws|azure|react|angular|vue|python|java|javascript|typescript|sql|git|linux|bash|rest|api|testing|agile|scrum|devops|jenkins|bitbucket|maven|gradle|npm|yarn|webpack|babel|eslint|prettier|jest|mocha|pytest|unittest|junit|mockito|sonarqube|sonar|terraform|ansible|chef|puppet|prometheus|grafana|elk|splunk|datadog|newrelic|apache|nginx|tomcat|spring|hibernate|jpa|jdbc|powermock|appium|cucumber|behave|robot|postman|swagger|openapi|graphql|soap|xml|json|yaml|html|css|sass|less|bootstrap|tailwind|material|figma|sketch|adobe|photoshop|illustrator|invision|zeplin|framer|protopie|principle|lottie|after|effects|premiere|final|cut|pro|logic|tools|mongodb|postgresql|mysql|redis|elasticsearch|kafka|node|express|django|flask)\b'
                    if not re.search(tech_words, company_name, re.IGNORECASE):
                        return company_name
    
    for line in lines[:5]:
        candidate = line.strip()
        if not candidate:
            continue
        
        leading_pattern = re.search(r'leading\s+([A-Za-z\s]+?)\s+(?:agency|company|firm|organization)', candidate, re.IGNORECASE)
        if leading_pattern:
            company_desc = leading_pattern.group(1).strip()
            if company_desc and len(company_desc.split()) <= 3:
                return company_desc.title()
        
        we_leading_pattern = re.search(r'we are a\s+leading\s+([A-Za-z\s]+?)\s+(?:agency|company|firm|organization)', candidate, re.IGNORECASE)
        if we_leading_pattern:
            company_desc = we_leading_pattern.group(1).strip()
            if company_desc and len(company_desc.split()) <= 3:
                return company_desc.title()
        
        growing_pattern = re.search(r'fast growing\s+([A-Za-z\s]+?)\s+(?:company|firm|organization)', candidate, re.IGNORECASE)
        if growing_pattern:
            company_desc = growing_pattern.group(1).strip()
            if company_desc and len(company_desc.split()) <= 3:
                return company_desc.title()
    
    job_keywords = r'\b(engineer|developer|manager|lead|analyst|tester|designer|architect|specialist|consultant|administrator|officer|director|qa|devops|position|role|job|contract|working|model)\b'
    
    for line in lines[:10]:
        candidate = line.strip()
        if not candidate or re.search(job_keywords, candidate, re.IGNORECASE):
            continue
        
        if candidate and candidate[0].isupper() and len(candidate.split()) <= 4:
            if not re.match(r'^(About|We|Our|The|This|A|An|Contract|Working|Model|Key|Qualifications)\b', candidate, re.IGNORECASE):
                return candidate
    
    return "the company"

def extract_keywords_from_jd(jd_text):
    jd_text = jd_text.lower()
    jd_text = re.sub(r"[\/\n]", " ", jd_text)
    jd_text = re.sub(r"[^a-z0-9\s]", "", jd_text)
    
    words = jd_text.split()
    keywords = []
    
    job_keywords = {
        "python", "java", "javascript", "typescript", "sql", "git", "linux", "bash",
        "rest", "api", "testing", "cypress", "playwright", "selenium", "jira",
        "agile", "scrum", "devops", "docker", "kubernetes", "aws", "azure",
        "react", "angular", "vue", "node", "express", "django", "flask",
        "mongodb", "postgresql", "mysql", "redis", "elasticsearch", "kafka",
        "jenkins", "github", "gitlab", "bitbucket", "maven", "gradle", "npm",
        "yarn", "webpack", "babel", "eslint", "prettier", "jest", "mocha",
        "pytest", "unittest", "junit", "mockito", "sonarqube", "sonar",
        "terraform", "ansible", "chef", "puppet", "prometheus", "grafana",
        "elk", "splunk", "datadog", "newrelic", "apache", "nginx", "tomcat",
        "spring", "hibernate", "jpa", "jdbc", "junit", "mockito", "powermock",
        "selenium", "appium", "cucumber", "behave", "robot", "postman",
        "swagger", "openapi", "graphql", "soap", "xml", "json", "yaml",
        "html", "css", "sass", "less", "bootstrap", "tailwind", "material",
        "figma", "sketch", "adobe", "photoshop", "illustrator", "invision",
        "zeplin", "framer", "protopie", "principle", "lottie", "after",
        "effects", "premiere", "final", "cut", "pro", "logic", "pro", "tools",
        "sketch", "figma", "invision", "zeplin", "framer", "protopie",
        "principle", "lottie", "after", "effects", "premiere", "final",
        "cut", "pro", "logic", "pro", "tools", "sketch", "figma", "invision",
        "zeplin", "framer", "protopie", "principle", "lottie", "after",
        "effects", "premiere", "final", "cut", "pro", "logic", "pro", "tools"
    }
    
    for word in words:
        if word in job_keywords and len(word) > 2:
            keywords.append(word)
    
    return sorted(list(set(keywords)))
