"""Это «главный выключатель» всего сервера: отсюда запускается программа, которая отвечает сайту.
Она соединяет все кусочки (вход, заметки, задачи) в одно целое, как пульт от телевизора.
Разрешает браузеру общаться с сервером (CORS) и кладёт загруженные файлы в папку uploads.
Есть простая проверка /health — как спросить «ты жив?», сервер отвечает «да».
"""
import os
# asynccontextmanager — декоратор для lifespan FastAPI (старт/остановка приложения)
from contextlib import asynccontextmanager

# FastAPI — точка входа ASGI-приложения
from fastapi import FastAPI
# CORSMiddleware — разрешает запросы с фронта (другой порт/домен)
from fastapi.middleware.cors import CORSMiddleware
# StaticFiles — отдача файлов с диска по URL /uploads/...
from fastapi.staticfiles import StaticFiles

# Глобальные настройки (CORS, папка uploads)
from app.config import settings
# Подключаемые модули с APIRouter в каждом файле routers/
from app.routers import admin, auth, calendar, export_router, notes, sync, todos, users

# Каталог для вложений; exist_ok=True — не падать, если уже создан
os.makedirs(settings.uploads_dir, exist_ok=True)


# Контекст жизненного цикла приложения; сейчас пустой (место под init/shutdown БД, кэша и т.д.)
@asynccontextmanager
async def lifespan(_: FastAPI):
    yield  # между yield — работающее приложение; до/после — инициализация и очистка


# Экземпляр API: title в Swagger; lifespan — хук старта/остановки
app = FastAPI(title="TickTick API", lifespan=lifespan)

# Разбиваем cors_origins на список URL без пробелов по краям
_origins = [o.strip() for o in settings.cors_origins.split(",") if o.strip()]
# Регистрируем CORS до роутеров — preflight OPTIONS и заголовки Authorization
app.add_middleware(
    CORSMiddleware,
    allow_origins=_origins,  # только перечисленные фронты, не *
    allow_credentials=True,  # куки/Authorization с credentials: include
    allow_methods=["*"],  # GET, POST, PUT, DELETE, ...
    allow_headers=["*"],  # Content-Type, Authorization, ...
)

# Статика: файлы из uploads_dir доступны по http://host:8000/uploads/имя_файла
app.mount("/uploads", StaticFiles(directory=settings.uploads_dir), name="uploads")

# Префиксы и эндпоинты задаются внутри каждого router (см. routers/*.py)
app.include_router(auth.router)  # регистрация, логин, refresh
app.include_router(users.router)  # профиль текущего пользователя
app.include_router(admin.router)  # админ: пользователи, статистика, роли
app.include_router(notes.router)  # заметки, поиск, корзина
app.include_router(todos.router)  # задачи
app.include_router(calendar.router)  # события календаря
app.include_router(sync.router)  # синхронизация чекпоинтов
app.include_router(export_router.router)  # экспорт данных


# Проверка «жив ли сервис» без БД (Docker healthcheck, мониторинг)
@app.get("/health")
def health():
    return {"status": "ok"}  # JSON-ответ 200