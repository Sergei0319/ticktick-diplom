"""Это записная книжка с секретами и адресами: откуда брать базу данных и ключи для пропусков (JWT).
Читает файл .env, как список паролей, которые не пишут прямо в код.
Там написано, сколько минут живёт «короткий пропуск» и куда можно заходить с фронта.
Все остальные файлы спрашивают настройки только отсюда.
"""
from pydantic_settings import BaseSettings, SettingsConfigDict


# Единый объект настроек приложения (создаётся один раз в конце файла)
class Settings(BaseSettings):
    # env_file=".env" — файл рядом с запуском Backend; extra="ignore" — лишние ключи в .env не ломают загрузку
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    # Строка подключения SQLAlchemy к PostgreSQL (драйвер psycopg2); переопределяется через DATABASE_URL в .env
    database_url: str = (
        "postgresql+psycopg2://ticktick_user:ticktick_user@localhost:5434/ticktick_db"
    )
    # Секрет для подписи JWT; в проде обязательно из .env, не дефолт
    jwt_secret: str = "fx!K9mP2@qRzLw8#vNjT5&cYeA1sDhU6"
    # Претензия «кто выдал токен» (claim iss) — проверяется при decode
    jwt_issuer: str = "TickTick.Api"
    # Аудитория токена (claim aud) — для кого предназначен (фронт)
    jwt_audience: str = "TickTick.App"
    # Время жизни access-токена в минутах (короткий срок)
    access_token_minutes: int = 15
    # Срок refresh-токена в днях (длинный, хранится в БД как хеш)
    refresh_token_days: int = 30
    # Папка для загружаемых файлов вложений заметок; создаётся в main.py
    uploads_dir: str = "uploads"
    # Список origin через запятую — с каких URL браузеру разрешён CORS на API
    cors_origins: str = "http://localhost:5173,http://localhost:3000"


# Глобальный экземпляр: import settings from app.config во всех модулях
settings = Settings()