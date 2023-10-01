
import uuid
from fastapi import APIRouter

from api.dependencies import UOWDependency, CurrentUserDependency
from schemas.user_schemas import UserCreateSchema
from service.user_service import UserService


router = APIRouter(
    prefix="/users",
    tags=["Users"],
)


@router.post("")
async def create_user(user: UserCreateSchema, uow: UOWDependency):
    user_id = await UserService().add_user(uow=uow, user=user)
    return {"user_id": user_id}


@router.get("/{user_id}",)
async def get_user(uow: UOWDependency, user_id: uuid.UUID, current_user: CurrentUserDependency):
    user = await UserService().find_user_by_id(uow, user_id=user_id)
    return user