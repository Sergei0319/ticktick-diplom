import hashlib
import secrets
import uuid
from datetime import datetime, timedelta, timezone

from jose import jwt
from passlib.context import CryptContext

from app.config import settings
from app.models import User

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
NAME_ID_CLAIM = "http://schemas.xmlsoap.org/ws/2005/05/identity/claims/nameidentifier"


# Хеширует пароль для хранения в базе
def hash_password(password: str) -> str:
    return pwd_context.hash(password)


# Сверяет пароль с хешем из базы
def verify_password(password: str, password_hash: str) -> bool:
    return pwd_context.verify(password, password_hash)


# Выпускает краткоживущий access JWT
def generate_access_token(user: User) -> str:
    now = datetime.now(timezone.utc)
    payload = {
        NAME_ID_CLAIM: str(user.id),
        "email": user.email,
        "display_name": user.display_name or "",
        "role": user.role or "user",
        "iss": settings.jwt_issuer,
        "aud": settings.jwt_audience,
        "exp": now + timedelta(minutes=settings.access_token_minutes),
        "iat": now,
    }
    return jwt.encode(payload, settings.jwt_secret, algorithm="HS256")


# Генерирует случайный refresh-токен
def generate_refresh_token() -> str:
    return secrets.token_urlsafe(64)


# Хеширует refresh-токен для хранения в базе
def hash_token(token: str) -> str:
    return hashlib.sha256(token.encode()).hexdigest().upper()


# Считает срок истечения нового refresh-токена
def refresh_expires_at() -> datetime:
    return datetime.now(timezone.utc) + timedelta(days=settings.refresh_token_days)
