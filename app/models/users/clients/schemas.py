from app.models.excursions.schemas import GetExcursionSchema
from app.models.users.base import GetUserSchema, PostUserSchema
    
class GetClientSchema(GetUserSchema):
    favs: list["GetExcursionSchema"]
    
class PostClientSchema(PostUserSchema):
    favs: list["GetExcursionSchema"] = []