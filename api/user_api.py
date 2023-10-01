from typing import Annotated
import uuid
from fastapi import APIRouter, Depends
from schemas.user_schemas import UserSchema
from api.dependencies import UOWDependency
from schemas.user_schemas import UserCreateSchema
from service.user_service import UserService
from api.login_router import oauth2_scheme

router = APIRouter(
    prefix="/users",
    tags=["Users"],
)


@router.post("")
async def create_user(user: UserCreateSchema, uow: UOWDependency):
    user_id = await UserService().add_user(uow=uow, user=user)
    return {"user_id": user_id}


@router.get("/{user_id}")
async def get_user(uow: UOWDependency, user_id: uuid.UUID, token: str = Depends(oauth2_scheme)):
    user = await UserService().find_user_by_id(uow, user_id=user_id)
    return user