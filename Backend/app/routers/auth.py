from datetime import datetime, timezone

from fastapi import APIRouter, Body, HTTPException, status

from app.deps import DbSession
from app.models import RefreshToken, User
from app.schemas import AuthResponse, LoginRequest, RegisterRequest
from app.services import tokens as token_svc

router = APIRouter(prefix="/api/auth", tags=["auth"])


# Выдаёт пару access и refresh токенов
def _issue_tokens(db, user: User) -> AuthResponse:
    raw = token_svc.generate_refresh_token()
    db.add(
        RefreshToken(
            user_id=user.id,
            token_hash=token_svc.hash_token(raw),
            expires_at=token_svc.refresh_expires_at(),
        )
    )
    db.commit()
    return AuthResponse(
        access_token=token_svc.generate_access_token(user),
        refresh_token=raw,
        user_id=user.id,
        display_name=user.display_name,
        role=user.role or "user",
    )


# Регистрация нового пользователя
@router.post("/register", response_model=AuthResponse)
def register(req: RegisterRequest, db: DbSession):
    email = req.email.lower()
    if db.query(User).filter(User.email == email).first():
        raise HTTPException(status.HTTP_409_CONFLICT, detail={"message": "Email уже зарегистрирован"})
    user = User(
        email=email,
        password_hash=token_svc.hash_password(req.password),
        display_name=req.display_name,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return _issue_tokens(db, user)


# Вход по email и паролю
@router.post("/login", response_model=AuthResponse)
def login(req: LoginRequest, db: DbSession):
    user = (
        db.query(User)
        .filter(User.email == req.email.lower(), User.deleted_at.is_(None))
        .first()
    )
    if not user or not token_svc.verify_password(req.password, user.password_hash):
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, detail={"message": "Неверный email или пароль"})
    return _issue_tokens(db, user)


# Обновление пары токенов по refresh
@router.post("/refresh", response_model=AuthResponse)
def refresh(db: DbSession, refresh_token: str = Body(...)):
    token_hash = token_svc.hash_token(refresh_token)
    stored = (
        db.query(RefreshToken)
        .filter(RefreshToken.token_hash == token_hash, RefreshToken.revoked.is_(False))
        .first()
    )
    now = datetime.now(timezone.utc)
    if not stored or stored.expires_at < now:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, detail={"message": "Refresh token недействителен"})
    user = db.query(User).filter(User.id == stored.user_id).first()
    if not user:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, detail={"message": "Refresh token недействителен"})
    stored.revoked = True
    db.commit()
    return _issue_tokens(db, user)


# Выход и отзыв refresh-токена
@router.post("/logout", status_code=status.HTTP_204_NO_CONTENT)
def logout(db: DbSession, refresh_token: str = Body(...)):
    token_hash = token_svc.hash_token(refresh_token)
    stored = db.query(RefreshToken).filter(RefreshToken.token_hash == token_hash).first()
    if stored:
        stored.revoked = True
        db.commit()
