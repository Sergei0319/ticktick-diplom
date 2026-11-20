from pydantic_settings import BaseSettings, SettingsConfigDict



class Settings(BaseSettings):

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


    database_url: str = (
        "postgresql+psycopg2://ticktick_user:ticktick_user@localhost:5434/ticktick_db"
    )

    jwt_secret: str = "fx!K9mP2@qRzLw8#vNjT5&cYeA1sDhU6"

    jwt_issuer: str = "TickTick.Api"

    jwt_audience: str = "TickTick.App"

    access_token_minutes: int = 15

    refresh_token_days: int = 30

    uploads_dir: str = "uploads"

    cors_origins: str = "http://localhost:5173,http://localhost:3000"



settings = Settings()