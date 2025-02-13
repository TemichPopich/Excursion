from datetime import datetime, timedelta, timezone
import jwt
import bcrypt

from app.config import settings


def encode_jwt(
    payload: dict,
    private_key: str = settings.auth.private_key_path.read_text(),
    algorithm: str = settings.auth.algorithm,
    expire_minutes: int = settings.auth.access_token_expire_minutes,
    expire_timedelta: timedelta | None = None,
):
    now = datetime.now(timezone.utc)
    to_encode = payload.copy()
    if expire_timedelta:
        expire = now + expire_timedelta
    else:
        expire = now + timedelta(minutes=expire_minutes)
    to_encode.update(exp=expire, iat=now)
    encoded = jwt.encode(payload=payload, key=private_key, algorithm=algorithm)
    return encoded


def decode_jwt(
    token: str | bytes,
    key=settings.auth.public_key_path.read_text(),
    algorithm=settings.auth.algorithm,
):
    decoded = jwt.decode(jwt=token, key=key, algorithms=[algorithm])
    return decoded


def hash_password(password: str) -> bytes:
    salt = bcrypt.gensalt()
    password_bytes = password.encode()
    return bcrypt.hashpw(password_bytes, salt)


def hash_user(user_data: dict) -> dict:
    if password := user_data.get("password"):
        user_data["password"] = hash_password(password=password)
    return user_data


def validate_pwd(password: str, hashed_password) -> bool:
    return bcrypt.checkpw(password=password.encode(), hashed_password=hashed_password)
