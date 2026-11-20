"""Это проверяльщик входящих и исходящих писем в формате JSON.
Если фронт прислал не email, а «абракадабра», схема скажет «так нельзя» до базы.
CamelModel переводит имена полей в стиль, понятный JavaScript (userId вместо user_id).
Готовит красивые ответы для экрана: токены, заметки, задачи — всё по шаблону.
"""
from datetime import datetime
# UUID в Pydantic-моделях (id, foreign keys в JSON)
from uuid import UUID

# BaseModel — схема валидации; EmailStr — формат email; Field — alias и дефолты
from pydantic import BaseModel, ConfigDict, EmailStr, Field
# to_camel — snake_case полей Python → camelCase в JSON для фронта
from pydantic.alias_generators import to_camel


# Базовый DTO: JSON на фронте в camelCase, чтение из ORM через from_attributes
class CamelModel(BaseModel):
    model_config = ConfigDict(
        alias_generator=to_camel,  # user_id → userId в JSON
        populate_by_name=True,  # принимать и snake_case, и camelCase на входе
        from_attributes=True,  # Note(...) → NoteDto.model_validate(orm_note)
        serialize_by_alias=True,  # в ответе отдавать алиасы (camelCase)
    )


# --- Auth: регистрация, логин, ответ с токенами ---

# Тело POST /auth/register
class RegisterRequest(BaseModel):
    email: EmailStr  # валидный email
    password: str  # пароль (длина проверяется в роутере при необходимости)
    display_name: str | None = Field(None, alias="displayName")  # имя с фронта как displayName

    model_config = ConfigDict(populate_by_name=True)  # можно передать display_name или displayName


# Тело POST /auth/login
class LoginRequest(BaseModel):
    email: EmailStr
    password: str


# Ответ после login/register: токены + краткие данные пользователя
class AuthResponse(CamelModel):
    access_token: str  # JWT access
    refresh_token: str  # opaque refresh (в БД хеш)
    user_id: UUID
    display_name: str | None
    role: str = "user"  # роль по умолчанию


# Профиль GET /users/me
class UserProfileDto(CamelModel):
    id: UUID
    email: str
    display_name: str | None
    role: str
    created_at: datetime


# Строка пользователя в админ-таблице
class AdminUserDto(CamelModel):
    id: UUID
    email: str
    display_name: str | None
    role: str
    created_at: datetime
    is_deleted: bool  # есть deleted_at у User


# Сводные счётчики для админ-дашборда
class AdminStatsDto(CamelModel):
    users: int
    notes: int
    todos: int
    events: int


# PATCH роли пользователя админом
class SetRoleRequest(BaseModel):
    role: str  # user | admin


# --- Notes: заметки, wiki-ссылки, поиск ---

# Одна связь в графе wiki [[Note Title]]
class NoteLinkDto(CamelModel):
    note_id: UUID
    title: str


# Полная заметка для страницы детали
class NoteDto(CamelModel):
    id: UUID
    title: str
    content: str
    tags: list[str]
    created_at: datetime
    updated_at: datetime
    outgoing_links: list[NoteLinkDto]  # куда ссылается
    incoming_links: list[NoteLinkDto]  # кто ссылается сюда


# Элемент списка заметок (без content — экономия трафика)
class NoteListItemDto(CamelModel):
    id: UUID
    title: str
    tags: list[str]
    updated_at: datetime


# POST создание заметки
class CreateNoteRequest(BaseModel):
    title: str
    content: str
    tags: list[str] | None = None  # опционально


# PUT/PATCH обновление — все поля optional
class UpdateNoteRequest(BaseModel):
    title: str | None = None
    content: str | None = None
    tags: list[str] | None = None


# Результат полнотекстового поиска
class SearchResultDto(CamelModel):
    id: UUID
    title: str
    snippet: str  # фрагмент с подсветкой/контекстом
    rank: float  # релевантность


# --- Todos ---

# Задача в ответе API
class TodoDto(CamelModel):
    id: UUID
    title: str
    description: str | None
    is_done: bool
    priority: int
    due_at: datetime | None
    linked_note_id: UUID | None
    created_at: datetime
    updated_at: datetime


# POST новая задача; dueAt/linkedNoteId — camelCase с фронта
class CreateTodoRequest(BaseModel):
    title: str
    description: str | None = None
    priority: int = 2  # средний по умолчанию
    due_at: datetime | None = Field(None, alias="dueAt")
    linked_note_id: UUID | None = Field(None, alias="linkedNoteId")

    model_config = ConfigDict(populate_by_name=True)


# PATCH задачи — частичное обновление
class UpdateTodoRequest(BaseModel):
    title: str | None = None
    description: str | None = None
    is_done: bool | None = Field(None, alias="isDone")
    priority: int | None = None
    due_at: datetime | None = Field(None, alias="dueAt")
    linked_note_id: UUID | None = Field(None, alias="linkedNoteId")

    model_config = ConfigDict(populate_by_name=True)


# --- Calendar ---

# Событие в календаре (ответ)
class CalendarEventDto(CamelModel):
    id: UUID
    title: str
    description: str | None
    start_at: datetime
    end_at: datetime
    color: str
    all_day: bool
    linked_note_id: UUID | None


# POST событие; startAt/endAt обязательны с фронта
class CreateEventRequest(BaseModel):
    title: str
    description: str | None = None
    start_at: datetime = Field(alias="startAt")
    end_at: datetime = Field(alias="endAt")
    color: str | None = None
    all_day: bool = Field(False, alias="allDay")
    linked_note_id: UUID | None = Field(None, alias="linkedNoteId")

    model_config = ConfigDict(populate_by_name=True)


# PATCH событие
class UpdateEventRequest(BaseModel):
    title: str | None = None
    description: str | None = None
    start_at: datetime | None = Field(None, alias="startAt")
    end_at: datetime | None = Field(None, alias="endAt")
    color: str | None = None
    all_day: bool | None = Field(None, alias="allDay")
    linked_note_id: UUID | None = Field(None, alias="linkedNoteId")

    model_config = ConfigDict(populate_by_name=True)