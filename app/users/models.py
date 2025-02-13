import re
from pydantic import EmailStr, validator

from app.database import Role
from app.models import TuneModel


class UserSchema(TuneModel):
    id: int
    username: str
    email: EmailStr
    role: Role


class PostUser(TuneModel):
    phone: str
    username: str
    password: str
    email: EmailStr
    avatar: str | None

    @validator("phone")
    def validate_phone_number(cls, value):
        if not re.match(r"^\+\d{1,15}$", value):
            raise ValueError(
                'Номер телефона должен начинаться с "+" и содержать от 1 до 15 цифр'
            )
        return value


class PatchUser(TuneModel):
    phone: str | None = None
    username: str | None = None
    password: str | None = None
    email: EmailStr | None = None
    avatar: str | None = None

    @validator("phone")
    def validate_phone_number(cls, value):
        if not re.match(r"^\+\d{1,15}$", value):
            raise ValueError(
                'Номер телефона должен начинаться с "+" и содержать от 1 до 15 цифр'
            )
        return value


class GetUser(PostUser):
    id: int
    role: Role
