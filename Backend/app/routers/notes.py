"""Заметки текущего пользователя: список, фильтр
по тегу, поиск, корзина, правка и файл.
После сохранения заново собирает вики-ссылки [[название]].
"""

import os
import uuid
from datetime import datetime, timezone

from fastapi import APIRouter, File, HTTPException, Query, UploadFile, status
from sqlalchemy import text
from sqlalchemy.orm import joinedload

from app.config import settings
from app.deps import DbSession, UserId
from app.models import Note, NoteAttachment, NoteLink
from app.schemas import CreateNoteRequest, NoteDto, NoteLinkDto, NoteListItemDto, SearchResultDto, UpdateNoteRequest
from app.services import wiki_links

router = APIRouter(prefix="/api/notes", tags=["notes"])


def _map_note(note: Note) -> NoteDto:
    return NoteDto(
        id=note.id,
        title=note.title,
        content=note.content,
        tags=note.tags or [],
        created_at=note.created_at,
        updated_at=note.updated_at,
        outgoing_links=[
            NoteLinkDto(note_id=l.target_note_id, title=l.target_note.title if l.target_note else "")
            for l in (note.outgoing_links or [])
        ],
        incoming_links=[
            NoteLinkDto(note_id=l.source_note_id, title=l.source_note.title if l.source_note else "")
            for l in (note.incoming_links or [])
        ],
    )


@router.get("", response_model=list[NoteListItemDto])
def get_all(db: DbSession, user_id: UserId, tag: str | None = None):
    q = db.query(Note).filter(Note.user_id == user_id, Note.is_deleted.is_(False))
    if tag:
        q = q.filter(Note.tags.contains([tag]))
    notes = q.order_by(Note.updated_at.desc()).all()
    return [
        NoteListItemDto(id=n.id, title=n.title, tags=n.tags or [], updated_at=n.updated_at) for n in notes
    ]


@router.get("/trash", response_model=list[NoteListItemDto])
def get_trash(db: DbSession, user_id: UserId):
    notes = (
        db.query(Note)
        .filter(Note.user_id == user_id, Note.is_deleted.is_(True))
        .order_by(Note.deleted_at.desc())
        .all()
    )
    return [
        NoteListItemDto(id=n.id, title=n.title, tags=n.tags or [], updated_at=n.updated_at) for n in notes
    ]


@router.get("/search", response_model=list[SearchResultDto])
def search(db: DbSession, user_id: UserId, q: str = Query(...)):
    if not q.strip():
        raise HTTPException(status.HTTP_400_BAD_REQUEST, detail={"message": "Параметр q обязателен"})
    rows = db.execute(
        text("SELECT id, title, snippet, rank FROM search_notes(:q, :uid)"),
        {"q": q, "uid": str(user_id)},
    ).mappings()
    return [SearchResultDto(**row) for row in rows]


@router.get("/{note_id}", response_model=NoteDto)
def get_one(note_id: uuid.UUID, db: DbSession, user_id: UserId):
    note = (
        db.query(Note)
        .options(
            joinedload(Note.outgoing_links).joinedload(NoteLink.target_note),
            joinedload(Note.incoming_links).joinedload(NoteLink.source_note),
        )
        .filter(Note.id == note_id, Note.user_id == user_id, Note.is_deleted.is_(False))
        .first()
    )
    if not note:
        raise HTTPException(status.HTTP_404_NOT_FOUND)
    return _map_note(note)


@router.post("", response_model=NoteDto, status_code=status.HTTP_201_CREATED)
def create(req: CreateNoteRequest, db: DbSession, user_id: UserId):
    note = Note(user_id=user_id, title=req.title, content=req.content, tags=req.tags or [])
    db.add(note)
    db.commit()
    db.refresh(note)
    wiki_links.sync_links(db, note, user_id)
    db.refresh(note)
    return _map_note(note)


@router.put("/{note_id}", response_model=NoteDto)
def update(note_id: uuid.UUID, req: UpdateNoteRequest, db: DbSession, user_id: UserId):
    note = (
        db.query(Note)
        .filter(Note.id == note_id, Note.user_id == user_id, Note.is_deleted.is_(False))
        .first()
    )
    if not note:
        raise HTTPException(status.HTTP_404_NOT_FOUND)
    if req.title is not None:
        note.title = req.title
    if req.content is not None:
        note.content = req.content
    if req.tags is not None:
        note.tags = req.tags
    note.updated_at = datetime.now(timezone.utc)
    db.commit()
    wiki_links.sync_links(db, note, user_id)
    db.refresh(note)
    return _map_note(note)


@router.delete("/{note_id}", status_code=status.HTTP_204_NO_CONTENT)
def soft_delete(note_id: uuid.UUID, db: DbSession, user_id: UserId):
    note = (
        db.query(Note)
        .filter(Note.id == note_id, Note.user_id == user_id, Note.is_deleted.is_(False))
        .first()
    )
    if not note:
        raise HTTPException(status.HTTP_404_NOT_FOUND)
    note.is_deleted = True
    note.deleted_at = datetime.now(timezone.utc)
    db.commit()


@router.post("/{note_id}/restore", response_model=NoteDto)
def restore(note_id: uuid.UUID, db: DbSession, user_id: UserId):
    note = (
        db.query(Note)
        .filter(Note.id == note_id, Note.user_id == user_id, Note.is_deleted.is_(True))
        .first()
    )
    if not note:
        raise HTTPException(status.HTTP_404_NOT_FOUND)
    note.is_deleted = False
    note.deleted_at = None
    db.commit()
    db.refresh(note)
    return _map_note(note)


@router.delete("/{note_id}/permanent", status_code=status.HTTP_204_NO_CONTENT)
def hard_delete(note_id: uuid.UUID, db: DbSession, user_id: UserId):
    note = (
        db.query(Note)
        .filter(Note.id == note_id, Note.user_id == user_id, Note.is_deleted.is_(True))
        .first()
    )
    if not note:
        raise HTTPException(status.HTTP_404_NOT_FOUND)
    db.delete(note)
    db.commit()


@router.post("/{note_id}/attachments")
async def upload_attachment(
    note_id: uuid.UUID,
    db: DbSession,
    user_id: UserId,
    file: UploadFile = File(...),
):
    note = (
        db.query(Note)
        .filter(Note.id == note_id, Note.user_id == user_id, Note.is_deleted.is_(False))
        .first()
    )
    if not note:
        raise HTTPException(status.HTTP_404_NOT_FOUND)
    uploads_dir = os.path.join(settings.uploads_dir, str(user_id))
    os.makedirs(uploads_dir, exist_ok=True)
    ext = os.path.splitext(file.filename or "")[1]
    stored_name = f"{uuid.uuid4()}{ext}"
    path = os.path.join(uploads_dir, stored_name)
    data = await file.read()
    with open(path, "wb") as f:
        f.write(data)
    rel = os.path.join(str(user_id), stored_name)
    att = NoteAttachment(
        note_id=note.id,
        file_name=file.filename or stored_name,
        file_path=rel.replace("\\", "/"),
        mime_type=file.content_type or "application/octet-stream",
        file_size=len(data),
    )
    db.add(att)
    db.commit()
    db.refresh(att)
    return {
        "id": att.id,
        "fileName": att.file_name,
        "mimeType": att.mime_type,
        "fileSize": att.file_size,
    }