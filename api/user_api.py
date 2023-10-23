
import uuid
from fastapi import APIRouter, HTTPException
from sqlalchemy.exc import IntegrityError
from api.dependencies import UOWDependency, CurrentUserDependency
from schemas.user_schemas import UserCreateSchema, UserUpdateSchema, UserSchema
from service.user_service import UserService


router = APIRouter(
    prefix="/users",
    tags=["Users"],
)


@router.post("")
async def create_user(
        user: UserCreateSchema,
        uow: UOWDependency
):
    try:
        user: UserSchema = await UserService(uow).add_user(user)
        return user
    except IntegrityError as err:
        raise HTTPException(status_code=503, detail=f"Database error: {err}")


@router.get("/me")
async def get_user(
        uow: UOWDependency,
        current_user: CurrentUserDependency
):
    try:
        user: UserSchema = await UserService(uow).find_user_by_id(current_user)
        return user
    except IntegrityError as err:
        raise HTTPException(status_code=503, detail=f"Database error: {err}")


@router.patch("/me/update/")
async def update_user(
        uow: UOWDependency,
        current_user: CurrentUserDependency,
        data: UserUpdateSchema
):
    try:
        user: UserSchema = await UserService(uow).update_current_user(
            current_user,
            data
        )
        return user
    except IntegrityError as err:
        raise HTTPException(status_code=503, detail=f"Database error: {err}")

