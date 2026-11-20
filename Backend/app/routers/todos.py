import uuid
from datetime import datetime, timezone

from fastapi import APIRouter, HTTPException, Query, status

from app.deps import DbSession, UserId
from app.models import Todo
from app.schemas import CreateTodoRequest, TodoDto, UpdateTodoRequest

router = APIRouter(prefix="/api/todos", tags=["todos"])


def _map(t: Todo) -> TodoDto:
    return TodoDto(
        id=t.id,
        title=t.title,
        description=t.description,
        is_done=t.is_done,
        priority=t.priority,
        due_at=t.due_at,
        linked_note_id=t.linked_note_id,
        created_at=t.created_at,
        updated_at=t.updated_at,
    )


@router.get("", response_model=list[TodoDto])
def get_all(
    db: DbSession,
    user_id: UserId,
    done: bool | None = Query(None),
    priority: int | None = Query(None),
):
    q = db.query(Todo).filter(Todo.user_id == user_id, Todo.is_deleted.is_(False))
    if done is not None:
        q = q.filter(Todo.is_done == done)
    if priority is not None:
        q = q.filter(Todo.priority == priority)
    todos = q.order_by(Todo.priority, Todo.due_at).all()
    return [_map(t) for t in todos]


@router.get("/overdue", response_model=list[TodoDto])
def get_overdue(db: DbSession, user_id: UserId):
    now = datetime.now(timezone.utc)
    todos = (
        db.query(Todo)
        .filter(
            Todo.user_id == user_id,
            Todo.is_deleted.is_(False),
            Todo.is_done.is_(False),
            Todo.due_at < now,
        )
        .order_by(Todo.due_at)
        .all()
    )
    return [_map(t) for t in todos]


@router.get("/{todo_id}", response_model=TodoDto)
def get_one(todo_id: uuid.UUID, db: DbSession, user_id: UserId):
    t = db.query(Todo).filter(Todo.id == todo_id, Todo.user_id == user_id, Todo.is_deleted.is_(False)).first()
    if not t:
        raise HTTPException(status.HTTP_404_NOT_FOUND)
    return _map(t)


@router.post("", response_model=TodoDto, status_code=status.HTTP_201_CREATED)
def create(req: CreateTodoRequest, db: DbSession, user_id: UserId):
    if req.priority < 1 or req.priority > 3:
        raise HTTPException(
            status.HTTP_400_BAD_REQUEST,
            detail={"message": "Priority должен быть 1 (высокий), 2 (средний) или 3 (низкий)"},
        )
    todo = Todo(
        user_id=user_id,
        title=req.title,
        description=req.description,
        priority=req.priority,
        due_at=req.due_at,
        linked_note_id=req.linked_note_id,
    )
    db.add(todo)
    db.commit()
    db.refresh(todo)
    return _map(todo)


@router.put("/{todo_id}", response_model=TodoDto)
def update(todo_id: uuid.UUID, req: UpdateTodoRequest, db: DbSession, user_id: UserId):
    todo = db.query(Todo).filter(Todo.id == todo_id, Todo.user_id == user_id, Todo.is_deleted.is_(False)).first()
    if not todo:
        raise HTTPException(status.HTTP_404_NOT_FOUND)
    if req.title is not None:
        todo.title = req.title
    if req.description is not None:
        todo.description = req.description
    if req.is_done is not None:
        todo.is_done = req.is_done
    if req.priority is not None:
        todo.priority = req.priority
    if req.due_at is not None:
        todo.due_at = req.due_at
    if req.linked_note_id is not None:
        todo.linked_note_id = req.linked_note_id
    todo.updated_at = datetime.now(timezone.utc)
    db.commit()
    db.refresh(todo)
    return _map(todo)


@router.patch("/{todo_id}/toggle", response_model=TodoDto)
def toggle(todo_id: uuid.UUID, db: DbSession, user_id: UserId):
    todo = db.query(Todo).filter(Todo.id == todo_id, Todo.user_id == user_id, Todo.is_deleted.is_(False)).first()
    if not todo:
        raise HTTPException(status.HTTP_404_NOT_FOUND)
    todo.is_done = not todo.is_done
    todo.updated_at = datetime.now(timezone.utc)
    db.commit()
    db.refresh(todo)
    return _map(todo)


@router.delete("/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete(todo_id: uuid.UUID, db: DbSession, user_id: UserId):
    todo = db.query(Todo).filter(Todo.id == todo_id, Todo.user_id == user_id, Todo.is_deleted.is_(False)).first()
    if not todo:
        raise HTTPException(status.HTTP_404_NOT_FOUND)
    todo.is_deleted = True
    todo.updated_at = datetime.now(timezone.utc)
    db.commit()