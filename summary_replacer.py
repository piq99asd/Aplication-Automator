import re

def replace_summary_section(cv_text, new_summary):
    # Regex to find summary section and capture content until next section or end
    # Matches "About Me" or "Summary", optional colon/dash, then content until next title
    pattern = re.compile(
        r"(about me|summary)\s*[:\-]?\s*(.*?)(?=\n[A-Z][A-Z\s]+:?|\n[A-Z][a-z]+.*:|\n\Z|\n\n|\Z)",
        re.IGNORECASE | re.DOTALL
    )

    def replacer(match):
        section_title = match.group(1).title()
        return f"{section_title}\n{new_summary}\n"

    if re.search(pattern, cv_text):
        updated_cv = re.sub(pattern, replacer, cv_text, count=1)
    else:
        updated_cv = f"ABOUT ME\n{new_summary}\n\n" + cv_text

    return updated_cv 