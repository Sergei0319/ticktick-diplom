# -*- coding: utf-8 -*-
"""Вопросы-ответы к защите с привязкой к файлам и строкам."""
from datetime import date
from pathlib import Path

from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.shared import Pt

OUT_DOCX = Path(r"C:\Users\Сергей\Desktop\Вопросы_ответы_защита_TickTick.docx")
OUT_MD = Path(r"C:\Users\Сергей\Desktop\Вопросы_ответы_защита_TickTick.md")
REPO = "!!!Диплом!!!"


# (категория, вопрос, ответ, [(файл, строка_от, строка_до, фрагмент)])
QA = [
    (
        "ТЗ / общее",
        "Является ли проект клиент-серверным SPA с разделением фронта и бэка?",
        "Да. React SPA отдельно от FastAPI; обмен JSON по HTTP.",
        [("README.md", 3, 10, "Описание Front + Backend"), ("Backend/app/main.py", 29, 53, "FastAPI + роутеры")],
    ),
    (
        "ТЗ / стек",
        "Какой стек Backend и почему FastAPI, а не Django?",
        "Python 3.12, FastAPI, SQLAlchemy 2, Alembic, Pydantic. Курс допускает FastAPI как чистый REST API с автодокументацией.",
        [("README.md", 3, 3, "Стек в README"), ("Backend/requirements.txt", 1, 5, "fastapi, sqlalchemy")],
    ),
    (
        "ТЗ / CORS",
        "Где настроена CORS-политика?",
        "CORSMiddleware: origins из settings.cors_origins (.env), credentials и методы *.",
        [("Backend/app/main.py", 31, 40, "CORSMiddleware"), ("Backend/app/config.py", 26, 27, "cors_origins")],
    ),
    (
        "ТЗ / страницы",
        "Сколько страниц (маршрутов) на фронте?",
        "Не менее 6 требуемых: главная, деталь заметки, профиль, login/register, админ; плюс notes, calendar, todos.",
        [("Front/src/App.jsx", 24, 49, "Все Route")],
    ),
    (
        "ТЗ / компоненты",
        "Где декомпозиция UI (15–20 компонентов)?",
        "Каталог Front/src/components/ — карточки, лейаут, лоадер, поиск, маршруты-обёртки и т.д.",
        [("Front/src/components/NoteCard.jsx", 1, 18, "Пример карточки"), ("Front/src/components/Loader.jsx", 1, 9, "Loader")],
    ),
    (
        "ТЗ / состояние",
        "Используется ли Zustand для сессии?",
        "Да, persist в localStorage: токены, userId, role.",
        [("Front/src/store/authStore.js", 4, 31, "create + persist")],
    ),
    (
        "ТЗ / Axios",
        "Как фронт ходит в API и обрабатывает ошибки?",
        "Axios instance, Bearer в request interceptor, refresh при 401, единый reject с сообщением.",
        [("Front/src/api/client.js", 6, 43, "http + interceptors")],
    ),
    (
        "ТЗ / эндпоинты",
        "Где подключаются все роутеры API (≥15 эндпоинтов)?",
        "include_router для auth, users, admin, notes, todos, calendar, sync, export.",
        [("Backend/app/main.py", 45, 53, "include_router")],
    ),
    (
        "ТЗ / CRUD",
        "Где CRUD заметок?",
        "GET/POST list, GET one, PUT, DELETE soft, trash, restore, search, attachments.",
        [("Backend/app/routers/notes.py", 37, 100, "CRUD + search"), ("Backend/app/routers/notes.py", 121, 164, "delete/restore/attachments")],
    ),
    (
        "ТЗ / JWT",
        "Как реализована регистрация и выдача JWT?",
        "Register → bcrypt hash → User → access JWT + refresh в БД (хеш).",
        [("Backend/app/routers/auth.py", 32, 45, "register"), ("Backend/app/routers/auth.py", 12, 29, "_issue_tokens")],
    ),
    (
        "ТЗ / пароли",
        "Как хешируются пароли?",
        "passlib CryptContext, схема bcrypt.",
        [("Backend/app/services/tokens.py", 12, 21, "hash_password / verify")],
    ),
    (
        "ТЗ / JWT защита",
        "Как проверяется JWT на защищённых ручках?",
        "HTTPBearer → jwt.decode → user_id → User в БД.",
        [("Backend/app/deps.py", 27, 55, "get_token_payload, get_current_user")],
    ),
    (
        "ТЗ / роли",
        "Как разделяются user и admin?",
        "role в JWT и User; require_admin → 403; AdminUser в admin router.",
        [("Backend/app/deps.py", 58, 61, "require_admin"), ("Front/src/components/AdminRoute.jsx", 4, 7, "role === admin")],
    ),
    (
        "ТЗ / валидация",
        "Где валидация входящих данных?",
        "Pydantic-схемы: RegisterRequest, CreateNoteRequest и т.д.; 422 автоматически.",
        [("Backend/app/schemas.py", 13, 19, "CamelModel"), ("Backend/app/schemas.py", 25, 26, "RegisterRequest")],
    ),
    (
        "ТЗ / БД",
        "Сколько таблиц и какие связи?",
        "8 таблиц: users, refresh_tokens, notes, note_links, note_attachments, calendar_events, todos, sync_checkpoints.",
        [("Backend/ticktick_schema.sql", 11, 11, "users"), ("Backend/ticktick_schema.sql", 81, 88, "note_links FK")],
    ),
    (
        "ТЗ / M2M",
        "Где связь многие-ко-многим?",
        "note_links: две FK на notes — граф wiki-ссылок между заметками.",
        [("Backend/ticktick_schema.sql", 81, 88, "note_links"), ("Backend/app/models.py", 79, 95, "class NoteLink")],
    ),
    (
        "ТЗ / поиск",
        "Как реализован поиск заметок?",
        "PostgreSQL функция search_notes, вызов из SQLAlchemy text().",
        [("Backend/ticktick_schema.sql", 174, 174, "FUNCTION search_notes"), ("Backend/app/routers/notes.py", 61, 69, "GET /search")],
    ),
    (
        "ТЗ / .env",
        "Откуда читаются секреты и URL БД?",
        "pydantic-settings BaseSettings, env_file=.env.",
        [("Backend/app/config.py", 6, 27, "Settings"), ("Backend/.env.example", 1, 5, "переменные")],
    ),
    (
        "ТЗ / Docker",
        "Как запускается весь стек одной командой?",
        "docker-compose: db, api (uvicorn+alembic), front (nginx).",
        [("docker-compose.yml", 3, 39, "services db, api, front")],
    ),
    (
        "Архитектура",
        "Что такое SPA в вашем проекте?",
        "Один index.html, навигация React Router без перезагрузки страницы.",
        [("Front/src/main.jsx", 1, 16, "createRoot + Router"), ("Front/src/App.jsx", 22, 51, "Routes")],
    ),
    (
        "Архитектура",
        "Как устроена сессия БД в FastAPI?",
        "get_db: SessionLocal на запрос, yield, finally close.",
        [("Backend/app/db.py", 13, 28, "engine, get_db")],
    ),
    (
        "Архитектура",
        "Зачем CamelModel?",
        "JSON для фронта в camelCase (userId, accessToken), from_attributes из ORM.",
        [("Backend/app/schemas.py", 13, 19, "CamelModel config")],
    ),
    (
        "Фронт",
        "Как защищаются приватные маршруты?",
        "Нет accessToken → редирект на /auth/login.",
        [("Front/src/components/ProtectedRoute.jsx", 4, 8, "ProtectedRoute")],
    ),
    (
        "Фронт",
        "Где лоадер и ошибки на примере главной?",
        "HomePage: Loader при loading, ErrorMessage при catch.",
        [("Front/src/pages/HomePage.jsx", 32, 36, "Loader / ErrorMessage")],
    ),
    (
        "Бэкенд",
        "Как обновляется access-токен?",
        "POST /api/auth/refresh, старый refresh revoke, новая пара токенов.",
        [("Backend/app/routers/auth.py", 60, 76, "refresh")],
    ),
    (
        "Бэкенд",
        "Где CRUD задач и календаря?",
        "routers/todos.py, routers/calendar.py.",
        [("Backend/app/routers/todos.py", 27, 68, "todos endpoints"), ("Backend/app/routers/calendar.py", 28, 51, "calendar list/create")],
    ),
    (
        "Бэкенд",
        "Как экспорт заметки в файл?",
        "export_router → export_service (python-docx, fpdf2).",
        [("Backend/app/routers/export_router.py", 19, 33, "GET /docx"), ("Backend/app/services/export_service.py", 26, 48, "export_docx")],
    ),
    (
        "Бэкенд",
        "Что делает /api/sync?",
        "Отдаёт изменения notes/events/todos после since, обновляет sync_checkpoints.",
        [("Backend/app/routers/sync.py", 11, 44, "pull + checkpoint")],
    ),
    (
        "Бэкенд",
        "Что делает админ API?",
        "Статистика, список users, смена role, soft-delete user.",
        [("Backend/app/routers/admin.py", 13, 66, "admin routes")],
    ),
    (
        "Комиссия",
        "Почему refresh-токен хранится в БД, а не только в JWT?",
        "Можно отозвать (logout, rotation), хранится hash, не plaintext.",
        [("Backend/app/models.py", 44, 51, "RefreshToken"), ("Backend/app/routers/auth.py", 79, 85, "logout revoke")],
    ),
    (
        "Комиссия",
        "Чем soft delete заметок отличается от permanent?",
        "is_deleted + deleted_at; корзина и restore vs DELETE permanent.",
        [("Backend/app/routers/notes.py", 48, 58, "trash"), ("Backend/app/routers/notes.py", 135, 151, "restore/permanent")],
    ),
    (
        "Комиссия",
        "Как загружаются вложения?",
        "POST multipart, запись в uploads, NoteAttachment в БД, StaticFiles /uploads.",
        [("Backend/app/routers/notes.py", 164, 164, "attachments"), ("Backend/app/main.py", 42, 43, "mount uploads")],
    ),
    (
        "Комиссия",
        "Сколько минут живёт access-токен?",
        "access_token_minutes в config (по умолчанию 15).",
        [("Backend/app/config.py", 20, 23, "access_token_minutes"), ("Backend/app/services/tokens.py", 33, 34, "exp в JWT")],
    ),
    (
        "Комиссия",
        "Где миграции Alembic?",
        "alembic.ini, migrations/versions — например роль пользователя.",
        [("Backend/alembic.ini", 1, 20, "конфиг Alembic"), ("Backend/alembic/env.py", 1, 30, "подключение metadata")],
    ),
    (
        "Демо",
        "Как проверить, что API жив без БД?",
        "GET /health.",
        [("Backend/app/main.py", 56, 59, "health")],
    ),
]


def ref_line(file, lo, hi, hint):
    if lo is None:
        return f"  • {REPO}/{file} — {hint}"
    if lo == hi:
        return f"  • {REPO}/{file}, стр. {lo} — {hint}"
    return f"  • {REPO}/{file}, стр. {lo}–{hi} — {hint}"


def build_md():
    lines = [
        f"# Вопросы и ответы к защите — TickTick",
        f"",
        f"Дата: {date.today().strftime('%d.%m.%Y')}  ",
        f"Репозиторий: `{REPO}`",
        f"",
        f"Формат ссылки: **файл:строка** (открыть в IDE по Ctrl+G).",
        f"",
    ]
    cat = None
    n = 0
    for item in QA:
        category, q, a, refs = item
        if category != cat:
            cat = category
            lines.append(f"\n## {category}\n")
        n += 1
        lines.append(f"### {n}. {q}\n")
        lines.append(f"**Ответ:** {a}\n")
        lines.append("**Где в коде:**")
        for file, lo, hi, hint in refs:
            lines.append(ref_line(file, lo, hi, hint))
        lines.append("")
    return "\n".join(lines)


def build_docx():
    doc = Document()
    style = doc.styles["Normal"]
    style.font.name = "Times New Roman"
    style.font.size = Pt(12)

    t = doc.add_paragraph()
    t.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = t.add_run("Вопросы и ответы к защите\n(dиплом TickTick)")
    r.bold = True
    r.font.size = Pt(14)
    doc.add_paragraph(f"Дата: {date.today().strftime('%d.%m.%Y')}")
    doc.add_paragraph(
        "К каждому ответу указаны пути к файлам и номера строк в репозитории "
        f"«{REPO}». На защите открывайте файл и переходите к строке (Ctrl+G)."
    )

    n = 0
    cat = None
    for item in QA:
        category, q, a, refs = item
        if category != cat:
            cat = category
            doc.add_heading(category, level=1)
        n += 1
        doc.add_heading(f"{n}. {q}", level=2)
        p = doc.add_paragraph()
        p.add_run("Ответ: ").bold = True
        p.add_run(a)
        doc.add_paragraph("Ссылки на код:")
        for file, lo, hi, hint in refs:
            doc.add_paragraph(ref_line(file, lo, hi, hint).strip(" "), style="List Bullet")

    doc.save(OUT_DOCX)


def main():
    OUT_MD.write_text(build_md(), encoding="utf-8")
    build_docx()
    print(f"Saved: {OUT_DOCX}")
    print(f"Saved: {OUT_MD}")


if __name__ == "__main__":
    main()