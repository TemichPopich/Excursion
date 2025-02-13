from fastapi import APIRouter, Depends, HTTPException, status

from app.auth.dependencies import validate_rights, get_current_auth_user
from app.auth.utils import hash_user
from app.database import Role
from app.users.admins.dao import AdminDAO
from app.users.models import GetUser, PatchUser, PostUser, UserSchema
from app.users.rb import RBUser


router = APIRouter(prefix="/admins", tags=["Admins"])


@router.get("/")
async def get_all_admins(
    request_body: RBUser = Depends(),
    user: UserSchema = Depends(get_current_auth_user),
) -> list[GetUser]:
    validate_rights(user=user, roles=[Role.admin])
    admin_dict = request_body.to_dict()
    admin_dict["role"] = Role.admin
    return await AdminDAO.find_all(**admin_dict)


@router.get("/{id}")
async def get_admin_by_id(
    id: int,
    user: UserSchema = Depends(get_current_auth_user),
) -> GetUser | None:
    validate_rights(user=user, role=[Role.admin])
    return await AdminDAO.find_one_or_none_by_id(id)


@router.post("/add/")
async def register_admin(
    admin: PostUser,
    user: UserSchema = Depends(get_current_auth_user),
) -> dict:
    validate_rights(user=user, role=[Role.admin])
    admin_dict = admin.model_dump()
    admin_dict["role"] = Role.admin
    check = await AdminDAO.add(**hash_user(admin_dict))
    if check:
        return await AdminDAO.find_one_or_none_by_id(id)
    else:
        return {"message": "Adding admin error"}


@router.patch("/update/{id}")
async def update_admin(
    id: int,
    admin: PatchUser,
    user: UserSchema = Depends(get_current_auth_user),
) -> dict:
    validate_rights(user=user, role=[Role.admin])
    check = await AdminDAO.update(
        {"id": id}, **hash_user(admin.model_dump(exclude_none=True))
    )

    if check:
        return await AdminDAO.find_one_or_none_by_id(id)

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail=f"Admin {id} not found!"
    )


@router.delete("/delete/{id}")
async def delete_admin(
    id: int,
    user: UserSchema = Depends(get_current_auth_user),
) -> dict:
    validate_rights(user=user, role=[Role.admin])
    check = await AdminDAO.delete(id)
    if check:
        return await AdminDAO.find_one_or_none_by_id(id)

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail=f"Admin {id} not found!"
    )
