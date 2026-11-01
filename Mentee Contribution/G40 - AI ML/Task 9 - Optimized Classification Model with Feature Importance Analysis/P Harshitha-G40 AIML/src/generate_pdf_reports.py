import os
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
from reportlab.lib import colors

def build_pdf_from_text(title, text_file_path, output_pdf_path):
    doc = SimpleDocTemplate(
        output_pdf_path,
        pagesize=letter,
        rightMargin=40, leftMargin=40, topMargin=40, bottomMargin=40
    )
    
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Heading1'],
        fontSize=20,
        leading=24,
        textColor=colors.HexColor('#1a252f'),
        spaceAfter=15
    )
    h2_style = ParagraphStyle(
        'Heading2Custom',
        parent=styles['Heading2'],
        fontSize=14,
        leading=18,
        textColor=colors.HexColor('#2c3e50'),
        spaceBefore=12,
        spaceAfter=8
    )
    body_style = ParagraphStyle(
        'BodyCustom',
        parent=styles['Normal'],
        fontSize=10,
        leading=14,
        textColor=colors.HexColor('#34495e'),
        spaceAfter=6
    )

    story = []
    story.append(Paragraph(title, title_style))
    story.append(HRFlowable(width="100%", thickness=2, color=colors.HexColor('#3498db'), spaceAfter=15))

    if os.path.exists(text_file_path):
        with open(text_file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            
        for line in lines:
            line_str = line.strip()
            if not line_str:
                continue
            if line_str.startswith("# "):
                continue # Skip main title as added
            elif line_str.startswith("## "):
                story.append(Paragraph(line_str.replace("## ", ""), h2_style))
            elif line_str.startswith("### "):
                story.append(Paragraph(f"<b>{line_str.replace('### ', '')}</b>", h2_style))
            elif line_str.startswith("* ") or line_str.startswith("- "):
                story.append(Paragraph(f"• {line_str[2:]}", body_style))
            else:
                # Replace simple markdown bold
                clean_text = line_str.replace("**", "<b>", 1).replace("**", "</b>", 1)
                story.append(Paragraph(clean_text, body_style))
    
    doc.build(story)
    print(f"[PDF Generator] Successfully generated '{output_pdf_path}'.")

if __name__ == "__main__":
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "reports"))
    
    md_fi = os.path.join(base_dir, "feature_importance_report.md")
    pdf_fi = os.path.join(base_dir, "feature_importance_report.pdf")
    build_pdf_from_text("Feature Importance & Predictive Report", md_fi, pdf_fi)

    md_br = os.path.join(base_dir, "business_recommendations.md")
    pdf_br = os.path.join(base_dir, "business_recommendations.pdf")
    build_pdf_from_text("Strategic Business Recommendations", md_br, pdf_br)
