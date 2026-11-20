# TickTick (диплом)

Клиент-серверное SPA: **Front** (React, JavaScript, Ant Design, Zustand, Axios) и **Backend** (FastAPI, SQLAlchemy, PostgreSQL, Alembic, JWT).

```
!!!Диплом!!!
├── Backend/          # Python API
├── Front/            # React SPA
├── docker-compose.yml
└── README.md
```

## База данных (рекомендуется)

Скрипт пересоздаёт PostgreSQL в Docker, накатывает `Backend/ticktick_schema.sql` и миграции Alembic:

```powershell
# 1) Запусти Docker Desktop
powershell -File Backend\scripts\init_db.ps1
```

**Без Docker:** запусти службу PostgreSQL → в pgAdmin выполни `Backend/scripts/create_db_pgadmin.sql`, затем на БД `ticktick_db` — `Backend/ticktick_schema.sql` → в папке `Backend`: `alembic upgrade head`.

Файл `Backend/.env` настроен на `localhost:5434` / `ticktick_db` (порт 5434 — чтобы не конфликтовать с другим Postgres на 5432).

## Запуск без Docker

1. Сначала выполни `init_db.ps1` (или свой PostgreSQL + `ticktick_schema.sql` + `alembic upgrade head` в `Backend`).
2. `Backend`: `pip install -r requirements.txt`, `uvicorn app.main:app --reload --port 8000`.
3. `Front`: `npm install`, `npm run dev` → http://localhost:5173

Администратор: `UPDATE users SET role = 'admin' WHERE email = '...';`

## Docker

```bash
docker compose up --build
```

- API: http://localhost:8000/docs  
- Front: http://localhost:3000

## Соответствие требованиям

| Требование | Реализация |
|------------|------------|
| 5–6+ страниц | Главная, заметки, деталь, календарь, задачи, профиль, вход, регистрация, админ |
| 15–20 компонентов | `Front/src/components/` |
| Zustand | `Front/src/store/authStore.js` |
| Axios + лоадеры/ошибки | `Front/src/api/client.js` |
| 15+ эндпоинтов | auth, users, admin, notes, todos, calendar, sync, export |
| JWT + роли | user / admin |
| 7+ таблиц | см. `Backend/ticktick_schema.sql` |
| .env | `Backend/.env.example` |
| Docker | `Backend/Dockerfile`, `Front/Dockerfile`, `docker-compose.yml` |