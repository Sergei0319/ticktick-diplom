from collections.abc import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from app.config import settings


engine = create_engine(settings.database_url, pool_pre_ping=True)

SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)



class Base(DeclarativeBase):
    pass



# Открывает сессию базы на время запроса
def get_db() -> Generator:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
