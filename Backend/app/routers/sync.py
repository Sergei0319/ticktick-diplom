from datetime import datetime, timezone

from fastapi import APIRouter, Query

from app.deps import DbSession, UserId
from app.models import CalendarEvent, Note, SyncCheckpoint, Todo

router = APIRouter(prefix="/api/sync", tags=["sync"])


@router.get("")
def pull(
    db: DbSession,
    user_id: UserId,
    since: datetime | None = Query(None),
    device_id: str = Query("default", alias="device_id"),
):
    from_dt = since or datetime.min.replace(tzinfo=timezone.utc)

    notes = (
        db.query(Note)
        .filter(Note.user_id == user_id, Note.updated_at > from_dt)
        .all()
    )
    events = (
        db.query(CalendarEvent)
        .filter(CalendarEvent.user_id == user_id, CalendarEvent.updated_at > from_dt)
        .all()
    )
    todos = (
        db.query(Todo)
        .filter(Todo.user_id == user_id, Todo.updated_at > from_dt)
        .all()
    )

    checkpoint = (
        db.query(SyncCheckpoint)
        .filter(SyncCheckpoint.user_id == user_id, SyncCheckpoint.device_id == device_id)
        .first()
    )
    now = datetime.now(timezone.utc)
    if checkpoint is None:
        db.add(SyncCheckpoint(user_id=user_id, device_id=device_id, last_sync=now))
    else:
        checkpoint.last_sync = now
    db.commit()

    def note_row(n: Note):
        return {
            "id": n.id,
            "title": n.title,
            "content": n.content,
            "tags": n.tags,
            "isDeleted": n.is_deleted,
            "deletedAt": n.deleted_at,
            "createdAt": n.created_at,
            "updatedAt": n.updated_at,
        }

    def event_row(e: CalendarEvent):
        return {
            "id": e.id,
            "title": e.title,
            "description": e.description,
            "startAt": e.start_at,
            "endAt": e.end_at,
            "color": e.color,
            "allDay": e.all_day,
            "linkedNoteId": e.linked_note_id,
            "isDeleted": e.is_deleted,
            "createdAt": e.created_at,
            "updatedAt": e.updated_at,
        }

    def todo_row(t: Todo):
        return {
            "id": t.id,
            "title": t.title,
            "description": t.description,
            "isDone": t.is_done,
            "priority": t.priority,
            "dueAt": t.due_at,
            "linkedNoteId": t.linked_note_id,
            "isDeleted": t.is_deleted,
            "createdAt": t.created_at,
            "updatedAt": t.updated_at,
        }

    return {
        "syncedAt": now,
        "notes": [note_row(n) for n in notes],
        "events": [event_row(e) for e in events],
        "todos": [todo_row(t) for t in todos],
    }