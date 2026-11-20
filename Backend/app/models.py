"""Здесь нарисованы все «ящики» в базе: пользователи, заметки, задачи, календарь.
Каждый класс — это одна таблица; поля — что лежит в ячейках (имя, текст, дата).
Стрелочки Foreign Key говорят: «эта заметка принадлежит вот этому человеку».
Программа не пишет SQL руками каждый раз — она думает объектами, как в игре с инвентарём.
"""
import uuid
# datetime — колонки created_at, due_at и т.д.
from datetime import datetime

# Типы колонок SQLAlchemy и ограничения (FK, UNIQUE, CHECK)
from sqlalchemy import (
    BigInteger,  # file_size вложений
    Boolean,  # флаги is_done, is_deleted
    CheckConstraint,  # например priority 1–3 у todos
    DateTime,  # метки времени с timezone
    ForeignKey,  # связь на users.id, notes.id
    SmallInteger,  # priority задачи
    String,  # email, title
    Text,  # длинный content, token_hash
    UniqueConstraint,  # уникальные пары в note_links, sync_checkpoints
    func,  # server_default=func.now() на стороне БД
)
# ARRAY(Text) — массив тегов в PostgreSQL
from sqlalchemy.dialects.postgresql import ARRAY, UUID
# Mapped/mapped_column — стиль объявления моделей SQLAlchemy 2.0; relationship — ORM-связи
from sqlalchemy.orm import Mapped, mapped_column, relationship

# Общий DeclarativeBase из db.py
from app.db import Base


# Таблица users — учётные записи
class User(Base):
    __tablename__ = "users"  # имя таблицы в PostgreSQL

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)  # PK UUID
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)  # логин, уникальный
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)  # bcrypt/argon, не plaintext
    display_name: Mapped[str | None] = mapped_column(String(100))  # отображаемое имя, optional
    role: Mapped[str] = mapped_column(String(20), default="user")  # user | admin
    is_email_verified: Mapped[bool] = mapped_column(Boolean, default=False)  # верификация почты
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())  # создан
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())  # изменён
    deleted_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))  # soft delete пользователя


# Refresh-токены для продления сессии без повторного логина
class RefreshToken(Base):
    __tablename__ = "refresh_tokens"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)  # PK
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))  # владелец
    token_hash: Mapped[str] = mapped_column(Text, unique=True, nullable=False)  # хеш токена, не сам токен
    expires_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)  # срок годности
    revoked: Mapped[bool] = mapped_column(Boolean, default=False)  # отозван при logout/компрометации
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())  # когда выдан


# Заметки пользователя (основная сущность блока notes)
class Note(Base):
    __tablename__ = "notes"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)  # PK
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))  # владелец
    title: Mapped[str] = mapped_column(String(500), default="Без названия")  # заголовок
    content: Mapped[str] = mapped_column(Text, default="")  # markdown/текст
    tags: Mapped[list[str]] = mapped_column(ARRAY(Text), default=list)  # теги PG-массивом
    is_deleted: Mapped[bool] = mapped_column(Boolean, default=False)  # в корзине
    deleted_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))  # когда удалена
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    version: Mapped[int] = mapped_column(default=1)  # для оптимистичной синхронизации

    outgoing_links: Mapped[list["NoteLink"]] = relationship(  # ссылки ИЗ этой заметки
        foreign_keys="NoteLink.source_note_id", back_populates="source_note"
    )
    incoming_links: Mapped[list["NoteLink"]] = relationship(  # ссылки НА эту заметку (wiki)
        foreign_keys="NoteLink.target_note_id", back_populates="target_note"
    )


# Рёбра графа wiki-ссылок между заметками
class NoteLink(Base):
    __tablename__ = "note_links"
    __table_args__ = (UniqueConstraint("source_note_id", "target_note_id", name="uq_note_link"),)  # без дублей пары

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    source_note_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("notes.id", ondelete="CASCADE"))  # откуда
    target_note_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("notes.id", ondelete="CASCADE"))  # куда
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    source_note: Mapped[Note] = relationship(foreign_keys=[source_note_id], back_populates="outgoing_links")
    target_note: Mapped[Note] = relationship(foreign_keys=[target_note_id], back_populates="incoming_links")


# Файлы, прикреплённые к заметке
class NoteAttachment(Base):
    __tablename__ = "note_attachments"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    note_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("notes.id", ondelete="CASCADE"))  # родительская заметка
    file_name: Mapped[str] = mapped_column(String(500))  # исходное имя файла
    file_path: Mapped[str] = mapped_column(String(1000))  # путь на диске в uploads
    mime_type: Mapped[str] = mapped_column(String(100))  # image/png и т.д.
    file_size: Mapped[int] = mapped_column(BigInteger, default=0)  # размер в байтах
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())


# События календаря
class CalendarEvent(Base):
    __tablename__ = "calendar_events"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    linked_note_id: Mapped[uuid.UUID | None] = mapped_column(ForeignKey("notes.id", ondelete="SET NULL"))  # опц. связь
    title: Mapped[str] = mapped_column(String(500))
    description: Mapped[str | None] = mapped_column(Text)
    start_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))  # начало
    end_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))  # конец
    color: Mapped[str] = mapped_column(String(20), default="#4A90D9")  # цвет в UI
    all_day: Mapped[bool] = mapped_column(Boolean, default=False)  # событие на весь день
    is_deleted: Mapped[bool] = mapped_column(Boolean, default=False)  # мягкое удаление
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    version: Mapped[int] = mapped_column(default=1)


# Задачи (todos)
class Todo(Base):
    __tablename__ = "todos"
    __table_args__ = (CheckConstraint("priority BETWEEN 1 AND 3", name="chk_todo_priority"),)  # 1 низкий, 3 высокий

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    linked_note_id: Mapped[uuid.UUID | None] = mapped_column(ForeignKey("notes.id", ondelete="SET NULL"))
    title: Mapped[str] = mapped_column(String(500))
    description: Mapped[str | None] = mapped_column(Text)
    is_done: Mapped[bool] = mapped_column(Boolean, default=False)  # выполнена
    priority: Mapped[int] = mapped_column(SmallInteger, default=2)  # 1–3
    due_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))  # дедлайн
    is_deleted: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    version: Mapped[int] = mapped_column(default=1)


# Метка «последняя синхронизация» для устройства пользователя (модуль sync)
class SyncCheckpoint(Base):
    __tablename__ = "sync_checkpoints"
    __table_args__ = (UniqueConstraint("user_id", "device_id", name="uq_sync_device"),)  # одно устройство — одна запись

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    device_id: Mapped[str] = mapped_column(String(200))  # идентификатор клиента/браузера
    last_sync: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())  # время sync