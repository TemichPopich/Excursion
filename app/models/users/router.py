from fastapi import APIRouter, HTTPException, status
from app.models.users.auth import get_password_hash
from app.models.users.base import UserDAO
from app.models.users.base import GetUserSchema


router = APIRouter(prefix='/auth', tags=['Auth'])


@router.post("/register/")
async def register_user(user_data: GetUserSchema) -> dict:
    user = await UserDAO.find_one_or_none(email=user_data.email)
    if user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail='Пользователь уже существует'
        )
    user_dict = user_data.dict()
    user_dict['password'] = get_password_hash(user_data.password)
    await UserDAO.add(**user_dict)
    return {'message': 'Вы успешно зарегистрированы!'}