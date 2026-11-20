"""Это мастерская пропусков и паролей.
Пароль при регистрации превращает в «кашу» (хеш), чтобы в базе нельзя было прочитать настоящий пароль.
Делает короткий JWT — билет на 15 минут — и длинный секретный refresh.
Проверяет подпись билета, как печать на документе.
"""
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


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(password: str, password_hash: str) -> bool:
    return pwd_context.verify(password, password_hash)


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


def generate_refresh_token() -> str:
    return secrets.token_urlsafe(64)


def hash_token(token: str) -> str:
    return hashlib.sha256(token.encode()).hexdigest().upper()


def refresh_expires_at() -> datetime:
    return datetime.now(timezone.utc) + timedelta(days=settings.refresh_token_days)