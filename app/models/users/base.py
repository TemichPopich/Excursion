import re
from pydantic import BaseModel, ConfigDict, EmailStr, Field, validator
from app.config import Role
from app.database import session_maker
from sqlalchemy import select, exc


class UserDAO:
    model = None
    
    @classmethod
    async def find_all(cls,  **filter_by):
        async with session_maker() as session:
            query = (
                select(cls.model)
                # .options(selectinload(Client.favs))
                .filter_by(**filter_by)
            )
            result = await session.execute(query)
            return result.scalars().all()
        
        
    @classmethod
    async def find_one_or_none_by_id(cls, data_id: int):
        async with session_maker() as session:
            query = (
                select(cls.model)
                .filter_by(id=data_id))
            result = await session.execute(query)
            return result.scalar_one_or_none()  
        
        
    @classmethod
    async def add(cls, **values):
        async with session_maker() as session:
            async with session.begin():
                new_instance = cls.model(**values)
                session.add(new_instance)
                await session.flush()
                try:
                    await session.commit()
                except exc.SQLAlchemyError as e:
                    await session.rollback()
                    raise e
            return new_instance
        
        
class PostUserSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    __abstarct__ = True
    
    username: str = Field(..., min_length=1, max_length=50)
    password: str
    email: EmailStr
    phone: str
    avatar = None
    role = "client"
    
    @validator("phone")
    def validate_phone_number(cls, value):
        if not re.match(r'^\+\d{1,15}$', value):
            raise ValueError('Номер телефона должен начинаться с "+" и содержать от 1 до 15 цифр')
        return value  


class GetUserSchema(PostUserSchema):
    id: int   
    
    
class RBUser:
    def __init__(self, username: int | None = None,
                 id: int | None = None):
        self.username = username
        self.id = id
        
    def to_dict(self) -> dict:
        data = {'id': self.id, 'username': self.username}
        filtered_data = {key: value for key, value in data.items() if value is not None}
        return filtered_data 