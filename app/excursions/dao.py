from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.exc import SQLAlchemyError
from app.dao import BaseDAO
from app.schemas import Excursion
from app.database import async_session_maker
from app.users.clients.dao import ClientDAO
from app.users.models import GetUser


class ExcursionDAO(BaseDAO):
    model = Excursion

    @classmethod
    async def add_client(cls, excursion_id: int, client_id: int) -> GetUser:
        async with async_session_maker() as session:
            async with session.begin():
                query = (
                    select(cls.model)
                    .options(selectinload(cls.model.clients))
                    .filter_by(id=excursion_id)
                )

                result = await session.execute(query)
                client = await ClientDAO.find_one_or_none_by_id(client_id)
                excursion = result.scalar_one_or_none()
                excursion.clients.append(client)

                try:
                    await session.commit()
                except SQLAlchemyError as e:
                    await session.rollback()
                    raise e
                return client
