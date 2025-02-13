from sqlalchemy import select
from sqlalchemy.orm import selectinload
from app.dao import BaseDAO
from app.excursions.models import Excursion
from app.schemas import User
from app.database import async_session_maker


class ClientDAO(BaseDAO):
    model = User

    @classmethod
    async def find_all_excursion_by_client_id(cls, client_id: int) -> list[Excursion]:
        async with async_session_maker() as session:
            query = (
                select(cls.model)
                .options(selectinload(cls.model.favs))
                .filter_by(id=client_id)
            )

            result = await session.execute(query)
            return result.scalar_one_or_none().favs
