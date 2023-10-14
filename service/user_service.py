from schemas.user_schemas import UserCreateSchema, UserSchema, UserUpdateSchema
from service.hashing import get_password_hash
from utils.uow import AbstractUOW


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

    async def find_user_by_email(self, uow: AbstractUOW, email):
        async with uow:
            user = await uow.users.find_one(email=email)
            user = UserSchema(id=user.id, user_name=user.user_name, user_surname=user.user_surname, email=user.email)
            return user

    async def update_current_user(self, uow: AbstractUOW, user_id,  data: UserUpdateSchema):
        async with uow:
            user_dict = data.model_dump()
            user = await uow.users.edit_one(user_dict, id=user_id)
            user = UserSchema(id=user.id, user_name=user.user_name, user_surname=user.user_surname, email=user.email)
            return user
