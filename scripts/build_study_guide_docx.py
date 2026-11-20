# -*- coding: utf-8 -*-
"""План изучения проекта TickTick — для печати и самостоятельной работы."""
from datetime import date
from pathlib import Path

from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.shared import Cm, Pt
from docx.oxml.ns import qn

OUT_DOCX = Path(r"C:\Users\Сергей\Desktop\План_изучения_TickTick.docx")
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


def checkbox_lines(doc: Document, items: list[str]) -> None:
    for text in items:
        doc.add_paragraph(f"☐ {text}")


def build_docx() -> None:
    doc = Document()
    set_document_style(doc)

    title = doc.add_paragraph()
    title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    tr = title.add_run("План изучения проекта TickTick\n(диплом — подготовка к защите)")
    tr.bold = True
    tr.font.size = Pt(16)

    sub = doc.add_paragraph()
    sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
    sub.add_run(f"Дата: {date.today().strftime('%d.%m.%Y')}  •  Репозиторий: «{REPO}»")

    doc.add_paragraph(
        "Этот документ — рабочая тетрадь: распечатайте, отмечайте галочками пройденные блоки "
        "и заполняйте поля «Своими словами». Цикл из двух дней повторяется: "
        "День A — изучение (3–4 ч), День B — тестовая сдача (3–4 ч)."
    )

    # Краткая ориентировка
    doc.add_heading("О проекте (направление изучения)", level=1)
    doc.add_paragraph(
        "Клиент-серверное SPA: Front (React, Ant Design, Zustand, Axios) + "
        "Backend (FastAPI, SQLAlchemy, PostgreSQL, JWT). Модули: заметки (wiki, корзина, поиск), "
        "задачи, календарь, sync, export, профиль, админ."
    )
    add_table(
        doc,
        ["Папка / файл", "Зачем смотреть"],
        [
            ["README.md", "Стек, запуск, таблица ТЗ"],
            ["Backend/app/main.py", "CORS, роутеры, uploads, /health"],
            ["Backend/app/models.py", "Все таблицы и связи"],
            ["Backend/app/deps.py", "JWT, user, admin"],
            ["Backend/app/routers/*.py", "Бизнес-API по модулям"],
            ["Front/src/App.jsx", "Маршруты SPA"],
            ["Front/src/api/client.js", "Axios, refresh при 401"],
            ["Front/src/store/authStore.js", "Сессия Zustand"],
            ["docker-compose.yml", "Docker: db, api, front"],
        ],
    )

    # Что выписать в заметки
    doc.add_heading("Что выписать в отдельные заметки (11 разделов)", level=1)
    doc.add_paragraph(
        "Ведите один блокнот или файл. После каждого этапа A дописывайте минимум 3 пункта «своими словами»."
    )
    sections_notes = [
        (
            "1. Питч (30–60 сек)",
            "Название, зачем приложение, клиент-сервер, JSON, JWT. Кто пользователь.",
        ),
        (
            "2. Архитектура",
            "Схема: Браузер → Axios → FastAPI → SQLAlchemy → PostgreSQL. Где CORS и uploads.",
        ),
        (
            "3. Соответствие ТЗ",
            "Копия таблицы из README: требование → файл → как показать на демо.",
        ),
        (
            "4. Карта модулей",
            "Таблица: функция → backend router → front page → таблицы БД.",
        ),
        (
            "5. Авторизация",
            "register/login → bcrypt → access + refresh → Bearer → deps → refresh на 401.",
        ),
        (
            "6. БД и ER",
            "9 таблиц, user_id, CASCADE, soft delete, note_links, version для sync.",
        ),
        (
            "7. Фишки",
            "[[wiki]], корзина, поиск, вложения, export docx/pdf, sync, toggle задач.",
        ),
        (
            "8. Стек «почему так»",
            "По 1 фразе: FastAPI, SQLAlchemy, React SPA, Zustand, Docker.",
        ),
        (
            "9. Запуск и демо",
            "Команды, порты 5434/8000/5173. Сценарий 7–10 мин по шагам.",
        ),
        (
            "10. Указатель файлов",
            "10–15 пар: вопрос → путь к файлу (для «откройте в IDE»).",
        ),
        (
            "11. Ограничения",
            "Чего нет (OAuth, E2E, mobile) и что бы добавили — честно для комиссии.",
        ),
    ]
    for title, hint in sections_notes:
        p = doc.add_paragraph()
        p.add_run(title).bold = True
        doc.add_paragraph(hint)
        doc.add_paragraph("Своими словами: _________________________________________________")
        doc.add_paragraph("_______________________________________________________________")

    doc.add_page_break()

    # День A
    doc.add_heading("День A — Изучение (~3,5 часа)", level=1)
    doc.add_paragraph(
        "Правило: после каждого блока — 3 bullet’а своими словами, не копипаст из docstring в коде."
    )

    add_table(
        doc,
        ["Блок", "Время", "Действия", "Отметка"],
        [
            [
                "A1. Каркас",
                "40 мин",
                "README, docker-compose.yml, main.py, App.jsx",
                "☐",
            ],
            [
                "A2. Данные",
                "50 мин",
                "models.py; заглянуть ticktick_schema.sql / Alembic",
                "☐",
            ],
            [
                "A3. Безопасность",
                "45 мин",
                "auth.py, tokens.py, deps.py; authStore.js, client.js; ProtectedRoute, AdminRoute",
                "☐",
            ],
            [
                "A4. Бизнес-логика",
                "50 мин",
                "notes.py + wiki_links.py; по ~20 мин todos.py, calendar.py",
                "☐",
            ],
            [
                "A5. Фронт",
                "35 мин",
                "pages/* и связь с API; список 20 components",
                "☐",
            ],
            [
                "A6. Практика",
                "30 мин",
                "Запуск проекта, демо-сценарий, Swagger /docs",
                "☐",
            ],
        ],
    )

    doc.add_heading("A1. Каркас — чек-лист", level=2)
    checkbox_lines(
        doc,
        [
            "Назвал стек front и back из README.",
            "Перечислил 8 подключённых роутеров в main.py.",
            "Назвал все маршруты React из App.jsx (включая /auth и /admin).",
            "Понимаю, зачем три сервиса в docker-compose.",
        ],
    )

    doc.add_heading("A2. Данные — чек-лист", level=2)
    checkbox_lines(
        doc,
        [
            "Могу назвать все 9 таблиц без подсказки.",
            "Объясняю note_links и wiki-граф.",
            "Знаю, что is_deleted у notes — корзина.",
            "Знаю, зачем поле version у notes/todos/events.",
        ],
    )

    doc.add_heading("A3. Безопасность — чек-лист", level=2)
    checkbox_lines(
        doc,
        [
            "Цепочка: Bearer → decode JWT → user в БД.",
            "Разница access (минуты) и refresh (дни, hash в БД).",
            "Фронт: interceptor 401 → refresh → повтор запроса.",
            "admin: require_admin и AdminRoute на role.",
        ],
    )

    doc.add_heading("A4. Бизнес — чек-лист", level=2)
    checkbox_lines(
        doc,
        [
            "CRUD заметок + trash + restore + permanent.",
            "Как вызывается sync_links при сохранении заметки.",
            "Эндпоинты todos: overdue, toggle.",
            "CRUD calendar_events, связь с note опциональна.",
        ],
    )

    doc.add_heading("A5–A6. Фронт и практика — чек-лист", level=2)
    checkbox_lines(
        doc,
        [
            "Нашёл Loader и ErrorMessage на примере HomePage.",
            "Прошёл демо: регистрация → 2 заметки с [[ссылкой]] → задача → календарь.",
            "Открыл Swagger и вызвал один защищённый метод с токеном.",
            "Записал команды запуска для «холодного» старта.",
        ],
    )

    doc.add_heading("Приоритет, если мало времени (< 4 ч)", level=2)
    doc.add_paragraph(
        "Не сокращать: A3 (JWT) и A4 (notes + wiki). Обязательно: A1 и таблица ТЗ."
    )

    doc.add_page_break()

    # День B
    doc.add_heading("День B — Тестовая сдача (~3,5 часа)", level=1)
    add_table(
        doc,
        ["Блок", "Время", "Действия", "Критерий", "☐"],
        [
            [
                "B1. Питч",
                "25 мин",
                "3 прогона: 1 / 3 / 5 минут по таймеру",
                "Укладываюсь, стек без пауз",
                "",
            ],
            [
                "B2. Демо",
                "45 мин",
                "Сценарий без шпаргалки; запас: Swagger + скрин",
                "UI и API согласованы",
                "",
            ],
            [
                "B3. Вопросы ТЗ",
                "60 мин",
                "Страницы, компоненты, эндпоинты, JWT, CORS, Docker, роли",
                "На ответ — файл в голове",
                "",
            ],
            [
                "B4. «Покажи в коде»",
                "40 мин",
                "8 тем: wiki, restore, admin 403, refresh, deps",
                "Объясняю Depends",
                "",
            ],
            [
                "B5. Разбор",
                "30 мин",
                "Список провалов → красная зона",
                "5 пунктов записаны",
                "",
            ],
            [
                "B6. Повтор",
                "20 мин",
                "Только красная зона + питч",
                "Самооценка ≥ 7/10",
                "",
            ],
        ],
    )

    doc.add_heading("B1 — шаблон питча (вписать и заучить)", level=2)
    doc.add_paragraph(
        "«Разработан органайзер TickTick: заметки, задачи, календарь. "
        "Клиент — React SPA, сервер — FastAPI и PostgreSQL. "
        "Авторизация JWT, роли user и admin. Развёртывание через Docker. "
        "Дополнительно: wiki-ссылки, корзина, экспорт, синхронизация.»"
    )
    doc.add_paragraph("Свой вариант: _________________________________________________________")

    doc.add_heading("B3 — вопросы для самопроверки", level=2)
    checkbox_lines(
        doc,
        [
            "Сколько страниц и где в App.jsx?",
            "Сколько компонентов в components/?",
            "Сколько примерно эндпоинтов и где include_router?",
            "Где CORS и откуда origins?",
            "Где bcrypt и где проверка JWT?",
            "Чем soft delete отличается от permanent?",
            "Зачем refresh_tokens в БД?",
            "Как назначить admin?",
        ],
    )

    doc.add_heading("B4 — задания «открой файл»", level=2)
    add_table(
        doc,
        ["Задание", "Файл", "Сделано"],
        [
            ["Показать выдачу токенов", "Backend/app/routers/auth.py", "☐"],
            ["Показать verify JWT", "Backend/app/deps.py", "☐"],
            ["Показать wiki regex", "Backend/app/services/wiki_links.py", "☐"],
            ["Показать корзину", "Backend/app/routers/notes.py", "☐"],
            ["Показать refresh на фронте", "Front/src/api/client.js", "☐"],
            ["Показать persist сессии", "Front/src/store/authStore.js", "☐"],
            ["Показать 403 admin", "Backend/app/deps.py + admin.py", "☐"],
            ["Показать export", "Backend/app/routers/export_router.py", "☐"],
        ],
    )

    doc.add_heading("B5 — красная зона (заполнить после теста)", level=2)
    for i in range(1, 6):
        doc.add_paragraph(f"{i}. _______________________________________________________________")

    doc.add_page_break()

    # Повтор цикла
    doc.add_heading("Повтор цикла (2-й раунд и дальше)", level=1)
    doc.add_paragraph("День A (2-й раз): только пункты из «красной зоны» B5 + один глубокий модуль на выбор:")
    checkbox_lines(
        doc,
        [
            "export + export_service",
            "sync + sync_checkpoints",
            "admin + статистика",
            "поиск заметок + search_notes в SQL",
            "вложения + uploads",
        ],
    )
    doc.add_paragraph(
        "День B (2-й раз): питч без листа; вопросы в случайном порядке; "
        "демо после «холодного» запуска (docker compose up или init_db + uvicorn + npm run dev)."
    )

    doc.add_heading("Связанные материалы на рабочем столе", level=1)
    doc.add_paragraph(
        "• Заметки_к_защите_TickTick.docx — готовые ответы и таблицы для защиты.\n"
        "• Вопросы_ответы_защита_TickTick.docx — банк вопросов с номерами строк в коде.\n"
        "• Этот файл — план работы и чек-листы; дополняйте рукописными пометками при печати."
    )

    doc.add_heading("Лист самоконтроля (один день — одна строка)", level=1)
    add_table(
        doc,
        ["Дата", "День A / B", "Часы", "Оценка 1–10", "Главный вывод"],
        [["", "", "", "", ""]] * 6,
    )

    doc.save(OUT_DOCX)


def main() -> None:
    build_docx()
    print(f"Saved: {OUT_DOCX}")


if __name__ == "__main__":
    main()