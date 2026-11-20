# -*- coding: utf-8 -*-
"""Генерация .docx: ТЗ проекта, стек, архитектура, соответствие требованиям КА ТОП."""
from datetime import date
from pathlib import Path

from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.shared import Pt

OUT = Path(r"C:\Users\Сергей\Desktop\Соответствие_ТЗ_и_репозитория_TickTick.docx")
REPO = r"C:\Users\Сергей\Desktop\!!!Диплом!!!"


def add_heading(doc, text, level=1):
    doc.add_heading(text, level=level)


def add_qa(doc, question, answer):
    p = doc.add_paragraph()
    r = p.add_run("Требование: ")
    r.bold = True
    p.add_run(question)
    p = doc.add_paragraph()
    r = p.add_run("Выполнение в проекте: ")
    r.bold = True
    p.add_run(answer)


def add_table(doc, headers, rows):
    table = doc.add_table(rows=1, cols=len(headers))
    table.style = "Table Grid"
    hdr = table.rows[0].cells
    for i, h in enumerate(headers):
        hdr[i].text = h
    for row in rows:
        cells = table.add_row().cells
        for i, val in enumerate(row):
            cells[i].text = val
    doc.add_paragraph()


def main():
    doc = Document()
    style = doc.styles["Normal"]
    style.font.name = "Times New Roman"
    style.font.size = Pt(12)

    title = doc.add_paragraph()
    title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = title.add_run(
        "Дипломный проект\n"
        "«TickTick — веб-планировщик заметок, задач и календаря»\n\n"
        "Техническое задание · Стек · Архитектура\n"
        "Соответствие требованиям Компьютерной Академии ТОП"
    )
    r.bold = True
    r.font.size = Pt(14)

    sub = doc.add_paragraph()
    sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
    sub.add_run(f"Дата: {date.today().strftime('%d.%m.%Y')}\n")
    sub.add_run(f"Исходный код: {REPO}")

    # --- РАЗДЕЛ I: ТЗ ПРОЕКТА ---
    add_heading(doc, "Раздел I. Техническое задание проекта", 1)

    add_heading(doc, "1.1. Наименование и суть", 2)
    doc.add_paragraph(
        "Наименование: TickTick (учебное fullstack web-приложение).\n"
        "Суть: клиент-серверная система личной продуктивности — пользователь ведёт "
        "заметки с тегами и вложениями, планирует задачи и события календаря, "
        "синхронизирует данные между устройствами; администратор управляет пользователями "
        "и видит сводную статистику. Тип приложения по классификации курса: "
        "«клиент-серверное веб-приложение» (аналог личного кабинета / контент-системы)."
    )

    add_heading(doc, "1.2. Цели и задачи", 2)
    for item in [
        "Обеспечить разделённую архитектуру SPA + REST API на Python и React.",
        "Реализовать безопасную аутентификацию (JWT, роли user/admin).",
        "Обеспечить CRUD основных сущностей: заметки, задачи, события календаря.",
        "Реализовать поиск, корзину заметок, экспорт в DOCX/PDF, загрузку вложений.",
        "Развернуть проект в Docker (БД + API + фронтенд).",
    ]:
        doc.add_paragraph(item, style="List Bullet")

    add_heading(doc, "1.3. Пользователи и роли", 2)
    add_table(
        doc,
        ["Роль", "Возможности"],
        [
            ("user", "Регистрация, заметки, задачи, календарь, профиль, поиск, экспорт"),
            ("admin", "Всё выше + панель /admin: пользователи, статистика, смена ролей, soft-delete"),
        ],
    )

    add_heading(doc, "1.4. Функциональные требования (кратко)", 2)
    func = [
        "Регистрация и вход по email/паролю; обновление access-токена через refresh.",
        "Список и детальная страница заметки; создание, редактирование, удаление (корзина).",
        "Полнотекстовый поиск заметок (функция search_notes в PostgreSQL).",
        "CRUD задач с приоритетом, сроком, отметкой выполнения; список просроченных.",
        "CRUD событий календаря с привязкой к заметке.",
        "Профиль текущего пользователя.",
        "Админ: статистика, список пользователей, смена роли, удаление пользователя.",
        "Эндпоинт синхронизации изменений с момента since.",
        "Выгрузка заметки в DOCX/PDF.",
    ]
    for f in func:
        doc.add_paragraph(f, style="List Bullet")

    add_heading(doc, "1.5. Нефункциональные требования", 2)
    doc.add_paragraph(
        "JSON REST; CORS для фронтенда; секреты в .env; валидация запросов Pydantic; "
        "пароли только в виде bcrypt-хеша; миграции Alembic; документация OpenAPI (/docs)."
    )

    # --- РАЗДЕЛ II: СТЕК ---
    add_heading(doc, "Раздел II. Стек технологий", 1)
    add_table(
        doc,
        ["Слой", "Технология", "Версия / файл"],
        [
            ("Backend", "Python, FastAPI", "3.12, Backend/requirements.txt"),
            ("ORM", "SQLAlchemy 2.0", "Backend/app/models.py"),
            ("Валидация API", "Pydantic", "Backend/app/schemas.py"),
            ("Миграции", "Alembic", "Backend/migrations/, alembic.ini"),
            ("СУБД", "PostgreSQL 15", "ticktick_schema.sql, docker-compose db"),
            ("Auth", "JWT (access+refresh), bcrypt", "tokens.py, auth.py, deps.py"),
            ("Frontend", "React 18, Vite", "Front/package.json"),
            ("Навигация", "React Router 6", "Front/src/App.jsx"),
            ("UI", "Ant Design 5", "страницы и формы"),
            ("HTTP-клиент", "Axios", "Front/src/api/client.js"),
            ("State", "Zustand (+ persist)", "Front/src/store/authStore.js"),
            ("DevOps", "Docker, docker-compose", "Backend/Dockerfile, Front/Dockerfile"),
            ("Переменные", ".env", "Backend/.env.example, Front/.env (VITE_API_URL)"),
        ],
    )

    # --- РАЗДЕЛ III: АРХИТЕКТУРА ---
    add_heading(doc, "Раздел III. Архитектура", 1)

    add_heading(doc, "3.1. Общая схема", 2)
    doc.add_paragraph(
        "Трёхзвенная клиент-серверная архитектура SPA:\n\n"
        "[Браузер] → React SPA (порт 5173 dev / 3000 Docker)\n"
        "         ↓ HTTPS/HTTP, JSON, Authorization: Bearer\n"
        "[FastAPI] REST API (порт 8000) — роутеры app/routers/*, бизнес-логика services/*\n"
        "         ↓ SQLAlchemy\n"
        "[PostgreSQL] (порт 5434 с хоста / 5432 в compose-сети)\n\n"
        "Статические вложения: каталог uploads, раздача через StaticFiles /uploads."
    )

    add_heading(doc, "3.2. Структура репозитория", 2)
    doc.add_paragraph(
        "!!!Диплом!!!/\n"
        "├── Backend/app/ — main.py, config, db, models, schemas, deps\n"
        "│   ├── routers/ — auth, users, notes, todos, calendar, admin, sync, export\n"
        "│   └── services/ — tokens, wiki_links, export_service\n"
        "├── Front/src/ — pages/, components/, api/, store/\n"
        "├── docker-compose.yml — сервисы db, api, front\n"
        "└── Backend/ticktick_schema.sql — начальная схема БД"
    )

    add_heading(doc, "3.3. Поток аутентификации", 2)
    doc.add_paragraph(
        "1) POST /api/auth/register или /login → AuthResponse (accessToken, refreshToken).\n"
        "2) Zustand сохраняет токены (localStorage через persist middleware).\n"
        "3) Axios interceptor добавляет Bearer к каждому запросу.\n"
        "4) При 401 — автоматический POST /api/auth/refresh; при неудаче — выход.\n"
        "5) AdminRoute и deps.AdminUser проверяют role=admin на бэкенде и фронте."
    )

    add_heading(doc, "3.4. CORS и интеграция", 2)
    doc.add_paragraph(
        "CORSMiddleware в main.py: origins из CORS_ORIGINS (.env), credentials=True. "
        "Фронт обращается к VITE_API_URL; при Docker — front за nginx, API на :8000."
    )

    # --- РАЗДЕЛ IV: СООТВЕТСТВИЕ ТРЕБОВАНИЯМ КА ТОП ---
    add_heading(doc, "Раздел IV. Соответствие техническим требованиям КА ТОП", 1)

    add_heading(doc, "4.0. Базовые требования курса", 2)
    add_qa(
        doc,
        "Клиент-серверное веб-приложение; Backend — чистый API; SPA; JSON REST; CORS.",
        "Выполнено. FastAPI без серверного рендера HTML; React SPA; client.js + CORS в main.py.",
    )
    add_qa(
        doc,
        "PostgreSQL + ORM + миграции; React Router + UI-библиотека; FastAPI или DRF.",
        "PostgreSQL, SQLAlchemy, Alembic; React Router, Ant Design; FastAPI.",
    )

    add_heading(doc, "4.1. Frontend (React)", 2)
    pages = [
        ("/ (index)", "HomePage.jsx", "Главная — дашборд, счётчики"),
        ("/notes", "NotesPage.jsx", "Лента заметок, поиск, теги, корзина"),
        ("/notes/:id", "NoteDetailPage.jsx", "Деталь объекта (заметка) + экспорт"),
        ("/calendar", "CalendarPage.jsx", "Создание контента — события"),
        ("/todos", "TodosPage.jsx", "Создание контента — задачи"),
        ("/profile", "ProfilePage.jsx", "Личный кабинет"),
        ("/auth/login", "LoginPage.jsx", "Авторизация"),
        ("/auth/register", "RegisterPage.jsx", "Регистрация"),
        ("/admin", "AdminPage.jsx", "Панель администратора"),
    ]
    add_qa(
        doc,
        "Не менее 5–6 полноценных страниц (Routes).",
        f"Реализовано {len(pages)} маршрутов (см. таблицу). Файл маршрутизации: Front/src/App.jsx.",
    )
    add_table(doc, ["Маршрут", "Компонент", "Назначение"], pages)

    component_files = [
        "AdminRoute", "AdminUserTable", "AppLayout", "AuthLayout", "EmptyPlaceholder",
        "ErrorMessage", "EventCreateForm", "EventItem", "Loader", "NoteCard", "NoteList",
        "PageTitle", "ProfileCard", "ProtectedRoute", "SearchBar", "SideMenu", "TagChips",
        "TodoCreateForm", "TodoItem", "TrashDrawer",
    ]
    add_qa(
        doc,
        "15–20 переиспользуемых компонентов; декомпозиция UI.",
        f"Front/src/components/ — {len(component_files)} компонентов в отдельных файлах; "
        "кнопки/инпуты — Ant Design, обёртки Loader, ErrorMessage, PageTitle.",
    )
    doc.add_paragraph("Список компонентов: " + ", ".join(component_files) + ".")

    add_qa(
        doc,
        "useState, useEffect; желательно Zustand/Redux для сессии.",
        "Локальное состояние на страницах (useState/useEffect). "
        "Глобальная сессия: Zustand authStore.js (accessToken, refreshToken, setSession, logout).",
    )
    add_qa(
        doc,
        "Axios/Fetch + лоадеры и обработка ошибок.",
        "api/client.js — Axios, timeout, refresh при 401. Loader.jsx, ErrorMessage.jsx на страницах.",
    )

    add_heading(doc, "4.2. Backend (Python API)", 2)
    endpoints_sample = [
        "POST /api/auth/register, /login, /refresh, /logout",
        "GET /api/users/me",
        "GET/POST/PUT/DELETE /api/notes (+ trash, restore, search, attachments)",
        "GET /api/notes/{id}/export/docx, /pdf",
        "CRUD /api/todos (+ /overdue, /toggle)",
        "CRUD /api/calendar",
        "GET /api/sync",
        "GET /api/admin/stats, /users; PATCH role; DELETE user",
        "GET /health",
    ]
    add_qa(
        doc,
        "Не менее 15 эндпоинтов; CRUD для основных сущностей.",
        "Более 35 HTTP-операций в routers/*.py. Полный CRUD: notes, todos, calendar. "
        "Сводка: Swagger http://localhost:8000/docs.",
    )
    for e in endpoints_sample:
        doc.add_paragraph(e, style="List Bullet")

    add_qa(
        doc,
        "Регистрация, bcrypt/argon2, JWT, роли user/admin, Pydantic-валидация.",
        "passlib+bcrypt, password_hash в users; JWT access/refresh; role user|admin; "
        "schemas RegisterRequest, NoteDto и др.; 422 при невалидных данных.",
    )

    add_heading(doc, "4.3. База данных", 2)
    tables = [
        "users", "refresh_tokens", "notes", "note_links", "note_attachments",
        "calendar_events", "todos", "sync_checkpoints",
    ]
    add_qa(
        doc,
        "5–7+ связанных таблиц; FK; One-to-Many и Many-to-Many.",
        f"8 таблиц в ticktick_schema.sql. "
        "One-to-Many: user → notes, todos, events; note → attachments. "
        "Many-to-Many (граф): note_links (source_note_id ↔ target_note_id). "
        "Миграции: Alembic (например add_user_role).",
    )
    doc.add_paragraph("Таблицы: " + ", ".join(tables) + ".")

    add_heading(doc, "4.4. Инфраструктура и DevOps", 2)
    add_qa(
        doc,
        ".env для секретов и БД; Dockerfile×2; docker-compose с БД; запуск одной командой.",
        "Backend/.env.example (DATABASE_URL, JWT_*, CORS_ORIGINS). "
        "Backend/Dockerfile, Front/Dockerfile, docker-compose.yml (db, api, front). "
        "Команда: docker compose up --build или scripts/init_db.ps1.",
    )

    # --- РАЗДЕЛ V: ПРЕДЗАЩИТА И ЗАЩИТА ---
    add_heading(doc, "Раздел V. Материалы к предзащите и защите", 1)
    add_table(
        doc,
        ["Требование", "Подготовка по проекту TickTick"],
        [
            ("Исходный код", f"Папка {REPO}; готовность открыть routers/, pages/, models.py"),
            ("Презентация PPT", "Цели, стек, архитектура (разделы I–III), скриншоты UI, схема БД"),
            ("Рабочее ДЕМО", "docker compose up или init_db.ps1 + npm run dev; сценарий ниже"),
            ("Регламент ~15 мин", "1) Архитектура 2–3 мин 2) Регистрация/логин 3) Заметки CRUD 4) Задачи/календарь 5) Админ"),
            ("Вопросы комиссии", "JWT, FK в БД, difference SPA vs SSR, зачем Zustand, структура FastAPI router"),
        ],
    )

    add_heading(doc, "5.1. Сценарий демонстрации (обязательно)", 2)
    demo = [
        "Открыть главную — счётчики заметок/задач/событий.",
        "Создать заметку, открыть деталь, поиск по тексту.",
        "Удалить в корзину, восстановить из TrashDrawer.",
        "Скачать DOCX/PDF (export).",
        "Создать задачу и событие календаря.",
        "Профиль пользователя.",
        "Назначить admin в БД, показать /admin — пользователи и статистика.",
        "Показать Swagger /docs или фрагмент кода по запросу комиссии.",
    ]
    for i, d in enumerate(demo, 1):
        doc.add_paragraph(f"{i}. {d}")

    # --- РАЗДЕЛ VI: ИТОГ ---
    add_heading(doc, "Раздел VI. Итоговая матрица соответствия", 1)
    add_table(
        doc,
        ["Критерий КА ТОП", "Статус", "Доказательство в репозитории"],
        [
            ("Клиент-сервер + SPA + REST + CORS", "Да", "README, main.py, client.js"),
            ("FastAPI + PostgreSQL + ORM + миграции", "Да", "models.py, Alembic"),
            ("React Router + Ant Design", "Да", "App.jsx, package.json"),
            ("≥5–6 страниц", "Да (9)", "pages/*.jsx"),
            ("≥15 компонентов", "Да (20)", "components/*.jsx"),
            ("Zustand + Axios + Loader/Error", "Да", "authStore.js, client.js"),
            ("≥15 эндпоинтов + CRUD", "Да", "routers/*.py, /docs"),
            ("JWT + bcrypt + роли", "Да", "auth.py, deps.py"),
            ("≥5–7 таблиц + FK + связи", "Да (8)", "ticktick_schema.sql"),
            (".env + Docker×2 + compose", "Да", "docker-compose.yml"),
            ("Демо без сбоя", "Готовить заранее", "Раздел V.1"),
        ],
    )

    add_heading(doc, "Приложение. Ответы на типовые вопросы комиссии", 1)
    faq = [
        (
            "Почему FastAPI, а не Django?",
            "Требование курса допускает FastAPI; выбрана явная схема Pydantic и автодокументация OpenAPI.",
        ),
        (
            "Где Many-to-Many?",
            "Таблица note_links связывает две заметки (wiki-ссылки); это M:N через промежуточную таблицу.",
        ),
        (
            "Чем заменена «корзина магазина»?",
            "Корзина удалённых заметок (trash) + оформление контента через создание заметок/задач/событий.",
        ),
        (
            "Где хранится JWT?",
            "localStorage через Zustand persist (access/refresh); альтернатива httpOnly — возможное улучшение.",
        ),
    ]
    for q, a in faq:
        add_qa(doc, q, a)

    OUT.parent.mkdir(parents=True, exist_ok=True)
    doc.save(OUT)
    print(f"Saved: {OUT}")


if __name__ == "__main__":
    main()