from schemas.user_schemas import UserCreateSchema, UserSchema
from service.hashing import get_password_hash
from fastapi import Depends
from utils.uow import AbstractUOW
from service.hashing import verify_password
from fastapi.security import OAuth2PasswordRequestForm


class UserService:

    async def add_user(self, uow: AbstractUOW, user: UserCreateSchema):
        user_dict = user.model_dump()
        hashed_password = get_password_hash(user_dict["password"])
        user_dict["password"] = hashed_password
        async with uow:
            user_id = await uow.users.add_one(user_dict)
            await uow.commit()
            return user_id

    async def find_user_by_id(self, uow: AbstractUOW, user_id):
        async with uow:
            user = await uow.users.find_one(id=user_id)
            user = UserSchema(id=user.id, user_name=user.user_name, user_surname=user.user_surname,email=user.email)
            return user


