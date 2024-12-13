from app.models.excursions.schemas import GetExcursionSchema
from app.models.users.base import GetUserSchema, PostUserSchema
    
class GetGuideSchema(GetUserSchema):
    excursions: list["GetExcursionSchema"]
    role = "guide"
    
class PostGuideSchema(PostUserSchema):
    excursions = []