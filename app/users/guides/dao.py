from sqlalchemy import select
from sqlalchemy.orm import selectinload

from app.dao import BaseDAO
from app.schemas import User
from app.database import async_session_maker


class GuideDAO(BaseDAO):
    model = User

    @classmethod
    async def find_all_excursion_by_guide_id(cls, guide_id: int):
        async with async_session_maker() as session:
            query = (
                select(cls.model)
                .options(selectinload(cls.model.excusrsions))
                .filter_by(id=guide_id)
            )

            result = await session.execute(query)
            return result.scalar_one_or_none().excusrsions
