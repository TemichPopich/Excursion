from sqlalchemy import select
from sqlalchemy.orm import selectinload
from app.models.users.base import UserDAO
from app.database import Guide, session_maker

class GuideDAO(UserDAO):
    model = Guide
    
    
    @classmethod
    async def find_guide_by_id(cls, id: int):
        async with session_maker() as session:
            query = (
                    select(cls.model)
                    .options(selectinload(Guide.excusrsions))
                    .filter_by(id=id)
                )
            result = await session.execute(query)
            return result.scalar_one_or_none()