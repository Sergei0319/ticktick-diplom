# -*- coding: utf-8 -*-
"""Шпаргалка к защите TickTick — полные ответы по разделам (для печати)."""
from datetime import date
from pathlib import Path

from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.shared import Cm, Pt
from docx.oxml.ns import qn

OUT_DOCX = Path(r"C:\Users\Сергей\Desktop\Заметки_к_защите_TickTick.docx")
REPO = "!!!Диплом!!!"


def set_document_style(doc: Document) -> None:
    style = doc.styles["Normal"]
    style.font.name = "Times New Roman"
    style.font.size = Pt(12)
    style._element.rPr.rFonts.set(qn("w:eastAsia"), "Times New Roman")
    for section in doc.sections:
        section.top_margin = Cm(2)
        section.bottom_margin = Cm(2)
        section.left_margin = Cm(2.5)
        section.right_margin = Cm(1.5)


def add_bullets(doc: Document, items: list[str]) -> None:
    for text in items:
        doc.add_paragraph(text, style="List Bullet")


def add_numbered(doc: Document, items: list[str]) -> None:
    for text in items:
        doc.add_paragraph(text, style="List Number")


def add_table(doc: Document, headers: list[str], rows: list[list[str]]) -> None:
    table = doc.add_table(rows=1 + len(rows), cols=len(headers))
    table.style = "Table Grid"
    hdr = table.rows[0].cells
    for i, h in enumerate(headers):
        hdr[i].text = h
        for p in hdr[i].paragraphs:
            for r in p.runs:
                r.bold = True
    for ri, row in enumerate(rows):
        cells = table.rows[ri + 1].cells
        for ci, val in enumerate(row):
            cells[ci].text = val
    doc.add_paragraph()


def build_docx() -> None:
    doc = Document()
    set_document_style(doc)

    title = doc.add_paragraph()
    title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    tr = title.add_run("Шпаргалка к защите диплома\n«TickTick» — клиент-серверное SPA")
    tr.bold = True
    tr.font.size = Pt(16)

    sub = doc.add_paragraph()
    sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
    sub.add_run(f"Дата подготовки: {date.today().strftime('%d.%m.%Y')}")

    doc.add_paragraph(
        f"Репозиторий: «{REPO}». Документ для печати: ответы по структуре проекта, "
        "соответствию ТЗ, демонстрации и типовым вопросам комиссии."
    )

    # --- 1. Питч ---
    doc.add_heading("1. Устный питч (30–60 секунд)", level=1)
    doc.add_paragraph(
        "Разработано веб-приложение TickTick — персональный органайзер: заметки с тегами и "
        "wiki-ссылками, список задач с приоритетами и дедлайнами, календарь событий, профиль "
        "пользователя и панель администратора."
    )
    doc.add_paragraph(
        "Архитектура клиент-серверная: фронтенд — одностраничное приложение (SPA) на React; "
        "бэкенд — REST API на FastAPI; данные хранятся в PostgreSQL. Обмен — JSON по HTTP, "
        "авторизация — JWT (короткий access-токен и длинный refresh с хранением в БД)."
    )
    doc.add_paragraph(
        "Проект развёртывается локально или в Docker (три сервиса: БД, API, фронт). "
        "Документация API доступна через Swagger на /docs."
    )

    # --- 2. Архитектура ---
    doc.add_heading("2. Архитектура системы", level=1)
    doc.add_paragraph("Цепочка запроса:", style="List Bullet")
    doc.add_paragraph(
        "Браузер (React, Vite) → Axios (Bearer JWT) → FastAPI (роутеры) → "
        "SQLAlchemy (сессия на запрос) → PostgreSQL.",
        style="List Bullet",
    )
    doc.add_paragraph(
        "Файлы-вложения заметок сохраняются на диск (папка uploads) и отдаются как статика "
        "по URL /uploads/… (FastAPI StaticFiles).",
        style="List Bullet",
    )
    add_bullets(
        doc,
        [
            "Точка сборки API: Backend/app/main.py — CORS, подключение роутеров, /health, /uploads.",
            "CORS: CORSMiddleware, список origin из Backend/.env (поле cors_origins в config.py).",
            "Сессия БД: get_db() в db.py — открытие Session на один HTTP-запрос, закрытие в finally.",
            "Фронт: маршрутизация React Router (App.jsx); layout AppLayout + боковое меню; "
            "гостевые страницы login/register; остальное за ProtectedRoute.",
            "Разделение слоёв: pages (экраны), components (переиспользуемые блоки UI), "
            "api/client.js (HTTP), store/authStore.js (сессия Zustand).",
        ],
    )

    # --- 3. ТЗ ---
    doc.add_heading("3. Соответствие техническому заданию", level=1)
    add_table(
        doc,
        ["Требование", "Реализация", "Где показать"],
        [
            [
                "5–6+ страниц SPA",
                "Главная, заметки, деталь заметки, календарь, задачи, профиль, вход, регистрация, админ",
                "Front/src/App.jsx — маршруты",
            ],
            [
                "15–20 компонентов",
                "20 файлов в Front/src/components/",
                "NoteCard, Loader, ProtectedRoute и др.",
            ],
            [
                "Zustand",
                "authStore: токены, userId, role, persist в localStorage",
                "Front/src/store/authStore.js",
            ],
            [
                "Axios, лоадеры, ошибки",
                "http + interceptors; Loader и ErrorMessage на страницах",
                "Front/src/api/client.js, HomePage.jsx",
            ],
            [
                "15+ эндпоинтов",
                "auth (4), users (1), admin (4), notes (11), todos (7), calendar (5), sync (1), export (2), health",
                "Swagger http://localhost:8000/docs",
            ],
            [
                "JWT и роли user / admin",
                "access + refresh; require_admin → 403; AdminRoute на фронте",
                "deps.py, auth.py, AdminRoute.jsx",
            ],
            [
                "7+ таблиц БД",
                "9 таблиц в models.py",
                "Backend/ticktick_schema.sql",
            ],
            [
                ".env",
                "pydantic-settings, Backend/.env.example",
                "config.py",
            ],
            [
                "Docker",
                "docker-compose: db, api, front",
                "docker-compose.yml",
            ],
        ],
    )

    # --- 4. Модули ---
    doc.add_heading("4. Карта модулей", level=1)
    add_table(
        doc,
        ["Функция", "Backend", "Frontend", "Таблицы БД"],
        [
            [
                "Регистрация и вход",
                "routers/auth.py, services/tokens.py",
                "LoginPage, RegisterPage, authStore",
                "users, refresh_tokens",
            ],
            [
                "Профиль",
                "routers/users.py — GET /api/users/me",
                "ProfilePage, ProfileCard",
                "users",
            ],
            [
                "Заметки",
                "routers/notes.py, services/wiki_links.py",
                "NotesPage, NoteDetailPage, NoteCard, SearchBar, TrashDrawer",
                "notes, note_links, note_attachments",
            ],
            [
                "Задачи",
                "routers/todos.py",
                "TodosPage, TodoItem, TodoCreateForm",
                "todos",
            ],
            [
                "Календарь",
                "routers/calendar.py",
                "CalendarPage, EventItem, EventCreateForm",
                "calendar_events",
            ],
            [
                "Админка",
                "routers/admin.py",
                "AdminPage, AdminUserTable, AdminRoute",
                "users (role, deleted_at)",
            ],
            [
                "Синхронизация",
                "routers/sync.py",
                "API для клиентов с device_id",
                "sync_checkpoints",
            ],
            [
                "Экспорт",
                "routers/export_router.py, services/export_service.py",
                "Запрос с фронта на /export/docx|pdf",
                "notes (чтение)",
            ],
        ],
    )

    # --- 5. JWT ---
    doc.add_heading("5. Авторизация и JWT", level=1)
    doc.add_paragraph("Регистрация (POST /api/auth/register):", style="List Bullet")
    add_numbered(
        doc,
        [
            "Pydantic проверяет email и пароль (schemas.py).",
            "Пароль хешируется bcrypt (passlib в services/tokens.py), в БД — только password_hash.",
            "Создаётся запись User; вызывается _issue_tokens: access JWT + случайный refresh.",
            "Refresh сохраняется в refresh_tokens как token_hash (не открытый текст).",
        ],
    )
    doc.add_paragraph("Вход (POST /api/auth/login): проверка пароля → та же выдача пары токенов.")
    doc.add_paragraph("Access-токен (≈15 мин): HS256, claims iss, aud, sub/nameidentifier (user UUID), role.")
    doc.add_paragraph(
        "Защита эндпоинтов: HTTPBearer → jwt.decode в deps.get_token_payload → "
        "get_current_user_id → get_current_user (пользователь не удалён). "
        "Админ: require_admin проверяет user.role == 'admin'."
    )
    doc.add_paragraph("Фронт:")
    add_bullets(
        doc,
        [
            "После login setSession в Zustand (persist ticktick-auth в localStorage).",
            "Каждый запрос: interceptor добавляет Authorization: Bearer accessToken.",
            "При 401: один раз POST /api/auth/refresh, обновление сессии, повтор запроса; иначе logout.",
            "ProtectedRoute: нет токена → /auth/login. AdminRoute: role !== admin → редирект.",
        ],
    )
    doc.add_paragraph(
        "Logout: refresh помечается revoked в БД — сессию можно отозвать без ожидания истечения JWT."
    )

    # --- 6. БД ---
    doc.add_heading("6. База данных и связи", level=1)
    doc.add_paragraph("Таблицы (SQLAlchemy models.py):")
    add_bullets(
        doc,
        [
            "users — учётная запись, role (user|admin), soft delete через deleted_at.",
            "refresh_tokens — хеш refresh, expires_at, revoked; FK user_id ON DELETE CASCADE.",
            "notes — title, content, tags (ARRAY), is_deleted, version (для sync).",
            "note_links — граф wiki-ссылок: source_note_id → target_note_id, уникальная пара.",
            "note_attachments — метаданные файла, file_path на диске.",
            "calendar_events — start_at, end_at, all_day, опционально linked_note_id.",
            "todos — is_done, priority 1–3 (CHECK), due_at, linked_note_id.",
            "sync_checkpoints — (user_id, device_id) уникально, last_sync.",
        ],
    )
    doc.add_paragraph(
        "Связи: почти все сущности привязаны к users через user_id с CASCADE. "
        "У todo и calendar_events linked_note_id при удалении заметки — SET NULL. "
        "Многие-ко-многим между заметками реализовано через промежуточную таблицу note_links "
        "(две FK на notes, не классическая M2M с тегами, а направленный граф ссылок)."
    )

    # --- 7. Фишки ---
    doc.add_heading("7. Ключевые особенности (не «голый CRUD»)", level=1)
    add_bullets(
        doc,
        [
            "Wiki-ссылки: в тексте [[Название другой заметки]]; при сохранении sync_links "
            "(wiki_links.py) парсит regex, находит заметки по title, пересобирает note_links.",
            "Корзина заметок: DELETE — мягкое удаление (is_deleted); GET /trash, restore, permanent delete.",
            "Поиск: GET /api/notes/search — использование функции PostgreSQL search_notes (полнотекст/фильтр в schema.sql).",
            "Вложения: multipart POST, запись в uploads_dir, строка в note_attachments; раздача через /uploads.",
            "Экспорт: GET .../export/docx и /pdf — сервис export_service (python-docx, fpdf2).",
            "Sync: GET /api/sync?since=…&device_id=… — отдаёт изменённые notes/todos/events, обновляет checkpoint.",
            "Задачи: отдельный GET /overdue; PATCH /toggle для быстрой отметки выполнения.",
        ],
    )

    # --- 8. Стек ---
    doc.add_heading("8. Обоснование технологий", level=1)
    add_bullets(
        doc,
        [
            "FastAPI — быстрый REST, автогенерация OpenAPI (/docs), dependency injection для auth и БД.",
            "SQLAlchemy 2 + Alembic — ORM и версионирование схемы (миграции, напр. добавление role).",
            "PostgreSQL — ARRAY для тегов, надёжные FK, возможность SQL-функций для поиска.",
            "Pydantic — валидация запросов/ответов; CamelModel — JSON в camelCase для JavaScript-клиента.",
            "React + Vite — SPA без перезагрузки страницы; React Router для вложенных маршрутов.",
            "Ant Design — готовые UI-компоненты (таблицы, формы, календарь на фронте).",
            "Zustand — лёгкое глобальное состояние сессии без boilerplate Redux.",
            "Docker Compose — воспроизводимый запуск БД, API и собранного фронта одной командой.",
        ],
    )

    # --- 9. Запуск и демо ---
    doc.add_heading("9. Запуск и сценарий демонстрации (~7–10 мин)", level=1)
    doc.add_paragraph("Запуск без Docker (из README):")
    add_numbered(
        doc,
        [
            "Инициализация БД: Backend/scripts/init_db.ps1 или PostgreSQL + ticktick_schema.sql + alembic upgrade head.",
            "Backend: pip install -r requirements.txt; uvicorn app.main:app --reload --port 8000.",
            "Front: npm install; npm run dev → http://localhost:5173 (API http://localhost:8000).",
        ],
    )
    doc.add_paragraph("Docker: docker compose up --build → API :8000, фронт :3000, Postgres :5434.")
    doc.add_paragraph("Назначение админа: UPDATE users SET role = 'admin' WHERE email = '…';")
    doc.add_paragraph("Рекомендуемый сценарий на защите:")
    add_numbered(
        doc,
        [
            "Регистрация нового пользователя → автоматический вход.",
            "Создать две заметки; во второй в тексте указать [[Заголовок первой]] → сохранить → показать связь.",
            "Добавить задачу с дедлайном, переключить выполнение (toggle).",
            "Создать событие в календаре.",
            "Удалить заметку в корзину → открыть корзину → восстановить.",
            "Профиль: GET /me с данными пользователя.",
            "Показать Swagger: 2–3 эндпоинта (notes list, auth login schema).",
            "При наличии админа: статистика и список пользователей.",
            "GET /health — сервис жив (для Docker healthcheck).",
        ],
    )

    # --- 10. Индекс ---
    doc.add_heading("10. Быстрый указатель «вопрос → файл»", level=1)
    add_table(
        doc,
        ["Тема", "Файл"],
        [
            ["Сборка API, CORS, роутеры", "Backend/app/main.py"],
            ["Модели и таблицы", "Backend/app/models.py"],
            ["JWT, Depends, admin", "Backend/app/deps.py"],
            ["Login, register, refresh", "Backend/app/routers/auth.py"],
            ["Хеш пароля, генерация JWT", "Backend/app/services/tokens.py"],
            ["CRUD заметок, корзина, поиск", "Backend/app/routers/notes.py"],
            ["Wiki-ссылки", "Backend/app/services/wiki_links.py"],
            ["Задачи", "Backend/app/routers/todos.py"],
            ["Календарь", "Backend/app/routers/calendar.py"],
            ["Админ API", "Backend/app/routers/admin.py"],
            ["Экспорт", "Backend/app/routers/export_router.py"],
            ["Маршруты SPA", "Front/src/App.jsx"],
            ["Сессия Zustand", "Front/src/store/authStore.js"],
            ["Axios + refresh", "Front/src/api/client.js"],
            ["Охрана маршрутов", "Front/src/components/ProtectedRoute.jsx, AdminRoute.jsx"],
            ["Docker", "docker-compose.yml"],
            ["Настройки .env", "Backend/app/config.py"],
        ],
    )

    # --- 11. Слабые места ---
    doc.add_heading("11. Ограничения и возможное развитие", level=1)
    doc.add_paragraph(
        "Честно для комиссии: нет мобильного нативного клиента (есть задел sync по device_id); "
        "нет OAuth через Google/VK; нет WebSocket для живых обновлений; автотесты E2E не выделены "
        "в отдельный контур. Email-верификация в модели есть (is_email_verified), полный поток писем "
        "может быть упрощён."
    )
    doc.add_paragraph("Развитие: refresh rotation, rate limiting, S3 для вложений, "
                      "полнотекстовый поиск с ранжированием, unit/integration-тесты на pytest.")

    # --- 12. Эндпоинты справочник ---
    doc.add_heading("12. Справочник основных API (префиксы)", level=1)
    add_bullets(
        doc,
        [
            "/api/auth — register, login, refresh, logout",
            "/api/users/me — профиль текущего пользователя",
            "/api/admin — stats, users, patch role, delete user",
            "/api/notes — CRUD, trash, search, restore, permanent, attachments",
            "/api/todos — list, overdue, CRUD, toggle",
            "/api/calendar — CRUD событий",
            "/api/sync — синхронизация по since",
            "/api/notes/{id}/export/docx|pdf — экспорт",
            "/health — проверка живости",
        ],
    )

    doc.add_page_break()
    doc.add_heading("Приложение: типовые вопросы (краткие ответы)", level=1)
    qa_short = [
        (
            "Почему FastAPI, а не Django?",
            "Нужен лёгкий REST API с OpenAPI; нет требования к админке Django и шаблонам на сервере.",
        ),
        (
            "Почему refresh в БД?",
            "Отзыв при logout, хранение только хеша, ротация при refresh.",
        ),
        (
            "Чем SPA отличается от MPA?",
            "Одна загрузка shell; React Router меняет view без полной перезагрузки document.",
        ),
        (
            "Как изолируются данные пользователей?",
            "Во всех запросах фильтр по user_id из JWT; чужие заметки недоступны.",
        ),
        (
            "Где валидация?",
            "Pydantic на входе; при ошибке 422 с деталями полей.",
        ),
        (
            "Как работает CORS?",
            "Браузер с другого порта (5173) разрешён явным списком origin в middleware.",
        ),
    ]
    for q, a in qa_short:
        p = doc.add_paragraph()
        p.add_run(f"Вопрос: {q} ").bold = True
        doc.add_paragraph(f"Ответ: {a}")

    doc.add_paragraph()
    p = doc.add_paragraph()
    p.add_run(
        "Расширенный банк вопросов с номерами строк: "
        "файл «Вопросы_ответы_защита_TickTick.docx» на рабочем столе "
        "(генерируется скриптом build_defense_qa_docx.py)."
    ).italic = True

    doc.save(OUT_DOCX)


def main() -> None:
    build_docx()
    print(f"Saved: {OUT_DOCX}")


if __name__ == "__main__":
    main()