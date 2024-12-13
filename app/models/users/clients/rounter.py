from fastapi import APIRouter, Depends
from app.models.users.clients.dao import ClientDAO
from app.models.users.clients.rb import RBClient
from app.models.users.clients.schemas import GetClientSchema, PostClientSchema
from app.models.users.base import GetUserSchema

router = APIRouter(prefix="/clients", tags=["clients"])


@router.get("/", summary="get list of clients")
async def get_all_clients(request_body: RBClient = Depends()) -> list[GetUserSchema]:
    return await ClientDAO.find_all(**request_body.to_dict())

@router.get("/{id}")
async def get_client(data_id: int) -> GetClientSchema | None:
    return await ClientDAO.find_client_by_id(data_id)

@router.post("/add/")
async def add_student(student: PostClientSchema) -> dict:
    check = await ClientDAO.add(**student.dict())
    if check:
        return {"message": "Клиент успешно добавлен!", "student": student}
    else:
        return {"message": "Ошибка при добавлении клиента!"}