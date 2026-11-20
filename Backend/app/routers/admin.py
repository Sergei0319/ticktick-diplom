"""Это кабинет директора: только для взрослого с табличкой admin.
Показывает, сколько в школе учеников, заметок, задач и событий — как счётчики на стене.
Можно посмотреть всех пользователей, сменить кому роль «учитель» (admin) или «ученик» (user).
Нельзя удалить себя и нельзя забыть себе права — иначе школа останется без директора.
"""
import uuid
from datetime import datetime, timezone

from fastapi import APIRouter, HTTPException, status

from app.deps import AdminUser, DbSession
from app.models import CalendarEvent, Note, Todo, User
from app.schemas import AdminStatsDto, AdminUserDto, SetRoleRequest

router = APIRouter(prefix="/api/admin", tags=["admin"])


@router.get("/stats", response_model=AdminStatsDto)
def stats(db: DbSession, _: AdminUser):
    return AdminStatsDto(
        users=db.query(User).filter(User.deleted_at.is_(None)).count(),
        notes=db.query(Note).filter(Note.is_deleted.is_(False)).count(),
        todos=db.query(Todo).filter(Todo.is_deleted.is_(False)).count(),
        events=db.query(CalendarEvent).filter(CalendarEvent.is_deleted.is_(False)).count(),
    )


@router.get("/users", response_model=list[AdminUserDto])
def list_users(db: DbSession, _: AdminUser):
    users = db.query(User).order_by(User.created_at.desc()).all()
    return [
        AdminUserDto(
            id=u.id,
            email=u.email,
            display_name=u.display_name,
            role=u.role or "user",
            created_at=u.created_at,
            is_deleted=u.deleted_at is not None,
        )
        for u in users
    ]


@router.patch("/users/{user_id}/role", response_model=AdminUserDto)
def set_role(user_id: uuid.UUID, req: SetRoleRequest, db: DbSession, admin: AdminUser):
    if req.role not in ("user", "admin"):
        raise HTTPException(status.HTTP_400_BAD_REQUEST, detail={"message": "role: user или admin"})
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status.HTTP_404_NOT_FOUND)
    if user.id == admin.id and req.role != "admin":
        raise HTTPException(status.HTTP_400_BAD_REQUEST, detail={"message": "Нельзя снять роль admin с себя"})
    user.role = req.role
    user.updated_at = datetime.now(timezone.utc)
    db.commit()
    db.refresh(user)
    return AdminUserDto(
        id=user.id,
        email=user.email,
        display_name=user.display_name,
        role=user.role,
        created_at=user.created_at,
        is_deleted=user.deleted_at is not None,
    )


@router.delete("/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def soft_delete_user(user_id: uuid.UUID, db: DbSession, admin: AdminUser):
    if user_id == admin.id:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, detail={"message": "Нельзя удалить себя"})
    user = db.query(User).filter(User.id == user_id, User.deleted_at.is_(None)).first()
    if not user:
        raise HTTPException(status.HTTP_404_NOT_FOUND)
    user.deleted_at = datetime.now(timezone.utc)
    db.commit()