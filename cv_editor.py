from docx import Document
import re

def replace_about_me(docx_path, new_summary, output_path="updated_cv.docx"):
    """
    Replace the summary section in a DOCX file while preserving formatting
    """
    doc = Document(docx_path)
    
    # Look for summary sections with various common names
    summary_headers = ["professional summary", "about me", "summary", "profile", "objective"]
    
    found_summary = False
    
    # First pass: look for summary headers
    for i, paragraph in enumerate(doc.paragraphs):
        text_lower = paragraph.text.lower().strip()
        
        # Check if this paragraph contains a summary header
        if any(header in text_lower for header in summary_headers):
            found_summary = True
            
            # Keep the header but replace the content
            # Find where the summary content starts (next paragraph)
            if i + 1 < len(doc.paragraphs):
                # Replace the next paragraph with the new summary
                doc.paragraphs[i + 1].text = new_summary
                
                # If the summary spans multiple paragraphs, we need to handle that
                # For now, we'll just replace the immediate next paragraph
                # and add additional paragraphs if needed
                
                # Split the new summary into paragraphs
                summary_paragraphs = new_summary.split('\n\n')
                
                if len(summary_paragraphs) > 1:
                    # Insert additional paragraphs after the first one
                    current_para = doc.paragraphs[i + 1]
                    current_para.text = summary_paragraphs[0]
                    
                    for j, para_text in enumerate(summary_paragraphs[1:], 1):
                        if para_text.strip():
                            # Insert a new paragraph after the current one
                            new_para = doc.add_paragraph(para_text.strip())
                            # Move it to the right position
                            doc._body._body.insert(current_para._element.getnext(), new_para._element)
                            current_para = new_para
                else:
                    # Single paragraph summary
                    doc.paragraphs[i + 1].text = new_summary
                
                break
    
    # If we didn't find a summary section, try to add one at the beginning
    if not found_summary:
        # Add a new paragraph at the beginning for the summary
        new_para = doc.add_paragraph("Professional Summary")
        new_para.style = 'Heading 2'  # Make it a heading
        
        # Add the summary content
        summary_para = doc.add_paragraph(new_summary)
        
        # Move these to the beginning
        doc._body._body.insert(0, new_para._element)
        doc._body._body.insert(1, summary_para._element)
    
    doc.save(output_path)
    print(f"✅ CV saved as {output_path}")

def replace_summary_section_docx(docx_path, new_summary, output_path="updated_cv.docx"):
    """
    Simplified summary replacement that preserves formatting
    """
    doc = Document(docx_path)
    
    summary_headers = ["professional summary", "about me", "summary", "profile", "objective"]
    
    # Find the summary section
    summary_start = None
    
    for i, paragraph in enumerate(doc.paragraphs):
        text_lower = paragraph.text.lower().strip()
        
        # Check if this is a summary header
        if any(header in text_lower for header in summary_headers):
            summary_start = i
            break
    
    if summary_start is not None and summary_start + 1 < len(doc.paragraphs):
        # Replace the paragraph after the header with the new summary
        doc.paragraphs[summary_start + 1].text = new_summary
        print(f"✅ Replaced summary at paragraph {summary_start + 1}")
    else:
        # No summary found, add one at the beginning
        # Create a new document with the summary at the top
        new_doc = Document()
        
        # Add the summary header
        header_para = new_doc.add_paragraph("Professional Summary")
        header_para.style = 'Heading 2'
        
        # Add the summary content
        summary_para = new_doc.add_paragraph(new_summary)
        
        # Add all paragraphs from the original document
        for paragraph in doc.paragraphs:
            new_doc.add_paragraph(paragraph.text)
        
        new_doc.save(output_path)
        print(f"✅ Created new CV with summary at the top")
        return
    
    doc.save(output_path)
    print(f"✅ CV saved as {output_path}")
