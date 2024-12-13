from sqlalchemy import select
from sqlalchemy.orm import selectinload
from app.models.users.base import UserDAO
from app.database import Client, session_maker

class ClientDAO(UserDAO):
    model = Client
    
    
    @classmethod
    async def find_client_by_id(cls, id: int):
        async with session_maker() as session:
            query = (
                    select(cls.model)
                    .options(selectinload(Client.favs))
                    .filter_by(id=id)
                )
            result = await session.execute(query)
            return result.scalar_one_or_none()