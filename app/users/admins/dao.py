from app.dao import BaseDAO
from app.schemas import User


class AdminDAO(BaseDAO):
    model = User
