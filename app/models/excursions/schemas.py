import datetime
from pydantic import BaseModel
from app.models.users.clients.schemas import *


class GetExcursionSchema(BaseModel):
    country: str
    city: str
    date: datetime.date
    price: float
    guide_id: int
    clients: list["GetClientSchema"]
    
class PostExcursionSchema(BaseModel):
    country: str
    city: str
    date: datetime.date
    price: float