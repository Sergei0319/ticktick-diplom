"""События календаря текущего пользователя.
Список можно сузить по датам.
Событие создаётся и меняется,
удаление только скрывает запись.
"""

import uuid
from datetime import datetime, timezone

from fastapi import APIRouter, HTTPException, Query, status

from app.deps import DbSession, UserId
from app.models import CalendarEvent
from app.schemas import CalendarEventDto, CreateEventRequest, UpdateEventRequest

router = APIRouter(prefix="/api/calendar", tags=["calendar"])


def _map(e: CalendarEvent) -> CalendarEventDto:
    return CalendarEventDto(
        id=e.id,
        title=e.title,
        description=e.description,
        start_at=e.start_at,
        end_at=e.end_at,
        color=e.color,
        all_day=e.all_day,
        linked_note_id=e.linked_note_id,
    )


@router.get("", response_model=list[CalendarEventDto])
def get_events(
    db: DbSession,
    user_id: UserId,
    from_: datetime | None = Query(None, alias="from"),
    to: datetime | None = Query(None),
):
    q = db.query(CalendarEvent).filter(CalendarEvent.user_id == user_id, CalendarEvent.is_deleted.is_(False))
    if from_ is not None:
        q = q.filter(CalendarEvent.end_at >= from_)
    if to is not None:
        q = q.filter(CalendarEvent.start_at <= to)
    events = q.order_by(CalendarEvent.start_at).all()
    return [_map(e) for e in events]


@router.get("/{event_id}", response_model=CalendarEventDto)
def get_one(event_id: uuid.UUID, db: DbSession, user_id: UserId):
    e = (
        db.query(CalendarEvent)
        .filter(CalendarEvent.id == event_id, CalendarEvent.user_id == user_id, CalendarEvent.is_deleted.is_(False))
        .first()
    )
    if not e:
        raise HTTPException(status.HTTP_404_NOT_FOUND)
    return _map(e)


@router.post("", response_model=CalendarEventDto, status_code=status.HTTP_201_CREATED)
def create(req: CreateEventRequest, db: DbSession, user_id: UserId):
    if req.end_at < req.start_at:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, detail={"message": "end_at не может быть раньше start_at"})
    ev = CalendarEvent(
        user_id=user_id,
        title=req.title,
        description=req.description,
        start_at=req.start_at,
        end_at=req.end_at,
        color=req.color or "#4A90D9",
        all_day=req.all_day,
        linked_note_id=req.linked_note_id,
    )
    db.add(ev)
    db.commit()
    db.refresh(ev)
    return _map(ev)


@router.put("/{event_id}", response_model=CalendarEventDto)
def update(event_id: uuid.UUID, req: UpdateEventRequest, db: DbSession, user_id: UserId):
    ev = (
        db.query(CalendarEvent)
        .filter(CalendarEvent.id == event_id, CalendarEvent.user_id == user_id, CalendarEvent.is_deleted.is_(False))
        .first()
    )
    if not ev:
        raise HTTPException(status.HTTP_404_NOT_FOUND)
    if req.title is not None:
        ev.title = req.title
    if req.description is not None:
        ev.description = req.description
    if req.start_at is not None:
        ev.start_at = req.start_at
    if req.end_at is not None:
        ev.end_at = req.end_at
    if req.color is not None:
        ev.color = req.color
    if req.all_day is not None:
        ev.all_day = req.all_day
    if req.linked_note_id is not None:
        ev.linked_note_id = req.linked_note_id
    ev.updated_at = datetime.now(timezone.utc)
    db.commit()
    db.refresh(ev)
    return _map(ev)


@router.delete("/{event_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete(event_id: uuid.UUID, db: DbSession, user_id: UserId):
    ev = (
        db.query(CalendarEvent)
        .filter(CalendarEvent.id == event_id, CalendarEvent.user_id == user_id, CalendarEvent.is_deleted.is_(False))
        .first()
    )
    if not ev:
        raise HTTPException(status.HTTP_404_NOT_FOUND)
    ev.is_deleted = True
    ev.updated_at = datetime.now(timezone.utc)
    db.commit()