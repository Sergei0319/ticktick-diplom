"""Это мост к базе данных — большому шкафу, где лежат все записи пользователей.
Создаёт «ручку» (сессию), чтобы на один запрос открыть шкаф, взять данные и закрыть.
Базовый класс Base — шаблон, по которому строятся все таблицы в models.py.
Без этого файла сервер не смог бы доставать заметки и пароли из PostgreSQL.
"""
from collections.abc import Generator

# create_engine — фабрика подключения к PostgreSQL; sessionmaker — фабрика сессий ORM
from sqlalchemy import create_engine
# DeclarativeBase — базовый класс для моделей SQLAlchemy 2.x; sessionmaker создаёт Session
from sqlalchemy.orm import DeclarativeBase, sessionmaker

# Настройки приложения (строка DATABASE_URL из .env)
from app.config import settings

# Движок SQLAlchemy: URL из настроек; pool_pre_ping — проверка «живости» соединения перед выдачей из пула
engine = create_engine(settings.database_url, pool_pre_ping=True)
# Фабрика сессий: привязка к engine; autocommit/autoflush False — явный commit во всех роутерах
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)


# Все модели (models.py) наследуются от Base — SQLAlchemy знает их метаданные для маппинга на таблицы
class Base(DeclarativeBase):
    pass  # тело пустое — достаточно наследования DeclarativeBase


# Зависимость FastAPI: одна сессия на HTTP-запрос, гарантированное закрытие в finally
def get_db() -> Generator:
    db = SessionLocal()  # открываем сессию (соединение с БД)
    try:
        yield db  # отдаём сессию в эндпоинт; после ответа выполнение продолжается ниже
    finally:
        db.close()  # закрываем сессию, возвращаем соединение в пул