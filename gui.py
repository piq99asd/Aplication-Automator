import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
from tkinter import ttk
import threading
import os
import sys
import core
try:
    from docx2pdf import convert as docx2pdf_convert
    DOCX2PDF_AVAILABLE = True
except ImportError:
    DOCX2PDF_AVAILABLE = False

def show_friendly_error(e):
    msg = str(e)
    if "OPENAI_API_KEY" in msg or "api key" in msg.lower():
        messagebox.showerror("Configuration Error", "OpenAI API key not set. Please set the OPENAI_API_KEY environment variable in your system or .env file.")
    elif "Word" in msg and ("not installed" in msg or "not found" in msg):
        messagebox.showerror("Word Not Installed", "Microsoft Word is required for PDF export. Please install and activate Word.")
    elif "permission denied" in msg.lower() or "in use" in msg.lower():
        messagebox.showerror("File In Use", "The file is open in another program or you do not have permission to write to it. Please close the file and try again.")
    elif "No such file or directory" in msg or "file not found" in msg.lower():
        messagebox.showerror("File Not Found", "One of the selected files could not be found. Please check the file paths and try again.")
    elif "rate limit" in msg.lower():
        messagebox.showerror("API Rate Limit", "You have reached the OpenAI API rate limit. Please wait and try again later.")
    elif "network" in msg.lower() or "timeout" in msg.lower():
        messagebox.showerror("Network Error", "A network error occurred while contacting the OpenAI API. Please check your internet connection and try again.")
    else:
        messagebox.showerror("Error", msg)

class JobAppAutomatorGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Job Application Automator")
        self.cv_path = tk.StringVar()
        self.jd_path = tk.StringVar()
        self.status = tk.StringVar()
        self.summary_text = None
        self.generated_summary = None
        self.cv_file = None
        self.jd_file = None
        self.save_as_pdf_var = tk.BooleanVar()
        self.cover_letter_btn = None
        self.progress = None
        self.prompt_custom = tk.StringVar(value="")
        self.pasted_jd_text = None
        self.paste_jd_label = None
        self.advanced_mode_toggled = tk.BooleanVar()
        

        self.create_widgets()
    def toggle_advanced_mode(self):
        print(f"Advanced mode is toggled: {self.advanced_mode_toggled.get()}")

    def create_widgets(self):
        tk.Label(self.root, text="CV File (.docx or .pdf):").grid(row=0, column=0, sticky="e")
        tk.Entry(self.root, textvariable=self.cv_path, width=50).grid(row=0, column=1)
        tk.Button(self.root, text="Browse", command=self.browse_cv).grid(row=0, column=2)

        tk.Label(self.root, text="Job Description File (.txt or .pdf):").grid(row=1, column=0, sticky="e")
        tk.Entry(self.root, textvariable=self.jd_path, width=50).grid(row=1, column=1)
        tk.Button(self.root, text="Browse", command=self.browse_jd).grid(row=1, column=2)
        tk.Button(self.root, text="Paste Job Description", command=self.open_paste_jd_dialog).grid(row=1, column=3, padx=5)
        self.paste_jd_label = tk.Label(self.root, text="", fg="green")
        self.paste_jd_label.grid(row=3, column=3, padx=5)

        self.save_as_pdf_checkbox = tk.Checkbutton(self.root, text="Save as PDF (for .docx CV)", variable=self.save_as_pdf_var, state=tk.DISABLED)
        self.save_as_pdf_checkbox.grid(row=2, column=0, columnspan=3, pady=2)

        
        self.advanced_mode_checkbox = tk.Checkbutton(self.root, text="Advanced Mode", variable=self.advanced_mode_toggled, command=self.toggle_advanced_mode)
        self.advanced_mode_checkbox.grid(row=2, column=3, padx=5)


        self.generate_btn = tk.Button(self.root, text="Generate Tailored Summary", command=self.run_automation)
        self.generate_btn.grid(row=3, column=0, columnspan=3, pady=10)

        self.save_btn = tk.Button(self.root, text="Save Updated CV", command=self.save_updated_cv, state=tk.DISABLED)
        self.save_btn.grid(row=4, column=0, pady=5)
        self.preview_btn = tk.Button(self.root, text="Preview Updated CV", command=self.preview_updated_cv, state=tk.DISABLED)
        self.preview_btn.grid(row=4, column=1, pady=5)
        self.prompt_btn = tk.Button(self.root, text="Prompt Options", command=self.open_prompt_options)
        self.prompt_btn.grid(row=4, column=2, pady=5)

        self.cover_letter_btn = tk.Button(self.root, text="Generate Cover Letter", command=self.open_cover_letter_dialog, state=tk.DISABLED)
        self.cover_letter_btn.grid(row=5, column=0, columnspan=3, pady=5)

        self.progress = ttk.Progressbar(self.root, mode='indeterminate')
        self.progress.grid(row=6, column=0, columnspan=3, sticky="ew", padx=10, pady=2)
        self.progress.grid_remove()

        tk.Label(self.root, textvariable=self.status, fg="blue").grid(row=7, column=0, columnspan=3)

        tk.Label(self.root, text="Generated Summary (editable):").grid(row=8, column=0, sticky="nw")
        self.summary_text = scrolledtext.ScrolledText(self.root, width=70, height=10, wrap=tk.WORD)
        self.summary_text.grid(row=8, column=1, columnspan=2, pady=5)
        self.summary_text.config(state=tk.DISABLED)

    def check_cover_letter_availability(self):
        cv_available = bool(self.cv_path.get() or hasattr(self, 'cv_file'))
        jd_available = bool(self.jd_path.get() or self.pasted_jd_text)
        
        if cv_available and jd_available:
            self.cover_letter_btn.config(state=tk.NORMAL)
        else:
            self.cover_letter_btn.config(state=tk.DISABLED)

    def show_progress(self):
        self.progress.grid()
        self.progress.start(10)
        self.root.update_idletasks()

    def hide_progress(self):
        self.progress.stop()
        self.progress.grid_remove()
        self.root.update_idletasks()

    def browse_cv(self):
        file_path = filedialog.askopenfilename(filetypes=[("CV Files", "*.docx *.pdf")])
        if file_path:
            self.cv_path.set(file_path)
            ext = os.path.splitext(file_path)[1].lower()
            if ext == ".docx" and DOCX2PDF_AVAILABLE:
                self.save_as_pdf_checkbox.config(state=tk.NORMAL)
            else:
                self.save_as_pdf_var.set(False)
                self.save_as_pdf_checkbox.config(state=tk.DISABLED)
            self.check_cover_letter_availability()

    def browse_jd(self):
        file_path = filedialog.askopenfilename(filetypes=[("Job Description Files", "*.txt *.pdf")])
        if file_path:
            self.jd_path.set(file_path)
            self.check_cover_letter_availability()

    def open_paste_jd_dialog(self):
        dialog = tk.Toplevel(self.root)
        dialog.title("Paste Job Description")
        tk.Label(dialog, text="Paste the job description below:").pack(anchor="w")
        text_widget = scrolledtext.ScrolledText(dialog, width=60, height=20, wrap=tk.WORD)
        text_widget.pack(padx=10, pady=5)
        if self.pasted_jd_text:
            text_widget.insert(tk.END, self.pasted_jd_text)
        def save_paste():
            pasted = text_widget.get(1.0, tk.END).strip()
            self.pasted_jd_text = pasted if pasted else None
            if self.pasted_jd_text:
                self.paste_jd_label.config(text="Using pasted job description")
            else:
                self.paste_jd_label.config(text="")
            dialog.destroy()
            self.check_cover_letter_availability()
        tk.Button(dialog, text="Save", command=save_paste).pack(pady=10)

    def run_automation(self):
        # Run in separate thread to prevent GUI freezing during API calls
        thread = threading.Thread(target=self._run_automation_thread)
        thread.start()

    def _run_automation_thread(self):
        self.show_progress()
        self.cv_file = self.cv_path.get()
        self.jd_file = self.jd_path.get()
        if not self.cv_file and not self.pasted_jd_text:
            self.hide_progress()
            messagebox.showerror("Error", "Please select a CV file and provide a job description (file or paste).")
            return
        if not self.cv_file:
            self.hide_progress()
            messagebox.showerror("Error", "Please select a CV file.")
            return
        if not self.pasted_jd_text and not self.jd_file:
            self.hide_progress()
            messagebox.showerror("Error", "Please provide a job description (file or paste).")
            return
        if not os.path.isfile(self.cv_file):
            self.hide_progress()
            messagebox.showerror("File Not Found", f"CV file not found: {self.cv_file}")
            return
        cv_ext = os.path.splitext(self.cv_file)[1].lower()
        if cv_ext not in [".docx", ".pdf"]:
            self.hide_progress()
            messagebox.showerror("Invalid File Type", "CV file must be a .docx or .pdf file.")
            return
        try:
            cv_text = core.parse_cv(self.cv_file)
            if self.pasted_jd_text:
                jd_text = self.pasted_jd_text
                jd_keywords = core.parse_jd("dummy.txt")[1] if False else core.parse_jd
                from jd_parser import extract_keywords_from_jd, extract_keywords_with_ai, extract_job_title_from_jd, extract_company_from_jd
                if self.advanced_mode_toggled.get():
                    jd_keywords = extract_keywords_with_ai(jd_text)
                else:
                    jd_keywords = extract_keywords_from_jd(jd_text)
                job_title = extract_job_title_from_jd(jd_text)
                company_name = extract_company_from_jd(jd_text)
            else:
                jd_text, jd_keywords, job_title, company_name = core.parse_jd(self.jd_file)
                if self.advanced_mode_toggled.get():
                    jd_keywords = extract_keywords_with_ai(jd_text)
                else:
                    jd_keywords = extract_keywords_from_jd(jd_text)
            matched, missing = core.match_cv_to_jd(cv_text, jd_keywords)
            self.status.set("Generating tailored summary...")
            self.root.update_idletasks()
            summary = core.generate_cv_summary(matched, missing, jd_text=jd_text, custom_instructions=self.prompt_custom.get())
            self.generated_summary = summary
            self.matched = matched
            self.missing = missing
            self.job_title = job_title
            self.company_name = company_name
            self.save_btn.config(state=tk.NORMAL)
            self.preview_btn.config(state=tk.NORMAL)
            self.summary_text.config(state=tk.NORMAL)
            self.summary_text.delete(1.0, tk.END)
            self.summary_text.insert(tk.END, summary)
            self.summary_text.config(state=tk.NORMAL)
            self.status.set("Summary generated. You can edit it below. Click 'Save Updated CV' when ready.")
        except Exception as e:
            self.status.set(f"Error: {e}")
            show_friendly_error(e)
        self.hide_progress()

    def _save_updated_cv_thread(self):
        self.show_progress()
        if not self.cv_file:
            self.hide_progress()
            messagebox.showerror("Error", "No CV file loaded.")
            return
        edited_summary = self.summary_text.get(1.0, tk.END).strip()
        if not edited_summary:
            self.hide_progress()
            messagebox.showerror("Error", "Summary cannot be empty.")
            return
        ext = os.path.splitext(self.cv_file)[1].lower()
        if ext not in [".docx", ".pdf"]:
            self.hide_progress()
            messagebox.showerror("Invalid File Type", "CV file must be a .docx or .pdf file.")
            return
        base_name = os.path.splitext(os.path.basename(self.cv_file))[0]
        default_name = f"{base_name}_updated{ext}"
        output_path = filedialog.asksaveasfilename(
            defaultextension=ext,
            filetypes=[("DOCX", "*.docx"), ("PDF", "*.pdf")],
            title="Save updated CV as...",
            initialfile=default_name
        )
        if not output_path:
            self.hide_progress()
            self.status.set("Operation cancelled.")
            return
        try:
            self.status.set("Saving updated CV...")
            self.root.update_idletasks()
            if ext == ".pdf":
                core.update_pdf_summary(self.cv_file, edited_summary, output_path)
            elif ext == ".docx":
                core.update_docx_summary(self.cv_file, edited_summary, output_path)
                if self.save_as_pdf_var.get():
                    if not DOCX2PDF_AVAILABLE:
                        messagebox.showerror("Error", "docx2pdf is not installed. Please install it to enable PDF export.")
                    else:
                        try:
                            pdf_output = os.path.splitext(output_path)[0] + ".pdf"
                            docx2pdf_convert(output_path, pdf_output)
                            if os.path.exists(pdf_output):
                                messagebox.showinfo("Success", f"PDF also saved as '{pdf_output}'")
                            else:
                                messagebox.showerror("Error", f"PDF was not created as expected at '{pdf_output}'")
                        except Exception as e:
                            show_friendly_error(e)
            else:
                raise ValueError("Unsupported CV format. Use PDF or DOCX.")
            self.status.set(f"✅ CV updated and saved as '{output_path}'")
            messagebox.showinfo("Success", f"CV updated and saved as '{output_path}'")
        except Exception as e:
            self.status.set(f"Error: {e}")
            show_friendly_error(e)
        self.hide_progress()

    def save_updated_cv(self):
        # Run in separate thread to prevent GUI freezing during file operations
        thread = threading.Thread(target=self._save_updated_cv_thread)
        thread.start()

    def preview_updated_cv(self):
        # Simulate the updated CV text (summary replaced)
        try:
            ext = os.path.splitext(self.cv_file)[1].lower()
            cv_text = core.parse_cv(self.cv_file)
            summary = self.summary_text.get(1.0, tk.END).strip()
            if ext == ".pdf":
                from summary_replacer import replace_summary_section
                preview_text = replace_summary_section(cv_text, summary)
            elif ext == ".docx":
                preview_text = f"[SUMMARY SECTION]\n{summary}\n\n[CV CONTENT]\n" + cv_text[:10000]
            else:
                preview_text = cv_text
            self.show_preview_window("CV Preview", preview_text)
        except Exception as e:
            show_friendly_error(e)

    def show_preview_window(self, title, content):
        win = tk.Toplevel(self.root)
        win.title(title)
        tk.Label(win, text=title).pack(anchor="w")
        text_widget = scrolledtext.ScrolledText(win, width=90, height=30, wrap=tk.WORD)
        text_widget.pack(padx=10, pady=5)
        text_widget.insert(tk.END, content)
        text_widget.config(state=tk.DISABLED)

    def open_cover_letter_dialog(self):
        if self.pasted_jd_text:
            from jd_parser import extract_job_title_from_jd, extract_company_from_jd
            job_title = extract_job_title_from_jd(self.pasted_jd_text)
            company_name = extract_company_from_jd(self.pasted_jd_text)
        elif self.jd_path.get():
            try:
                jd_text, jd_keywords, job_title, company_name = core.parse_jd(self.jd_path.get())
            except:
                job_title = getattr(self, 'job_title', "Job Title")
                company_name = getattr(self, 'company_name', "the company")
        else:
            job_title = getattr(self, 'job_title', "Job Title")
            company_name = getattr(self, 'company_name', "the company")
        dialog = tk.Toplevel(self.root)
        dialog.title("Cover Letter Details")
        tk.Label(dialog, text="Candidate Name:").grid(row=0, column=0, sticky="e")
        name_var = tk.StringVar(value="Dinu Alexandru-Cristian")
        tk.Entry(dialog, textvariable=name_var, width=30).grid(row=0, column=1)
        tk.Label(dialog, text="Job Title:").grid(row=1, column=0, sticky="e")
        job_var = tk.StringVar(value=job_title)
        tk.Entry(dialog, textvariable=job_var, width=30).grid(row=1, column=1)
        tk.Label(dialog, text="Company Name:").grid(row=2, column=0, sticky="e")
        company_var = tk.StringVar(value=company_name)
        tk.Entry(dialog, textvariable=company_var, width=30).grid(row=2, column=1)
        def on_generate():
            dialog.destroy()
            self.generate_and_show_cover_letter(name_var.get(), job_var.get(), company_var.get())
        tk.Button(dialog, text="Generate Cover Letter", command=on_generate).grid(row=3, column=0, columnspan=2, pady=10)

    def open_prompt_options(self):
        dialog = tk.Toplevel(self.root)
        dialog.title("Prompt Options")
        tk.Label(dialog, text="Custom Instructions:").grid(row=0, column=0, sticky="ne")
        custom_entry = tk.Text(dialog, width=40, height=5)
        custom_entry.insert(tk.END, self.prompt_custom.get())
        custom_entry.grid(row=0, column=1, padx=5, pady=5)
        def save_options():
            self.prompt_custom.set(custom_entry.get(1.0, tk.END).strip())
            dialog.destroy()
        tk.Button(dialog, text="Save", command=save_options).grid(row=1, column=0, columnspan=2, pady=10)

    def generate_and_show_cover_letter(self, candidate_name, job_title, company_name):
        # Run in separate thread to prevent GUI freezing during API calls
        thread = threading.Thread(target=self._generate_and_show_cover_letter_thread, args=(candidate_name, job_title, company_name))
        thread.start()

    def _generate_and_show_cover_letter_thread(self, candidate_name, job_title, company_name):
        self.show_progress()
        cv_file = getattr(self, 'cv_file', None) or self.cv_path.get()
        
        if not cv_file and not self.pasted_jd_text:
            self.hide_progress()
            messagebox.showerror("Error", "Please select a CV file and provide a job description (file or paste).")
            return
        if not cv_file:
            self.hide_progress()
            messagebox.showerror("Error", "Please select a CV file.")
            return
        if not self.pasted_jd_text and not self.jd_path.get():
            self.hide_progress()
            messagebox.showerror("Error", "Please provide a job description (file or paste).")
            return
        cv_ext = os.path.splitext(cv_file)[1].lower()
        if cv_ext not in [".docx", ".pdf"]:
            self.hide_progress()
            messagebox.showerror("Invalid File Type", "CV file must be a .docx or .pdf file.")
            return
        try:
            cv_text = core.parse_cv(cv_file)
            if self.pasted_jd_text:
                from jd_parser import extract_keywords_from_jd
                jd_text = self.pasted_jd_text
                jd_keywords = extract_keywords_from_jd(jd_text)
            else:
                jd_text, jd_keywords, _, _ = core.parse_jd(self.jd_path.get())
            matched, missing = core.match_cv_to_jd(cv_text, jd_keywords)
            self.status.set("Generating cover letter...")
            self.root.update_idletasks()
            cover_letter = core.generate_cv_cover_letter(matched, missing, job_title, candidate_name, company_name, custom_instructions=self.prompt_custom.get())
        except Exception as e:
            self.status.set(f"Error: {e}")
            show_friendly_error(e)
            self.hide_progress()
            return
        self.status.set("Cover letter generated.")
        self.hide_progress()
        self.show_cover_letter_window(cover_letter)

    def show_cover_letter_window(self, cover_letter):
        win = tk.Toplevel(self.root)
        win.title("Generated Cover Letter")
        tk.Label(win, text="Cover Letter (editable):").pack(anchor="w")
        text_widget = scrolledtext.ScrolledText(win, width=80, height=20, wrap=tk.WORD)
        text_widget.pack(padx=10, pady=5)
        text_widget.insert(tk.END, cover_letter)
        text_widget.config(state=tk.NORMAL)
        def save_cover_letter():
            content = text_widget.get(1.0, tk.END).strip()
            file_path = filedialog.asksaveasfilename(
                defaultextension=".pdf",
                filetypes=[("PDF Document", "*.pdf"), ("Word Document", "*.docx"), ("Text File", "*.txt")],
                title="Save Cover Letter As...",
                initialfile="cover_letter.pdf"
            )
            if file_path:
                if file_path.endswith(".pdf"):
                    try:
                        self.generate_cover_letter_pdf(content, file_path)
                        messagebox.showinfo("Success", f"Cover letter saved as '{file_path}'")
                    except Exception as e:
                        show_friendly_error(e)
                elif file_path.endswith(".docx"):
                    try:
                        from docx import Document
                        from docx.shared import Inches
                        from docx.enum.text import WD_ALIGN_PARAGRAPH
                        
                        doc = Document()
                        style = doc.styles['Normal']
                        style.font.name = 'Times New Roman'
                        style.font.size = docx.shared.Pt(12)
                        
                        for para in content.split("\n\n"):
                            if para.strip():
                                p = doc.add_paragraph(para.strip())
                                p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
                        
                        doc.save(file_path)
                        messagebox.showinfo("Success", f"Cover letter saved as '{file_path}'")
                    except Exception as e:
                        show_friendly_error(e)
                else:
                    try:
                        with open(file_path, "w", encoding="utf-8") as f:
                            f.write(content)
                        messagebox.showinfo("Success", f"Cover letter saved as '{file_path}'")
                    except Exception as e:
                        show_friendly_error(e)
        def preview_cover_letter():
            content = text_widget.get(1.0, tk.END).strip()
            self.show_preview_window("Cover Letter Preview", content)
        btn_frame = tk.Frame(win)
        btn_frame.pack(pady=10)
        tk.Button(btn_frame, text="Save Cover Letter", command=save_cover_letter).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Preview Cover Letter", command=preview_cover_letter).pack(side=tk.LEFT, padx=5)

    def generate_cover_letter_pdf(self, content, output_path):
        try:
            import fitz
            
            doc = fitz.open()
            page = doc.new_page()
            
            font_size = 12
            font_name = "Times-Roman"
            line_height = font_size * 1.2
            
            margin_left = 72
            margin_right = 72
            margin_top = 72
            margin_bottom = 72
            
            page_width = page.rect.width
            page_height = page.rect.height
            text_width = page_width - margin_left - margin_right
            text_height = page_height - margin_top - margin_bottom
            
            x = margin_left
            y = margin_top
            
            paragraphs = [p.strip() for p in content.split('\n\n') if p.strip()]
            
            for paragraph in paragraphs:
                if y + line_height > page_height - margin_bottom:
                    page = doc.new_page()
                    y = margin_top
                
                page.insert_text(
                    (x, y),
                    paragraph,
                    fontsize=font_size,
                    fontname=font_name,
                    color=(0, 0, 0)
                )
                
                lines = paragraph.split('\n')
                y += len(lines) * line_height + 10
            
            doc.save(output_path)
            doc.close()
            
        except ImportError:
            raise Exception("PyMuPDF (fitz) is required for PDF generation. Please install it with: pip install PyMuPDF")
        except Exception as e:
            raise Exception(f"Error generating PDF: {str(e)}")


def main():
    root = tk.Tk()
    app = JobAppAutomatorGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main() 