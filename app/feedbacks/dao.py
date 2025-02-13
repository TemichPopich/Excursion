from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.exc import SQLAlchemyError
from app.dao import BaseDAO
from app.schemas import Excursion, Feedback
from app.database import async_session_maker


class FeedbackDAO(BaseDAO):
    model = Feedback

    @classmethod
    async def find_feedback(cls, filter_by):
        async with async_session_maker() as session:
            query = select(cls.model).where(
                *[getattr(cls.model, k) == v for k, v in filter_by.items()]
            )

            result = await session.execute(query)
            return result.scalar_one_or_none()

    @classmethod
    async def change_excursion_score(cls, feedback: Feedback):
        async with async_session_maker() as session:
            async with session.begin():
                query = (
                    select(Excursion)
                    .filter_by(id=feedback.exc_id)
                    .options(selectinload(Excursion.feedbacks))
                )

                result = await session.execute(query)
                excursion = result.scalar_one()
                excursion.feedback_count += 1
                excursion.score = (
                    sum(f.score for f in excursion.feedbacks) / excursion.feedback_count
                )
                excursion.feedbacks.append(feedback)

                try:
                    await session.commit()
                except SQLAlchemyError as e:
                    await session.rollback()
                raise e
