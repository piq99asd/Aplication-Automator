import fitz
import re
import os
from summary_replacer import replace_summary_section
import textwrap

def advanced_overlay_summary_in_pdf(original_pdf_path, new_summary, output_path):
    doc = fitz.open(original_pdf_path)
    page = doc[0]
    page_dict = page.get_text("dict")  # Extract text with position data
    summary_headers = ["professional summary", "about me", "summary", "profile"]
    summary_bbox = None
    found_header = None
    header_block_idx = None
    
    # Find the summary header and its bounding box coordinates
    for block_idx, block in enumerate(page_dict["blocks"]):
        if "lines" in block:
            for line in block["lines"]:
                for span in line["spans"]:
                    text = span["text"].lower().strip()
                    for header in summary_headers:
                        if header in text:
                            summary_bbox = span["bbox"]  # (x0, y0, x1, y1) coordinates
                            found_header = header
                            header_block_idx = block_idx
                            break
                    if summary_bbox:
                        break
                if summary_bbox:
                    break
        if summary_bbox:
            break
    if not summary_bbox:
        print("Could not find summary section header. No changes made.")
        doc.save(output_path)
        doc.close()
        return
    
    # Calculate the vertical extent of the summary section
    y0 = summary_bbox[1]  # Top of summary header
    y1 = summary_bbox[3]  # Bottom of summary header
    max_x1 = summary_bbox[2]
    found_end = False
    end_block_idx = None
    
    # Find where the summary section ends (next major section or big gap)
    for block_idx, block in enumerate(page_dict["blocks"]):
        if "lines" in block:
            for line in block["lines"]:
                for span in line["spans"]:
                    text = span["text"].lower().strip()
                    if span["bbox"][1] > y1 + 10:  # Text below current summary
                        # Check if it's a new section header or big gap
                        if (text.isupper() and len(text) > 3) or any(h in text for h in ["experience", "education", "skills", "projects", "certifications", "languages"]):
                            y1 = span["bbox"][1] - 2
                            found_end = True
                            end_block_idx = block_idx
                            break
                        if span["bbox"][1] - y1 > 40:  # Large vertical gap
                            y1 = span["bbox"][1] - 2
                            found_end = True
                            end_block_idx = block_idx
                            break
                        max_x1 = max(max_x1, span["bbox"][2])
                if found_end:
                    break
        if found_end:
            break
    if end_block_idx is None:
        end_block_idx = len(page_dict["blocks"]) - 1
    
    # Prepare new summary text with proper line wrapping
    fontname = "Helvetica"
    fontsize = 11
    header_fontsize = fontsize + 2
    lines = []
    for paragraph in new_summary.split("\n"):
        lines.extend(textwrap.wrap(paragraph, width=90))
    
    # Calculate height needed for new summary
    summary_line_height = fontsize + 4
    header_line_height = header_fontsize + 4
    new_summary_height = header_line_height + len(lines) * summary_line_height
    old_summary_height = y1 - y0
    shift_delta = max(0, new_summary_height - old_summary_height)  # How much to shift content below
    
    # Clear old content by drawing white rectangle
    rect = fitz.Rect(summary_bbox[0], y0, page.rect.width - 20, page.rect.height - 20)
    page.draw_rect(rect, color=(1, 1, 1), fill=(1, 1, 1))  # White fill
    
    # Insert new summary header and content
    page.insert_text((summary_bbox[0], y0), found_header.title(), fontsize=header_fontsize, fontname="Helvetica-Bold")
    current_y = y0 + header_line_height
    for line in lines:
        if line.strip():
            page.insert_text((summary_bbox[0], current_y), line.strip(), fontsize=fontsize, fontname=fontname)
            current_y += summary_line_height
    
    # Re-insert all content below summary, shifted down to avoid overlap
    for block_idx in range(header_block_idx + 1, len(page_dict["blocks"])):
        block = page_dict["blocks"][block_idx]
        if "lines" in block:
            for line in block["lines"]:
                for span in line["spans"]:
                    orig_x, orig_y = span["bbox"][0], span["bbox"][1]
                    page.insert_text((orig_x, orig_y + shift_delta), span["text"], fontsize=span["size"], fontname=fontname)
    
    doc.save(output_path)
    doc.close()
    print(f"✅ PDF with advanced non-overlapping summary saved as: {output_path}")

def preserve_original_formatting(original_pdf_path, updated_text, output_path):
    try:
        advanced_overlay_summary_in_pdf(original_pdf_path, updated_text, output_path)
    except Exception as e:
        print(f"Warning: Could not overlay summary: {e}")
        print("Falling back to new PDF generation...")
        generate_pdf_from_text(updated_text, output_path)

def generate_pdf_from_text(text, output_path="updated_cv.pdf"):
    import fitz
    doc = fitz.open()
    page = doc.new_page()
    lines = text.split('\n')
    y_position = 50
    left_margin = 50
    for line in lines:
        if not line.strip():
            y_position += 10
            continue
        if line.strip().upper() in ["PROFESSIONAL SUMMARY", "ABOUT ME", "SUMMARY"]:
            font_size = 16
            font_name = "Helvetica-Bold"
            y_position += 20
        elif any(keyword in line.lower() for keyword in ["experience", "education", "skills", "projects", "certifications", "languages"]):
            font_size = 14
            font_name = "Helvetica-Bold"
            y_position += 15
        elif line.strip().startswith(("-", "•", "*")):
            font_size = 10
            font_name = "Helvetica"
            page.insert_text((left_margin + 20, y_position), line.strip(), fontsize=font_size, fontname=font_name)
            y_position += font_size + 3
            continue
        else:
            font_size = 11
            font_name = "Helvetica"
        if y_position > page.rect.height - 100:
            page = doc.new_page()
            y_position = 50
        page.insert_text((left_margin, y_position), line.strip(), fontsize=font_size, fontname=font_name)
        y_position += font_size + 5
    doc.save(output_path)
    doc.close()
    print(f"✅ New PDF saved as: {output_path}")
