import datetime

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base, Role, struniq


class User(Base):
    phone: Mapped[struniq]
    username: Mapped[struniq]
    password: Mapped[bytes]
    email: Mapped[struniq]
    avatar: Mapped[struniq | None]
    role: Mapped[Role]
    favs: Mapped[list["Excursion"]] = relationship(
        secondary="feedbacks", back_populates="clients"
    )
    excusrsions: Mapped[list["Excursion"]] = relationship(back_populates="guide")


class Excursion(Base):
    country: Mapped[str]
    city: Mapped[str]
    date: Mapped[datetime.date]
    price: Mapped[float]
    people_count: Mapped[int]
    child_presence: Mapped[bool]
    path_diff: Mapped[str]
    desc: Mapped[str]
    name: Mapped[str]
    score: Mapped[float]
    feedback_count: Mapped[int]
    guide_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    guide: Mapped["User"] = relationship(back_populates="excusrsions")
    clients: Mapped[list["User"]] = relationship(
        secondary="feedbacks", back_populates="favs"
    )
    feedbacks: Mapped[list["Feedback"]] = relationship(back_populates="excursion")


class Feedback(Base):
    client_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), primary_key=True
    )
    exc_id: Mapped[int] = mapped_column(
        ForeignKey("excursions.id", ondelete="CASCADE"), primary_key=True
    )
    excursion: Mapped["Excursion"] = relationship(back_populates="feedbacks")
    score: Mapped[int]
    desc: Mapped[str]
