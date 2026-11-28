import re
import uuid
from urllib.parse import quote

from fastapi import APIRouter, HTTPException
from fastapi.responses import Response

from app.deps import DbSession, UserId
from app.models import Note
from app.services import export_service

router = APIRouter(prefix="/api/notes/{note_id}/export", tags=["export"])


# Очищает имя файла от недопустимых символов
def _safe_name(title: str) -> str:
    clean = re.sub(r'[<>:"/\\|?*]', "", title).replace(" ", "_").strip(".")
    return clean or "note"


# Собирает заголовок Content-Disposition для скачивания
def _attachment_disposition(title: str, ext: str) -> str:
    """HTTP-заголовки только latin-1; кириллицу кодируем через filename* (RFC 5987)."""
    base = _safe_name(title)
    ascii_fallback = re.sub(r"[^\w.\-]", "_", base.encode("ascii", "ignore").decode()) or "note"
    encoded = quote(f"{base}.{ext}", safe="")
    return f"attachment; filename=\"{ascii_fallback}.{ext}\"; filename*=UTF-8''{encoded}"


# Экспорт заметки в DOCX
@router.get("/docx")
def export_docx(note_id: uuid.UUID, db: DbSession, user_id: UserId):
    note = (
        db.query(Note)
        .filter(Note.id == note_id, Note.user_id == user_id, Note.is_deleted.is_(False))
        .first()
    )
    if not note:
        raise HTTPException(status_code=404)
    data = export_service.export_docx(note)
    return Response(
        content=data,
        media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        headers={"Content-Disposition": _attachment_disposition(note.title, "docx")},
    )


# Экспорт заметки в PDF
@router.get("/pdf")
def export_pdf(note_id: uuid.UUID, db: DbSession, user_id: UserId):
    note = (
        db.query(Note)
        .filter(Note.id == note_id, Note.user_id == user_id, Note.is_deleted.is_(False))
        .first()
    )
    if not note:
        raise HTTPException(status_code=404)
    data = export_service.export_pdf(note)
    return Response(
        content=data,
        media_type="application/pdf",
        headers={"Content-Disposition": _attachment_disposition(note.title, "pdf")},
    )
