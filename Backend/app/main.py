"""Точка входа API TickTick.
Собирает приложение FastAPI, включает CORS,
раздаёт загруженные файлы и подключает роутеры.
Адрес /health показывает, что сервер отвечает.
"""

import os
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.config import settings
from app.routers import admin, auth, calendar, export_router, notes, sync, todos, users


os.makedirs(settings.uploads_dir, exist_ok=True)



@asynccontextmanager
async def lifespan(_: FastAPI):
    yield



app = FastAPI(title="TickTick API", lifespan=lifespan)


_origins = [o.strip() for o in settings.cors_origins.split(",") if o.strip()]

app.add_middleware(
    CORSMiddleware,
    allow_origins=_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.mount("/uploads", StaticFiles(directory=settings.uploads_dir), name="uploads")


app.include_router(auth.router)
app.include_router(users.router)
app.include_router(admin.router)
app.include_router(notes.router)
app.include_router(todos.router)
app.include_router(calendar.router)
app.include_router(sync.router)
app.include_router(export_router.router)



@app.get("/health")
def health():
    return {"status": "ok"}