import html
import re
from io import BytesIO
from fpdf import FPDF
from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.shared import Pt


def sanitize_text(text: str) -> str:
    replacements = {
        "\u2018": "'",
        "\u2019": "'",
        "\u201c": '"',
        "\u201d": '"',
        "\u2013": "-",
        "\u2014": "-",
        "\u00a0": " ",
    }
    for old, new in replacements.items():
        text = text.replace(old, new)
    return text.strip()


def _clean_lines(text):
    return [line.strip() for line in sanitize_text(text).splitlines() if line.strip()]


def format_html_preview(text: str, doc_type: str) -> str:
    body = []
    for line in _clean_lines(text):
        safe = html.escape(line)
        if re.match(r"^(\d+[.)]|ARTICLE\s+\d+)", line, re.I):
            body.append(f"<h3>{safe}</h3>")
        else:
            body.append(f"<p>{safe}</p>")

    return f'''<div style="
        background:#111827;
        color:#f9fafb;
        padding:28px;
        border-radius:14px;
        max-height:520px;
        overflow-y:auto;
        font-family:Georgia,serif;
        line-height:1.65;">
        <h2 style="text-align:center;">{html.escape(doc_type)}</h2>
        {''.join(body)}
    </div>'''


def format_docx(text: str, doc_type: str) -> bytes:
    doc = Document()
    section = doc.sections[0]
    section.top_margin = section.bottom_margin = Pt(54)
    section.left_margin = section.right_margin = Pt(54)

    title = doc.add_paragraph()
    title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = title.add_run(doc_type.upper())
    run.bold = True
    run.font.name = "Times New Roman"
    run.font.size = Pt(16)

    for line in _clean_lines(text):
        p = doc.add_paragraph()
        p.paragraph_format.space_after = Pt(8)
        r = p.add_run(line)
        r.font.name = "Times New Roman"
        r.font.size = Pt(11)

    footer = section.footer.paragraphs[0]
    footer.alignment = WD_ALIGN_PARAGRAPH.CENTER
    footer.add_run("LegalEase - AI-generated draft").italic = True

    buffer = BytesIO()
    doc.save(buffer)
    return buffer.getvalue()


class LegalPDF(FPDF):
    def footer(self):
        self.set_y(-15)
        self.set_font("Times", "I", 8)
        self.cell(0, 10, "LegalEase - AI-generated draft", align="C")


def format_pdf(text: str, doc_type: str) -> bytes:
    pdf = LegalPDF()
    pdf.set_auto_page_break(auto=True, margin=18)
    pdf.add_page()
    pdf.set_font("Times", "B", 16)
    pdf.multi_cell(0, 10, doc_type.upper(), align="C")
    pdf.ln(5)
    pdf.set_font("Times", "", 11)

    for line in _clean_lines(text):
        if re.match(r"^(\d+[.)]|ARTICLE\s+\d+)", line, re.I):
            pdf.set_font("Times", "B", 11)
            pdf.multi_cell(0, 7, line)
            pdf.set_font("Times", "", 11)
        else:
            pdf.multi_cell(0, 6, line)
            pdf.ln(2)

    return bytes(pdf.output())
