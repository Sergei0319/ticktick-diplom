# -*- coding: utf-8 -*-
"""Генерация PPTX по структуре дипломной презентации (TickTick)."""
from pathlib import Path

from pptx import Presentation
from pptx.util import Inches, Pt

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "presentation" / "Презентация_TickTick_диплом.pptx"

SLIDES = [
    {
        "title": "Дипломная работа",
        "body": [
            "Разработка Fullstack web-приложения «TickTick»",
            "(заметки, задачи, календарь, админка)",
            "",
            "Выполнил: студент группы [Группа / ФИО]",
            "Руководитель: [ФИО преподавателя]",
            "Компьютерная Академия ТОП",
        ],
    },
    {
        "title": "Цели и задачи проекта",
        "body": [
            "Цель: создать клиент-серверное SPA для личной продуктивности",
            "с разделением ролей user / admin и защищённым REST API.",
            "",
            "Задачи:",
            "• Разработать REST API на Python (FastAPI).",
            "• Реализовать интерактивный UI на React + Ant Design.",
            "• Организовать PostgreSQL, JWT (access + refresh), роли.",
            "• Заметки с поиском, wiki-ссылками [[...]], корзиной, export DOCX/PDF.",
            "• Контейнеризировать проект (Docker Compose).",
        ],
    },
    {
        "title": "Архитектура и технологический стек",
        "body": [
            "Backend: Python, FastAPI, SQLAlchemy, Alembic, JWT.",
            "Database: PostgreSQL.",
            "Frontend: React 18, React Router, Ant Design, Zustand, Axios.",
            "DevOps: Docker, Docker Compose, Git.",
            "",
            "Схема:",
            "React (SPA) ──JSON/HTTP──► FastAPI API ──► PostgreSQL",
            "Статика вложений: /uploads",
        ],
    },
    {
        "title": "Структура базы данных",
        "body": [
            "Основные сущности (8+ таблиц):",
            "users, refresh_tokens, notes, note_links, note_attachments,",
            "calendar_events, todos, sync_checkpoints.",
            "",
            "[ Вставить ER-диаграмму: pgAdmin / DBeaver / draw.io ]",
            "Связи: пользователь → заметки/задачи/события; note_links (граф wiki).",
        ],
    },
    {
        "title": "Реализация Backend API",
        "body": [
            "Модули: auth, users, notes, todos, calendar, admin, sync, export.",
            "15+ эндпоинтов (CRUD, поиск, корзина, вложения).",
            "JWT: access (короткий) + refresh в БД (хеш).",
            "",
            "[ Скриншот: http://localhost:8000/docs — Swagger OpenAPI ]",
        ],
    },
    {
        "title": "Клиентская часть (React)",
        "body": [
            "Маршруты: /, /notes, /notes/:id, /todos, /calendar,",
            "/profile, /admin, /auth/login, /auth/register.",
            "20 переиспользуемых компонентов в Front/src/components/.",
            "Zustand (authStore) + Axios interceptors (токены, ошибки, лоадеры).",
        ],
    },
    {
        "title": "ДЕМОНСТРАЦИЯ РАБОТЫ",
        "body": [
            "Живая демонстрация приложения",
            "(регистрация → заметки → задачи → календарь → export → админ)",
            "",
            "При сбое связи — запасная gif/видео запись экрана.",
        ],
    },
    {
        "title": "Сложные моменты и решения",
        "body": [
            "1) CORS при отдельных портах фронта и API.",
            "   → CORSMiddleware + CORS_ORIGINS в docker-compose.",
            "",
            "2) Экспорт DOCX/PDF с кириллицей в названии файла.",
            "   → Content-Disposition (filename* UTF-8); PDF — TTF DejaVu/Arial.",
            "",
            "3) Wiki-ссылки [[заголовок]] между заметками.",
            "   → services/wiki_links.sync_links при сохранении.",
        ],
    },
    {
        "title": "Заключение и планы развития",
        "body": [
            "Итог: готовое Fullstack-приложение, развёртывание через Docker Compose.",
            "",
            "Планы:",
            "• Redis-кэш для поиска и сессий.",
            "• Push / Telegram-уведомления о дедлайнах.",
            "• Мобильная адаптация / PWA.",
            "• Совместный доступ к заметкам.",
        ],
    },
    {
        "title": "Спасибо за внимание!",
        "body": [
            "Готов ответить на ваши вопросы.",
            "",
            "GitHub: github.com/Sergei0319/ticktick-diplom (ветка: экзамен)",
            "Email: [ваш email]",
        ],
    },
]


def add_slide(prs: Presentation, title: str, lines: list[str]) -> None:
    layout = prs.slide_layouts[1] if len(prs.slide_layouts) > 1 else prs.slide_layouts[0]
    slide = prs.slides.add_slide(layout)
    slide.shapes.title.text = title
    body = slide.placeholders[1].text_frame
    body.clear()
    for i, line in enumerate(lines):
        p = body.paragraphs[0] if i == 0 else body.add_paragraph()
        p.text = line
        p.font.size = Pt(18)
        if line.startswith("•"):
            p.level = 0


def main() -> None:
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    for i, s in enumerate(SLIDES):
        if i == 0 and prs.slide_layouts[0]:
            slide = prs.slides.add_slide(prs.slide_layouts[0])
            slide.shapes.title.text = s["title"]
            if len(slide.placeholders) > 1:
                tf = slide.placeholders[1].text_frame
                tf.text = "\n".join(s["body"])
            continue
        add_slide(prs, s["title"], s["body"])
    OUT.parent.mkdir(parents=True, exist_ok=True)
    prs.save(OUT)
    print(OUT)


if __name__ == "__main__":
    main()