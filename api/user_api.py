
import uuid
from fastapi import APIRouter

from api.dependencies import UOWDependency, CurrentUserDependency
from schemas.user_schemas import UserCreateSchema, UserUpdateSchema
from service.user_service import UserService


router = APIRouter(
    prefix="/users",
    tags=["Users"],
)


@router.post("")
async def create_user(user: UserCreateSchema, uow: UOWDependency):
    user_id = await UserService().add_user(uow=uow, user=user)
    return {"user_id": user_id}


@router.get("/me")
async def get_user(uow: UOWDependency, current_user: CurrentUserDependency):
    user = await UserService().find_user_by_id(uow, current_user)
    return user


@router.patch("/me/update/")
async def update_user(uow: UOWDependency, current_user: CurrentUserDependency, data: UserUpdateSchema):
    user = await UserService().update_current_user(uow=uow, user_id=current_user, data=data)
    return user

