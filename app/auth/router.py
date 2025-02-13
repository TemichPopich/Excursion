from fastapi import APIRouter, Depends

from app.auth.dependencies import (
    TokenInfo,
    create_access_token,
    create_refresh_token,
    validate_auth_user,
    get_current_auth_user_for_refresh,
    get_current_auth_user,
)
from app.users.models import UserSchema


router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/login/")
def auth_user(user: UserSchema = Depends(validate_auth_user)) -> TokenInfo:
    access_token = create_access_token(user)
    refresh_token = create_refresh_token(user)
    return TokenInfo(access_token=access_token, refresh_token=refresh_token)


@router.post("/refresh/", response_model_exclude_none=True)
def auth_refresh(
    user: UserSchema = Depends(get_current_auth_user_for_refresh),
) -> TokenInfo:
    access_token = create_access_token(user)
    return TokenInfo(access_token=access_token)


@router.get("/users/me")
async def auth_user_check(
    user: UserSchema = Depends(get_current_auth_user),
):
    return {
        "username": user.username,
        "email": user.email,
    }
