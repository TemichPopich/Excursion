from fastapi import APIRouter, Depends
from app.models.users.guides.dao import GuideDAO
from app.models.users.guides.rb import RBGuide
from app.models.users.guides.schemas import GetGuideSchema, PostGuideSchema


router = APIRouter(prefix="/guides", tags=["guides"])


@router.get("/", summary="get list of clients")
async def get_all_guides(request_body: RBGuide = Depends()) -> list[GetGuideSchema]:
    return await GuideDAO.find_all(**request_body.to_dict())

@router.get("/{id}")
async def get_guide(data_id: int) -> GetGuideSchema | None:
    return await GuideDAO.find_guide_by_id(data_id)

@router.post("/add/")
async def add_guide(guide: PostGuideSchema) -> dict:
    check = await GuideDAO.add(**guide.dict())
    if check:
        return {"message": "Клиент успешно добавлен!", "guide": guide}
    else:
        return {"message": "Ошибка при добавлении клиента!"}