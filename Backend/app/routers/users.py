from fastapi import APIRouter

from app.deps import CurrentUser
from app.schemas import UserProfileDto

router = APIRouter(prefix="/api/users", tags=["users"])


@router.get("/me", response_model=UserProfileDto)
def get_me(user: CurrentUser):
    return UserProfileDto(
        id=user.id,
        email=user.email,
        display_name=user.display_name,
        role=user.role or "user",
        created_at=user.created_at,
    )