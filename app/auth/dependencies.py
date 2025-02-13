from datetime import timedelta
from jwt.exceptions import InvalidTokenError
from fastapi import APIRouter, Depends, Form, HTTPException, status
from fastapi.security import (
    OAuth2PasswordBearer,
)
from pydantic import BaseModel
from app.dao import BaseDAO
from app.database import Role
from app.users.models import UserSchema
from app.auth import utils
from app.config import settings
from app.users.rb import RBUser


TOKEN_TYPE_FIELD = "type"
ACCESS_TOKEN_TYPE = "access"
REFRESH_TOKEN_TYPE = "refresh"


UNAUTHED_EXCEPTION = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED, detail="invalid token error"
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login/")


class TokenInfo(BaseModel):
    access_token: str
    refresh_token: str | None = None
    token_type: str = "Bearer"


async def validate_auth_user(
    username: str = Form(),
    password: str = Form(),
) -> UserSchema:
    rb_user = RBUser(username=username)

    try:
        users = await BaseDAO.find_all(**rb_user.to_dict())
    except:
        raise UNAUTHED_EXCEPTION

    user = users[0]

    if utils.validate_pwd(password=password, hashed_password=user.password):
        return UserSchema(
            id=user.id, username=user.username, email=user.email, role=user.role
        )

    raise UNAUTHED_EXCEPTION


def get_current_token_payload(token: str = Depends(oauth2_scheme)) -> dict:
    try:
        payload: dict = utils.decode_jwt(token=token)
    except InvalidTokenError:
        raise UNAUTHED_EXCEPTION
    return payload


def validate_token_type(type: str, payload: dict):
    token_type = payload.get(TOKEN_TYPE_FIELD)
    if token_type != type:
        raise UNAUTHED_EXCEPTION


async def get_current_user(payload: dict) -> UserSchema:
    id: int = int(payload.get("sub"))
    user = await BaseDAO.find_one_or_none_by_id(id)
    if user:
        return UserSchema(
            id=user.id, username=user.username, email=user.email, role=user.role
        )
    raise UNAUTHED_EXCEPTION


def validate_rights(user: UserSchema, roles: list[Role]):
    if user.role not in roles:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Access denied"
        )


def get_user_from_token_of_type(token_type: str):
    async def get_auth_user_from_token(
        payload: dict = Depends(get_current_token_payload),
    ) -> UserSchema:
        validate_token_type(payload=payload, type=token_type)
        return await get_current_user(payload=payload)

    return get_auth_user_from_token


get_current_auth_user = get_user_from_token_of_type(token_type=ACCESS_TOKEN_TYPE)
get_current_auth_user_for_refresh = get_user_from_token_of_type(
    token_type=REFRESH_TOKEN_TYPE
)


def create_token(
    token_type: str,
    token_data: dict,
    expire_minutes: int = settings.auth.access_token_expire_minutes,
    expire_timedelta: timedelta | None = None,
) -> str:
    payload = {TOKEN_TYPE_FIELD: token_type}
    payload.update(token_data)
    return utils.encode_jwt(
        payload=payload,
        expire_minutes=expire_minutes,
        expire_timedelta=expire_timedelta,
    )


def create_access_token(user: UserSchema) -> str:
    payload = {"sub": str(user.id), "username": user.username, "email": user.email}
    return create_token(
        token_type=ACCESS_TOKEN_TYPE,
        token_data=payload,
        expire_minutes=settings.auth.access_token_expire_minutes,
    )


def create_refresh_token(user: UserSchema) -> str:
    payload = {"sub": str(user.id)}
    return create_token(
        token_type=REFRESH_TOKEN_TYPE,
        token_data=payload,
        expire_timedelta=timedelta(days=settings.auth.refresh_token_expire_days),
    )
