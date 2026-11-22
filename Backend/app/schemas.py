"""JSON, который API принимает и отдаёт.
Pydantic проверяет поля и переводит имена
в camelCase для фронтенда.
Пароль и хеш токена в ответы не попадают.
"""

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, EmailStr, Field
from pydantic.alias_generators import to_camel



class CamelModel(BaseModel):
    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,
        from_attributes=True,
        serialize_by_alias=True,
    )





class RegisterRequest(BaseModel):
    email: EmailStr
    password: str
    display_name: str | None = Field(None, alias="displayName")

    model_config = ConfigDict(populate_by_name=True)



class LoginRequest(BaseModel):
    email: EmailStr
    password: str



class AuthResponse(CamelModel):
    access_token: str
    refresh_token: str
    user_id: UUID
    display_name: str | None
    role: str = "user"



class UserProfileDto(CamelModel):
    id: UUID
    email: str
    display_name: str | None
    role: str
    created_at: datetime



class AdminUserDto(CamelModel):
    id: UUID
    email: str
    display_name: str | None
    role: str
    created_at: datetime
    is_deleted: bool



class AdminStatsDto(CamelModel):
    users: int
    notes: int
    todos: int
    events: int



class SetRoleRequest(BaseModel):
    role: str





class NoteLinkDto(CamelModel):
    note_id: UUID
    title: str



class NoteDto(CamelModel):
    id: UUID
    title: str
    content: str
    tags: list[str]
    created_at: datetime
    updated_at: datetime
    outgoing_links: list[NoteLinkDto]
    incoming_links: list[NoteLinkDto]



class NoteListItemDto(CamelModel):
    id: UUID
    title: str
    tags: list[str]
    updated_at: datetime



class CreateNoteRequest(BaseModel):
    title: str
    content: str
    tags: list[str] | None = None



class UpdateNoteRequest(BaseModel):
    title: str | None = None
    content: str | None = None
    tags: list[str] | None = None



class SearchResultDto(CamelModel):
    id: UUID
    title: str
    snippet: str
    rank: float





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



class CreateTodoRequest(BaseModel):
    title: str
    description: str | None = None
    priority: int = 2
    due_at: datetime | None = Field(None, alias="dueAt")
    linked_note_id: UUID | None = Field(None, alias="linkedNoteId")

    model_config = ConfigDict(populate_by_name=True)



class UpdateTodoRequest(BaseModel):
    title: str | None = None
    description: str | None = None
    is_done: bool | None = Field(None, alias="isDone")
    priority: int | None = None
    due_at: datetime | None = Field(None, alias="dueAt")
    linked_note_id: UUID | None = Field(None, alias="linkedNoteId")

    model_config = ConfigDict(populate_by_name=True)





class CalendarEventDto(CamelModel):
    id: UUID
    title: str
    description: str | None
    start_at: datetime
    end_at: datetime
    color: str
    all_day: bool
    linked_note_id: UUID | None



class CreateEventRequest(BaseModel):
    title: str
    description: str | None = None
    start_at: datetime = Field(alias="startAt")
    end_at: datetime = Field(alias="endAt")
    color: str | None = None
    all_day: bool = Field(False, alias="allDay")
    linked_note_id: UUID | None = Field(None, alias="linkedNoteId")

    model_config = ConfigDict(populate_by_name=True)



class UpdateEventRequest(BaseModel):
    title: str | None = None
    description: str | None = None
    start_at: datetime | None = Field(None, alias="startAt")
    end_at: datetime | None = Field(None, alias="endAt")
    color: str | None = None
    all_day: bool | None = Field(None, alias="allDay")
    linked_note_id: UUID | None = Field(None, alias="linkedNoteId")

    model_config = ConfigDict(populate_by_name=True)