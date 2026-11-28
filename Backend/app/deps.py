import uuid
from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session

from app.config import settings
from app.db import get_db
from app.models import User

security = HTTPBearer(auto_error=False)
NAME_ID_CLAIM = "http://schemas.xmlsoap.org/ws/2005/05/identity/claims/nameidentifier"


# Проверяет подпись, срок, аудиторию и издателя access-токена
def _decode_token(token: str) -> dict:
    return jwt.decode(
        token,
        settings.jwt_secret,
        algorithms=["HS256"],
        audience=settings.jwt_audience,
        issuer=settings.jwt_issuer,
    )


# Достаёт и проверяет токен из заголовка Authorization
def get_token_payload(
    creds: Annotated[HTTPAuthorizationCredentials | None, Depends(security)],
) -> dict:
    if creds is None or creds.scheme.lower() != "bearer":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Требуется авторизация")
    try:
        return _decode_token(creds.credentials)
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Недействительный токен")


# Берёт id пользователя из payload токена
def get_current_user_id(payload: Annotated[dict, Depends(get_token_payload)]) -> uuid.UUID:
    raw = payload.get(NAME_ID_CLAIM) or payload.get("sub")
    if not raw:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    try:
        return uuid.UUID(str(raw))
    except ValueError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)


# Загружает живого пользователя по id из токена
def get_current_user(
    user_id: Annotated[uuid.UUID, Depends(get_current_user_id)],
    db: Annotated[Session, Depends(get_db)],
) -> User:
    user = db.query(User).filter(User.id == user_id, User.deleted_at.is_(None)).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    return user


# Пускает дальше только пользователя с ролью admin
def require_admin(user: Annotated[User, Depends(get_current_user)]) -> User:
    if user.role != "admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Доступ только для администратора")
    return user


DbSession = Annotated[Session, Depends(get_db)]
UserId = Annotated[uuid.UUID, Depends(get_current_user_id)]
CurrentUser = Annotated[User, Depends(get_current_user)]
AdminUser = Annotated[User, Depends(require_admin)]
