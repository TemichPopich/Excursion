import datetime
from enum import Enum
from typing import Annotated
from sqlalchemy import ForeignKey, text
from sqlalchemy.orm import mapped_column, declared_attr, Mapped, DeclarativeBase, relationship
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncAttrs
from app.config import Role, settings

engine = create_async_engine(
    url=settings.DATABASE_URL,
    echo=True
)


session_maker = async_sessionmaker(
    engine, 
    expire_on_commit=False
)

intpk = Annotated[int, mapped_column(primary_key=True)]
created_at = Annotated[datetime.datetime, mapped_column(server_default=text("TIMEZONE('utc', now())"))]
updated_at = Annotated[datetime.datetime, mapped_column(server_default=text("TIMEZONE('utc', now())"), onupdate=datetime.datetime.utcnow)]
struniq = Annotated[str, mapped_column(unique=True)]

class Base(AsyncAttrs, DeclarativeBase):
    __abstract__ = True
    
    id: Mapped[intpk]
    created_on: Mapped[created_at]
    updated_on: Mapped[updated_at]
    
    repr_cols = 5
    
    @declared_attr.directive
    def __tablename__(cls) -> str:
        return f"{cls.__name__.lower()}s"
    
    def __repr__(self):
        cols = []
        for idx, col in self.__table__.columns.keys():
            if idx < self.repr_cols:
                cols.append(f"{col}={getattr(self, col)}")
                
        return f"<{self.__class__.__name__} {', '.join(cols)}>"

    
class Excursion(Base):
    country: Mapped[str]
    city: Mapped[str]
    date: Mapped[datetime.date]
    price: Mapped[float]
    guide_id: Mapped[int] = mapped_column(ForeignKey("guides.id", ondelete="CASCADE"))
    guide: Mapped["Guide"] = relationship(
        back_populates="excusrsions"
    ) 
    clients: Mapped[list["Client"]] = relationship(
        back_populates="favs",
        secondary="feedbacks"
    )
    
    
class Feedback(Base):
    user_id: Mapped[int] = mapped_column(
        ForeignKey("clients.id", ondelete="CASCADE"),
        primary_key=True
    )
    exc_id: Mapped[int] = mapped_column(
        ForeignKey("excursions.id", ondelete="CASCADE"),
        primary_key=True
    )
    userScore: Mapped[int]
    desc: Mapped[str]
    
    
class User(Base):
    __abstract__ = True
    
    username: Mapped[struniq]
    password: Mapped[str]
    email: Mapped[struniq]
    phone: Mapped[struniq]
    avatar: Mapped[struniq | None]
    role: Mapped[Role]
    
    
class Client(User):
    favs: Mapped[list["Excursion"]] = relationship(
        back_populates="clients",
        secondary="feedbacks"
    )
    

class Guide(User):
    excusrsions: Mapped[list["Excursion"]] = relationship(
        back_populates="guide"
    )


class Moderator(User):
    pass