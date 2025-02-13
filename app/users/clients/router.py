from fastapi import APIRouter, Depends, HTTPException, status
from app.auth.dependencies import get_current_auth_user, validate_rights
from app.auth.utils import hash_user
from app.database import Role
from app.users.clients.dao import ClientDAO
from app.users.models import PatchUser, PostUser, GetUser, UserSchema
from app.users.rb import RBUser


router = APIRouter(prefix="/clients", tags=["Clients"])


@router.get("/")
async def get_all_clients(
    request_body: RBUser = Depends(),
    user: UserSchema = Depends(get_current_auth_user),
) -> list[GetUser]:
    validate_rights(user=user, roles=[Role.admin, Role.guide])
    client_dict = request_body.to_dict()
    client_dict["role"] = Role.client
    return await ClientDAO.find_all(**client_dict)


@router.get("/{id}")
async def get_client_by_id(
    id: int,
    user: UserSchema = Depends(get_current_auth_user),
) -> GetUser | None:
    validate_rights(user=user, role=[Role.admin])
    return await ClientDAO.find_one_or_none_by_id(id)


@router.post("/add/")
async def register_client(
    client: PostUser,
    user: UserSchema = Depends(get_current_auth_user),
) -> dict:
    validate_rights(user=user, role=[Role.admin])
    client_dict = client.model_dump()
    client_dict["role"] = Role.client
    check = await ClientDAO.add(**hash_user(client_dict))
    if check:
        return await ClientDAO.find_one_or_none_by_id(id)
    else:
        return {"message": "Adding client error"}


@router.patch("/update/{id}")
async def update_client(
    id: int,
    client: PatchUser,
    user: UserSchema = Depends(get_current_auth_user),
) -> dict:
    validate_rights(user=user, role=[Role.admin])
    check = await ClientDAO.update(
        {"id": id}, **hash_user(client.model_dump(exclude_none=True))
    )

    if check:
        return await ClientDAO.find_one_or_none_by_id(id)

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail=f"Client {id} not found!"
    )


@router.delete("/delete/{id}")
async def delete_client(
    id: int,
    user: UserSchema = Depends(get_current_auth_user),
) -> dict:
    validate_rights(user=user, role=[Role.admin])
    check = await ClientDAO.delete(id)
    if check:
        return await ClientDAO.find_one_or_none_by_id(id)

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail=f"Client {id} not found!"
    )
