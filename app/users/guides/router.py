from fastapi import APIRouter, Depends, HTTPException, status
from app.auth.utils import hash_user
from app.database import Role
from app.users.guides.dao import GuideDAO
from app.users.models import GetUser, PatchUser, PostUser, UserSchema
from app.users.rb import RBUser
from app.auth.dependencies import get_current_auth_user, validate_rights


router = APIRouter(prefix="/guides", tags=["Guides"])


@router.get("/")
async def get_all_guides(
    request_body: RBUser = Depends(),
    user: UserSchema = Depends(get_current_auth_user),
) -> list[GetUser]:
    validate_rights(user=user, roles=[Role.admin, Role.client, Role.guide])
    guide_dict = request_body.to_dict()
    guide_dict["role"] = Role.guide
    return await GuideDAO.find_all(**guide_dict)


@router.get("/{id}")
async def get_guide_by_id(
    id: int,
    user: UserSchema = Depends(get_current_auth_user),
) -> GetUser | None:
    validate_rights(user=user, role=[Role.admin])
    return await GuideDAO.find_one_or_none_by_id(id)


@router.post("/add/")
async def register_guide(
    guide: PostUser,
    user: UserSchema = Depends(get_current_auth_user),
) -> dict:
    validate_rights(user=user, role=[Role.admin])
    guide_dict = guide.model_dump()
    guide_dict["role"] = Role.guide
    check = await GuideDAO.add(**hash_user(guide_dict))
    if check:
        return {"guide": guide}
    else:
        return {"message": "Adding guide error"}


@router.patch("/update/{id}")
async def update_guide(
    id: int,
    guide: PatchUser,
    user: UserSchema = Depends(get_current_auth_user),
) -> GetUser:
    validate_rights(user=user, role=[Role.admin])
    check = await GuideDAO.update(
        {"id": id}, **hash_user(guide.model_dump(exclude_none=True))
    )

    if check:
        return await GuideDAO.find_one_or_none_by_id(id)

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail=f"Guide {id} not found!"
    )


@router.delete("/delete/{id}")
async def delete_guide(
    id: int,
    user: UserSchema = Depends(get_current_auth_user),
) -> dict:
    validate_rights(user=user, role=[Role.admin])
    check = await GuideDAO.delete(id=id)

    if check:
        return await GuideDAO.find_one_or_none_by_id(id)

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail=f"Guide {id} not found!"
    )
