from fastapi import APIRouter, Depends, HTTPException, status

from app.database import Role
from app.excursions.dao import ExcursionDAO
from app.excursions.models import Excursion, PostExcursion
from app.excursions.rb import RBExcursion
from app.users.guides.dao import GuideDAO
from app.users.clients.dao import ClientDAO
from app.users.models import GetUser, UserSchema
from app.auth.dependencies import get_current_auth_user, validate_rights

router = APIRouter(prefix="/excursions", tags=["Excursions"])


@router.get("/")
async def get_all_excursion(
    request_body: RBExcursion = Depends(),
) -> list[Excursion]:
    excursion_dict = request_body.to_dict()
    return await ClientDAO.find_all(**excursion_dict)


@router.get("/client/")
async def get_client_with_excursion(
    user: UserSchema = Depends(get_current_auth_user),
) -> list[Excursion]:
    validate_rights(user=user, roles=[Role.client])
    return await ClientDAO.find_all_excursion_by_client_id(user.id)


@router.get("/client/add/{id}")
async def get_client_with_excursion(
    id: int,
    user: UserSchema = Depends(get_current_auth_user),
) -> GetUser:
    validate_rights(user=user, roles=[Role.client])
    return await ExcursionDAO.add_client(id, user.id)


@router.get("/guide/")
async def get_guide_with_excursions(
    user: UserSchema = Depends(get_current_auth_user),
) -> list[Excursion]:
    validate_rights(user=user, roles=[Role.guide])
    return await GuideDAO.find_all_excursion_by_guide_id(user.id)


@router.post("/guide/create/")
async def create_excursion(
    excursion: PostExcursion,
    user: UserSchema = Depends(get_current_auth_user),
) -> dict:
    validate_rights(user=user, roles=[Role.guide])
    excursion_dict = excursion.model_dump()
    excursion_dict["guide_id"] = user.id
    check = await ExcursionDAO.add(**excursion_dict)
    if check:
        return {"excursion": excursion}
    else:
        return {"message": "Adding excursion error"}


@router.patch("/guide/update/")
async def update_excursion(
    id: int,
    excursion: PostExcursion,
    user: UserSchema = Depends(get_current_auth_user),
) -> Excursion:
    validate_rights(user=user, role=[Role.guide])
    check = await GuideDAO.update({"id": id}, **excursion.model_dump(exclude_none=True))

    if check:
        return await GuideDAO.find_one_or_none_by_id(id)

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail=f"Excursion {id} not found!"
    )


@router.delete("/delete/{id}")
async def delete_excursion(
    id: int,
    user: UserSchema = Depends(get_current_auth_user),
) -> dict:
    validate_rights(user=user, role=[Role.admin, Role.guide])
    check = await ExcursionDAO.delete(id=id)

    if check:
        return await ExcursionDAO.find_one_or_none_by_id(id)

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail=f"Excursion {id} not found!"
    )
