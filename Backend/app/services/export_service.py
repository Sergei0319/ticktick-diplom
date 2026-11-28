import re
from io import BytesIO
from pathlib import Path

from docx import Document
from fpdf import FPDF
from fpdf.enums import XPos, YPos

from app.models import Note

INLINE_MD = [
    (re.compile(r"\*\*(.+?)\*\*"), r"\1"),
    (re.compile(r"\*(.+?)\*"), r"\1"),
    (re.compile(r"~~(.+?)~~"), r"\1"),
    (re.compile(r"`(.+?)`"), r"\1"),
    (re.compile(r"\[\[(.+?)\]\]"), r"\1"),
    (re.compile(r"\[(.+?)\]\(.+?\)"), r"\1"),
]

PDF_FONT = "ExportFont"


# Убирает markdown-разметку из строки
def _strip_md(line: str) -> str:
    s = line
    for pat, repl in INLINE_MD:
        s = pat.sub(repl, s)
    return s


# Регистрирует шрифты для PDF с кириллицей
def _pdf_font_files() -> tuple[Path, Path]:
    pairs = [
        (
            Path("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"),
            Path("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"),
        ),
        (
            Path("C:/Windows/Fonts/arial.ttf"),
            Path("C:/Windows/Fonts/arialbd.ttf"),
        ),
        (
            Path("C:/Windows/Fonts/DejaVuSans.ttf"),
            Path("C:/Windows/Fonts/DejaVuSans-Bold.ttf"),
        ),
    ]
    for regular, bold in pairs:
        if regular.is_file():
            return regular, bold if bold.is_file() else regular
    raise RuntimeError("Не найден TTF-шрифт с поддержкой кириллицы для PDF")


# Собирает PDF-документ из абзацев
def _make_pdf() -> FPDF:
    regular, bold = _pdf_font_files()
    pdf = FPDF()
    pdf.add_font(PDF_FONT, "", str(regular))
    pdf.add_font(PDF_FONT, "B", str(bold))
    return pdf


# Экспорт заметки в DOCX
def export_docx(note: Note) -> bytes:
    doc = Document()
    doc.add_heading(note.title, level=1)
    if note.tags:
        doc.add_paragraph(f"Теги: {', '.join(note.tags)}")
    doc.add_paragraph(f"Изменено: {note.updated_at:%d.%m.%Y %H:%M}")
    for line in (note.content or "").split("\n"):
        t = line.rstrip()
        if t.startswith("# "):
            doc.add_heading(_strip_md(t[2:]), level=1)
        elif t.startswith("## "):
            doc.add_heading(_strip_md(t[3:]), level=2)
        elif t.startswith("### "):
            doc.add_heading(_strip_md(t[4:]), level=3)
        elif t.startswith("- ") or t.startswith("* "):
            doc.add_paragraph(_strip_md(t[2:]), style="List Bullet")
        elif t.startswith("```"):
            continue
        else:
            doc.add_paragraph(_strip_md(t))
    buf = BytesIO()
    doc.save(buf)
    return buf.getvalue()


# Экспорт заметки в PDF
def export_pdf(note: Note) -> bytes:
    pdf = _make_pdf()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    cell = dict(new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.set_font(PDF_FONT, "B", 18)
    pdf.multi_cell(0, 10, note.title, **cell)
    pdf.set_font(PDF_FONT, size=10)
    pdf.multi_cell(0, 6, f"Изменено: {note.updated_at:%d.%m.%Y %H:%M}", **cell)
    if note.tags:
        pdf.multi_cell(0, 6, f"Теги: {', '.join(note.tags)}", **cell)
    pdf.ln(4)
    pdf.set_font(PDF_FONT, size=11)
    for line in (note.content or "").split("\n"):
        t = line.rstrip()
        if not t:
            pdf.ln(4)
            continue
        if t.startswith("```"):
            continue
        if t.startswith("# "):
            pdf.set_font(PDF_FONT, "B", 14)
            pdf.multi_cell(0, 8, _strip_md(t[2:]), **cell)
            pdf.set_font(PDF_FONT, size=11)
        elif t.startswith("## "):
            pdf.set_font(PDF_FONT, "B", 12)
            pdf.multi_cell(0, 7, _strip_md(t[3:]), **cell)
            pdf.set_font(PDF_FONT, size=11)
        elif t.startswith("- ") or t.startswith("* "):
            pdf.multi_cell(0, 6, "  • " + _strip_md(t[2:]), **cell)
        else:
            pdf.multi_cell(0, 6, _strip_md(t), **cell)
    return bytes(pdf.output())
