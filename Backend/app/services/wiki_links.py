"""Это детектив ссылок внутри заметки.
Ищет в тексте [[название другой заметки]] и связывает тетрадки между собой.
Если ссылку убрали из текста — связь в базе тоже исчезает.
Вызывается, когда сохраняешь заметку, чтобы граф ссылок не врал.
"""
import re
import uuid

from sqlalchemy.orm import Session

from app.models import Note, NoteLink

WIKI_LINK = re.compile(r"\[\[(.+?)\]\]")


def sync_links(db: Session, note: Note, user_id: uuid.UUID) -> None:
    titles = list(
        dict.fromkeys(
            m.group(1).strip()
            for m in WIKI_LINK.finditer(note.content or "")
            if m.group(1).strip()
        )
    )
    lower_titles = {t.lower() for t in titles}
    targets = (
        db.query(Note)
        .filter(Note.user_id == user_id, Note.is_deleted.is_(False))
        .all()
    )
    target_notes = [n for n in targets if n.title.lower() in lower_titles]

    db.query(NoteLink).filter(NoteLink.source_note_id == note.id).delete()
    for target in target_notes:
        if target.id == note.id:
            continue
        db.add(NoteLink(source_note_id=note.id, target_note_id=target.id))
    db.commit()