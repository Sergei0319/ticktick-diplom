# -*- coding: utf-8 -*-
"""Ответы к «Плану изучения TickTick» — отдельный файл для печати."""
from datetime import date
from pathlib import Path

from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.shared import Cm, Pt
from docx.oxml.ns import qn

OUT_DOCX = Path(r"C:\Users\Сергей\Desktop\Ответы_к_плану_изучения_TickTick.docx")
REPO = "!!!Диплом!!!"
PLAN_NAME = "План_изучения_TickTick.docx"


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


def qa(doc: Document, question: str, answer: str) -> None:
    p = doc.add_paragraph()
    p.add_run(f"Вопрос: {question}").bold = True
    doc.add_paragraph(f"Ответ: {answer}")


def build_docx() -> None:
    doc = Document()
    set_document_style(doc)

    title = doc.add_paragraph()
    title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    tr = title.add_run("Ответы к плану изучения\nTickTick (диплом)")
    tr.bold = True
    tr.font.size = Pt(16)

    sub = doc.add_paragraph()
    sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
    sub.add_run(f"Дата: {date.today().strftime('%d.%m.%Y')}")

    doc.add_paragraph(
        f"Пара к документу «{PLAN_NAME}» на рабочем столе. "
        "План — чек-листы и поля для записей; этот файл — готовые ответы для чтения и печати."
    )

    # --- Ориентировка ---
    doc.add_heading("О проекте — развёрнутые ответы к таблице файлов", level=1)
    add_table(
        doc,
        ["Файл", "Ответ: что искать и что сказать"],
        [
            [
                "README.md",
                "Стек: Front React/Vite/Ant Design/Zustand/Axios; Backend FastAPI/SQLAlchemy/PostgreSQL/Alembic/JWT. "
                "Команды init_db, uvicorn, npm run dev, docker compose. Таблица соответствия ТЗ.",
            ],
            [
                "Backend/app/main.py",
                "Создаётся app FastAPI; CORSMiddleware из settings.cors_origins; mount /uploads; "
                "include_router × 8; GET /health без БД.",
            ],
            [
                "Backend/app/models.py",
                "9 ORM-моделей = 9 таблиц; UUID PK; ARRAY tags; NoteLink как граф; CheckConstraint priority 1–3.",
            ],
            [
                "Backend/app/deps.py",
                "HTTPBearer → jwt.decode (iss, aud, HS256) → UUID пользователя → SELECT User; require_admin → 403.",
            ],
            [
                "Backend/app/routers/",
                "Каждый файл — APIRouter с prefix /api/...; изоляция по user_id; Pydantic DTO на вход/выход.",
            ],
            [
                "Front/src/App.jsx",
                "Routes: /auth/login, /auth/register; вложенные /, notes, notes/:id, calendar, todos, profile, admin.",
            ],
            [
                "Front/src/api/client.js",
                "axios.create(baseURL); Bearer в request; при 401 один refresh и retry; иначе logout.",
            ],
            [
                "Front/src/store/authStore.js",
                "Zustand persist: accessToken, refreshToken, userId, displayName, role; setSession/logout.",
            ],
            [
                "docker-compose.yml",
                "db:5434→5432 + schema SQL; api: alembic + uvicorn :8000; front nginx :3000; volume uploads.",
            ],
        ],
    )

    # --- 11 разделов заметок ---
    doc.add_heading("Раздел 1. Питч (30–60 сек) — готовый текст", level=1)
    doc.add_paragraph(
        "Тема диплома — веб-приложение TickTick для личной продуктивности: заметки с тегами и wiki-ссылками, "
        "список задач с приоритетом и дедлайнами, календарь событий. Реализована клиент-серверная архитектура: "
        "в браузере одностраничное приложение на React, на сервере REST API на FastAPI, данные в PostgreSQL. "
        "Пользователь регистрируется, получает JWT и работает только со своими данными; администратор видит "
        "статистику и управляет ролями. Проект можно поднять в Docker одной командой."
    )

    doc.add_heading("Раздел 2. Архитектура", level=1)
    doc.add_paragraph(
        "Запрос пользователя обрабатывается так: React-компонент вызывает apiGet/apiSend → Axios добавляет "
        "Authorization: Bearer → FastAPI находит роут → Depends подставляет db-сессию и current user → "
        "SQLAlchemy выполняет запрос к PostgreSQL → ответ сериализуется Pydantic в JSON camelCase → фронт обновляет UI."
    )
    doc.add_paragraph(
        "CORS настроен в main.py: список origin из .env (localhost:5173 и :3000), иначе браузер заблокирует "
        "запросы с фронта. Файлы вложений пишутся на диск в uploads_dir и отдаются через StaticFiles по /uploads."
    )

    doc.add_heading("Раздел 3. Соответствие ТЗ", level=1)
    add_table(
        doc,
        ["Требование", "Где", "Как показать"],
        [
            ["6+ страниц", "App.jsx", "Пройти меню: главная, заметки, деталь, календарь, задачи, профиль"],
            ["20 компонентов", "Front/src/components/", "Перечислить NoteCard, AppLayout, SideMenu…"],
            ["Zustand", "authStore.js", "localStorage ключ ticktick-auth после login"],
            ["Axios + ошибки", "client.js, HomePage", "Loader при загрузке, ErrorMessage при catch"],
            ["15+ API", "main.py + Swagger", "Открыть /docs, пролистать теги auth, notes, todos…"],
            ["JWT + роли", "auth.py, deps.py", "Login → заголовок Authorization в Network"],
            ["7+ таблиц", "models.py", "Перечислить 9 имён таблиц"],
            [".env", "config.py", "database_url, jwt_secret, cors_origins"],
            ["Docker", "docker-compose.yml", "docker compose up --build"],
        ],
    )

    doc.add_heading("Раздел 4. Карта модулей", level=1)
    add_table(
        doc,
        ["Функция", "Backend", "Front", "БД"],
        [
            ["Вход", "auth.py, tokens.py", "LoginPage, RegisterPage", "users, refresh_tokens"],
            ["Заметки", "notes.py, wiki_links.py", "NotesPage, NoteDetailPage", "notes, note_links, attachments"],
            ["Задачи", "todos.py", "TodosPage", "todos"],
            ["Календарь", "calendar.py", "CalendarPage", "calendar_events"],
            ["Профиль", "users.py", "ProfilePage", "users"],
            ["Админ", "admin.py", "AdminPage", "users.role"],
            ["Sync", "sync.py", "(API)", "sync_checkpoints"],
            ["Export", "export_router.py", "кнопка/запрос с UI", "notes (read)"],
        ],
    )

    doc.add_heading("Раздел 5. Авторизация", level=1)
    doc.add_paragraph(
        "Register: уникальный email, password → hash_password → User в БД → _issue_tokens: JWT access "
        "(≈15 мин, claim role) + случайный refresh → в refresh_tokens только SHA-хеш refresh. "
        "Login: verify_password → новая пара токенов. Logout: refresh revoked=true."
    )
    doc.add_paragraph(
        "На защищённых ручках Depends(get_current_user_id): Bearer, decode, UUID, загрузка User. "
        "Фронт: setSession после auth; interceptor на 401 → POST /api/auth/refresh → повтор исходного запроса."
    )

    doc.add_heading("Раздел 6. БД и ER", level=1)
    doc.add_paragraph(
        "Таблицы: users; refresh_tokens; notes; note_links; note_attachments; calendar_events; todos; sync_checkpoints "
        "(9 сущностей в models.py). Общий паттерн — user_id FK ON DELETE CASCADE. "
        "notes.is_deleted + deleted_at — корзина. note_links — направленные рёбра между двумя notes (wiki). "
        "Поля version у notes, todos, calendar_events — для инкрементальной синхронизации (sync router). "
        "linked_note_id у todo/event — опциональная связь; при удалении заметки SET NULL."
    )

    doc.add_heading("Раздел 7. Фишки", level=1)
    doc.add_paragraph(
        "Wiki: в content пишется [[Заголовок]]; после PUT/POST notes вызывается sync_links — regex ищет заголовки, "
        "находит Note того же user, пересоздаёт строки note_links. Корзина: DELETE ставит is_deleted; "
        "GET /trash; POST restore; DELETE permanent — физическое удаление. Поиск: GET /api/notes/search?q=… . "
        "Вложения: multipart → файл в uploads + NoteAttachment. Export: docx/pdf через export_service. "
        "Sync: параметры since и device_id. Задачи: GET /overdue, PATCH …/toggle без полного PUT."
    )

    doc.add_heading("Раздел 8. Стек «почему так»", level=1)
    for line in [
        "FastAPI — REST, типизация, Swagger из коробки, Depends для auth и БД.",
        "SQLAlchemy 2 + Alembic — объекты вместо сырого SQL, миграции схемы.",
        "PostgreSQL — FK, ARRAY тегов, SQL-функция поиска.",
        "React SPA — быстрый UI без перезагрузки страницы; Vite — сборка.",
        "Zustand — минимальный код для глобальной сессии.",
        "Ant Design — готовые формы, таблицы, статистика на HomePage.",
        "Docker — один сценарий для БД, API и статики фронта.",
    ]:
        doc.add_paragraph(line, style="List Bullet")

    doc.add_heading("Раздел 9. Запуск и демо", level=1)
    doc.add_paragraph("Порты: PostgreSQL 5434 (хост), API 8000, Vite 5173, Docker front 3000.")
    doc.add_paragraph("Без Docker:")
    for cmd in [
        "Docker Desktop → powershell -File Backend\\scripts\\init_db.ps1",
        "cd Backend → pip install -r requirements.txt → uvicorn app.main:app --reload --port 8000",
        "cd Front → npm install → npm run dev",
    ]:
        doc.add_paragraph(cmd, style="List Number")
    doc.add_paragraph("Docker: docker compose up --build")
    doc.add_paragraph("Демо по шагам: (1) регистрация (2) две заметки, во второй [[первая]] (3) задача + toggle "
                      "(4) событие календаря (5) удаление в корзину и restore (6) главная — цифры со счётчиков "
                      "(7) Swagger Authorize с accessToken (8) admin: UPDATE role + AdminPage.")

    doc.add_heading("Раздел 10. Указатель файлов", level=1)
    add_table(
        doc,
        ["Вопрос", "Файл"],
        [
            ["Где роутеры?", "Backend/app/main.py"],
            ["Где таблицы?", "Backend/app/models.py"],
            ["Где JWT?", "Backend/app/deps.py, services/tokens.py"],
            ["Где заметки API?", "Backend/app/routers/notes.py"],
            ["Где wiki?", "Backend/app/services/wiki_links.py"],
            ["Где маршруты React?", "Front/src/App.jsx"],
            ["Где Axios?", "Front/src/api/client.js"],
            ["Где сессия?", "Front/src/store/authStore.js"],
            ["Где guard маршрутов?", "Front/src/components/ProtectedRoute.jsx"],
            ["Где админ UI?", "Front/src/components/AdminRoute.jsx, pages/AdminPage.jsx"],
            ["Где CORS env?", "Backend/app/config.py"],
            ["Где compose?", "docker-compose.yml"],
        ],
    )

    doc.add_heading("Раздел 11. Ограничения", level=1)
    doc.add_paragraph(
        "Не реализованы: нативное мобильное приложение (есть задел sync по device_id); вход через Google/VK; "
        "WebSocket; полноценная отправка email для is_email_verified; отдельный контур E2E-тестов. "
        "Развитие: rate limiting, S3 для файлов, pytest, ротация refresh, 2FA."
    )

    doc.add_page_break()

    # --- День A ответы на чек-листы ---
    doc.add_heading("День A — ответы на чек-листы", level=1)

    doc.add_heading("A1. Каркас", level=2)
    qa(
        doc,
        "Стек front и back?",
        "Front: React, JavaScript, Ant Design, Zustand, Axios, React Router, Vite. "
        "Back: Python, FastAPI, SQLAlchemy, Pydantic, Alembic, PostgreSQL, JWT (python-jose), passlib bcrypt.",
    )
    qa(
        doc,
        "8 роутеров в main.py?",
        "auth, users, admin, notes, todos, calendar, sync, export_router — все через app.include_router.",
    )
    qa(
        doc,
        "Маршруты React?",
        "/auth/login, /auth/register; внутри layout: / (Home), /notes, /notes/:id, /calendar, /todos, /profile, /admin.",
    )
    qa(
        doc,
        "Зачем три сервиса Docker?",
        "db — данные; api — бизнес-логика и JWT; front — собранный SPA (nginx). Разделение ответственности и масштабирования.",
    )

    doc.add_heading("A2. Данные", level=2)
    qa(
        doc,
        "9 таблиц?",
        "users, refresh_tokens, notes, note_links, note_attachments, calendar_events, todos, sync_checkpoints "
        "(в models.py восемь классов сущностей + users; всего 9 таблиц).",
    )
    qa(
        doc,
        "note_links и wiki?",
        "Две FK на notes: source — кто ссылается, target — на кого; уникальная пара; строится из [[title]] в тексте.",
    )
    qa(
        doc,
        "is_deleted?",
        "Мягкое удаление заметки: скрыта из основного списка, попадает в /trash, можно restore или permanent delete.",
    )
    qa(
        doc,
        "version?",
        "Счётчик изменения сущности; sync отдаёт записи новее since и помогает клиенту не тянуть всё каждый раз.",
    )

    doc.add_heading("A3. Безопасность", level=2)
    qa(doc, "Цепочка Bearer?", "HTTPBearer credentials → _decode_token → UUID из sub/nameidentifier → User в БД.")
    qa(
        doc,
        "Access vs refresh?",
        "Access — короткий JWT в памяти/localStorage, для API. Refresh — длинный секрет, в БД хеш; обмен на новую пару.",
    )
    qa(doc, "401 на фронте?", "client.js: _retry, POST refresh с телом refreshToken, setSession, повтор запроса с новым Bearer.")
    qa(doc, "Admin?", "Backend require_admin (role != admin → 403). Front AdminRoute: role !== 'admin' → редирект.")

    doc.add_heading("A4. Бизнес", level=2)
    qa(
        doc,
        "CRUD заметок?",
        "GET /, POST, GET /{id}, PUT, DELETE (soft), GET /trash, GET /search, POST restore, DELETE permanent, POST attachments.",
    )
    qa(doc, "sync_links?", "Вызывается из notes router после сохранения content; парсит [[...]], обновляет note_links.")
    qa(doc, "todos overdue/toggle?", "GET /api/todos/overdue — просроченные; PATCH /api/todos/{id}/toggle — смена is_done.")
    qa(
        doc,
        "Календарь?",
        "Стандартный CRUD в calendar.py; linked_note_id необязателен — связь с заметкой для контекста.",
    )

    doc.add_heading("A5–A6. Фронт и практика", level=2)
    qa(
        doc,
        "Loader и ErrorMessage?",
        "HomePage.jsx строки ~38–42: if (loading) return <Loader />; ErrorMessage для error из catch Promise.all.",
    )
    qa(
        doc,
        "20 компонентов?",
        "AppLayout, AuthLayout, SideMenu, ProtectedRoute, AdminRoute, NoteCard, NoteList, SearchBar, TagChips, "
        "TrashDrawer, Loader, ErrorMessage, PageTitle, EmptyPlaceholder, ProfileCard, AdminUserTable, "
        "TodoItem, TodoCreateForm, EventItem, EventCreateForm.",
    )
    qa(
        doc,
        "9 страниц (pages/)?",
        "HomePage, NotesPage, NoteDetailPage, CalendarPage, TodosPage, ProfilePage, LoginPage, RegisterPage, AdminPage.",
    )
    qa(
        doc,
        "Swagger с токеном?",
        "Authorize → Bearer <accessToken из localStorage ticktick-auth> → вызвать GET /api/users/me или /api/notes.",
    )

    doc.add_page_break()

    # --- День B ---
    doc.add_heading("День B — ответы", level=1)

    doc.add_heading("B1. Питчи разной длины", level=2)
    doc.add_paragraph("~1 мин:", style="List Bullet")
    doc.add_paragraph(
        "TickTick — органайзер: заметки, задачи, календарь. React + FastAPI + PostgreSQL, JWT, Docker."
    )
    doc.add_paragraph("~3 мин:", style="List Bullet")
    doc.add_paragraph(
        "Описать модули (заметки с wiki и корзиной, задачи с overdue, календарь, админ), "
        "архитектуру SPA, REST, роли, Swagger, соответствие ТЗ по страницам и эндпоинтам."
    )
    doc.add_paragraph("~5 мин:", style="List Bullet")
    doc.add_paragraph(
        "Добавить демонстрацию на словах: регистрация → заметка со ссылкой → задача → корзина; "
        "упомянуть sync, export, поиск; честно назвать ограничения и перспективы."
    )

    doc.add_heading("B2. Демо — что говорить вслух", level=2)
    for step in [
        "«Сейчас регистрирую пользователя — фронт вызывает POST /api/auth/register, получаем JWT.»",
        "«Создаю заметку; в тексте [[другая]] — после сохранения сервер строит note_links.»",
        "«На главной видны счётчики — параллельные GET к notes, todos, overdue, calendar.»",
        "«Удаляю заметку — soft delete; в корзине restore или окончательное удаление.»",
        "«При истечении access фронт обновит сессию через refresh без повторного логина.»",
        "«Документация API — Swagger на /docs, схемы Pydantic.»",
    ]:
        doc.add_paragraph(step, style="List Number")

    doc.add_heading("B3. Вопросы для самопроверки — ответы", level=2)
    qa(doc, "Сколько страниц и где?", "9 экранов в pages/; маршруты объявлены в Front/src/App.jsx (строки Routes).")
    qa(doc, "Сколько компонентов?", "Ровно 20 файлов в Front/src/components/.")
    qa(
        doc,
        "Сколько эндпоинтов и где include_router?",
        "Около 35 HTTP-методов в routers + /health; подключение в main.py строки include_router.",
    )
    qa(doc, "CORS и origins?", "main.py CORSMiddleware; origins из settings.cors_origins в config.py / .env.")
    qa(doc, "bcrypt и JWT?", "services/tokens.py — hash_password/verify; deps.py — jwt.decode на защищённых ручках.")
    qa(
        doc,
        "soft vs permanent?",
        "Soft: is_deleted=true, запись остаётся. Permanent: физическое DELETE из БД, необратимо.",
    )
    qa(
        doc,
        "Зачем refresh в БД?",
        "Отзыв при logout, хранение хеша вместо токена, возможность ротации и инвалидации сессии.",
    )
    qa(doc, "Как admin?", "SQL: UPDATE users SET role = 'admin' WHERE email = '...'; или PATCH /api/admin/users/{id}/role от админа.")

    doc.add_heading("B4. «Открой файл» — что объяснить", level=2)
    b4 = [
        (
            "auth.py — _issue_tokens",
            "Показать: generate_refresh_token, RefreshToken в БД с token_hash, return AuthResponse с access и refresh.",
        ),
        (
            "deps.py — JWT",
            "get_token_payload: HTTPBearer, decode с secret/aud/iss; get_current_user: фильтр по id и deleted_at.",
        ),
        (
            "wiki_links.py",
            "WIKI_LINK = re [[...]]; sync_links удаляет старые NoteLink и создаёт новые по заголовкам заметок user.",
        ),
        (
            "notes.py — корзина",
            "delete: is_deleted; list trash: filter is_deleted; restore сбрасывает флаг; permanent — db.delete.",
        ),
        (
            "client.js — refresh",
            "response interceptor: status 401, _retry, axios.post /api/auth/refresh, setSession, return http(original).",
        ),
        (
            "authStore.js",
            "persist middleware, ключ ticktick-auth; setSession заполняет токены и role после login.",
        ),
        (
            "admin 403",
            "deps.require_admin; в admin.py зависимость AdminUser; иначе HTTP 403 Forbidden.",
        ),
        (
            "export_router.py",
            "prefix /api/notes/{note_id}/export; GET docx и pdf; проверка что note принадлежит user_id.",
        ),
    ]
    for title, text in b4:
        p = doc.add_paragraph()
        p.add_run(title).bold = True
        doc.add_paragraph(text)

    doc.add_page_break()

    doc.add_heading("2-й раунд — ответы по углублённым модулям", level=1)
    deep = [
        (
            "export + export_service",
            "export_router дергает export_service: чтение title/content заметки, формирование DOCX (python-docx) "
            "или PDF (fpdf2), отдача FileResponse.",
        ),
        (
            "sync + sync_checkpoints",
            "GET /api/sync?since=&device_id= — выборка изменённых notes/todos/events после времени; "
            "обновление sync_checkpoints.last_sync для пары user+device.",
        ),
        (
            "admin + статистика",
            "GET /api/admin/stats — агрегаты по пользователям и сущностям; GET users, PATCH role, DELETE user (soft).",
        ),
        (
            "поиск search_notes",
            "В schema.sql функция search_notes; notes.py /search вызывает через SQL/text с параметром q и user_id.",
        ),
        (
            "вложения + uploads",
            "POST multipart в notes.py; файл save в settings.uploads_dir; NoteAttachment; раздача main.mount /uploads.",
        ),
    ]
    for title, text in deep:
        p = doc.add_paragraph()
        p.add_run(title).bold = True
        doc.add_paragraph(text)

    doc.add_heading("Холодный старт — шпаргалка команд", level=1)
    doc.add_paragraph("PowerShell из корня репозитория:")
    doc.add_paragraph("1) powershell -File Backend\\scripts\\init_db.ps1")
    doc.add_paragraph("2) cd Backend; .\\.venv\\Scripts\\activate; uvicorn app.main:app --reload --port 8000")
    doc.add_paragraph("3) cd Front; npm run dev")
    doc.add_paragraph("Проверка: http://localhost:8000/health → {\"status\":\"ok\"}; фронт http://localhost:5173")

    doc.add_paragraph()
    p = doc.add_paragraph()
    p.add_run(
        f"См. также: Заметки_к_защите_TickTick.docx и Вопросы_ответы_защита_TickTick.docx на рабочем столе. "
        f"Репозиторий: {REPO}."
    ).italic = True

    doc.save(OUT_DOCX)


def main() -> None:
    build_docx()
    print(f"Saved: {OUT_DOCX}")


if __name__ == "__main__":
    main()