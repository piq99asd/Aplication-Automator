

# Job Application Automator

Automate the process of tailoring your CV to specific job descriptions! This tool lets you select your CV, provide a job description (by file or by pasting text), and generates a customized summary and cover letter, which you can edit, preview, and save in your preferred format.

---

## Features
- User-friendly GUI for all operations
- Select your CV file (`.docx` or `.pdf`)
- Provide the job description by selecting a file (`.txt` or `.pdf`) **or** by pasting the text directly
- Generate a tailored summary for your CV
- Generate a tailored cover letter
- Edit the generated summary and cover letter before saving
- Preview the updated CV and cover letter before saving
- Add custom instructions to influence the AI output
- Save the updated CV as `.docx` or `.pdf`
- All processing is local except for summary/cover letter generation (uses OpenAI API)

---

## Step-by-Step User Guide

1. **Launch the GUI:**
   ```bash
   python gui.py
   ```
2. **Select your CV file:**
   - Click "Browse" next to "CV File" and choose a `.docx` or `.pdf` file.
3. **Provide the job description:**
   - Either click "Browse" next to "Job Description File" and select a `.txt` or `.pdf` file,
   - **OR** click "Paste Job Description" and paste the text into the dialog. If you paste text, it will be used instead of any selected file.
4. *(Optional)* **Add Custom Instructions:**
   - Click "Prompt Options" and enter any special instructions for the AI (e.g., "Emphasize teamwork", "Use British English", etc.).
5. **Generate Summary:**
   - Click "Generate Tailored Summary". The summary will appear in the editable box.
6. *(Optional)* **Preview:**
   - Click "Preview Updated CV" to see a preview of the updated CV.
7. *(Optional)* **Generate Cover Letter:**
   - Click "Generate Cover Letter" and review/edit the result. You can also preview it.
8. **Save the Updated CV:**
   - Click "Save Updated CV". You can also choose to save as PDF if your CV is a `.docx`.

---

## Troubleshooting

- **OpenAI API Key Not Set:**
  - Set the `OPENAI_API_KEY` environment variable or add it to a `.env` file in the project root.
- **Microsoft Word Required for PDF Export:**
  - PDF export from `.docx` requires Word to be installed and activated on Windows.
- **File In Use or Permission Denied:**
  - Close the file in other programs before saving or exporting.
- **Invalid File Type:**
  - Only `.docx` or `.pdf` for CVs, and `.txt` or `.pdf` for job descriptions are supported.
- **API Rate Limit or Network Error:**
  - Wait and try again later, or check your internet connection.

---

## Sample Files
- Example CVs and job descriptions are provided in the `samples/` folder.
- You can add your own files for testing.

---

## Screenshots

*Screenshots of the GUI and features will be added here.*



---

## Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/yourusername/job_application_automator.git
   cd job_application_automator
   ```
2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

---

## Usage (Legacy Command Line)

1. Place your CV (Word or PDF) and the job description (txt/pdf) in the `samples/` folder.
2. Run the main script:
   ```bash
   python main.py
   ```
3. The tool will parse your files, match your skills, generate a summary, and output an updated CV in the `samples/` folder.

---

## Technologies Used
- Python 3
- docx, PyPDF2, PyMuPDF, openai, and other libraries (see requirements.txt)

---

>>>>>>> ce7e6cf (Initial commit)
