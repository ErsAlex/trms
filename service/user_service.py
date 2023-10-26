import uuid

from schemas.user_schemas import UserCreateSchema, UserSchema, UserUpdateSchema
from service.hashing import get_password_hash
from utils.uow import AbstractUOW
from schemas.room_schemas import RoomResponseSchema
from schemas.task_schemas import  TaskResponseSchema



class UserService:
    def __init__(self, uow: AbstractUOW):
        self.uow = uow

    async def add_user(
            self,
            user: UserCreateSchema
    ):
        user_dict = user.model_dump()
        hashed_password = get_password_hash(user_dict["password"])
        user_dict["password"] = hashed_password
        async with self.uow:
            created_user = await self.uow.users.add_one(user_dict)
            await self.uow.commit()
            return UserSchema.model_validate(created_user)

    async def find_user_by_id(
            self,
            user_id: uuid.UUID
    ):
        async with self.uow:
            user = await self.uow.users.find_one(id=user_id)
            return UserSchema.model_validate(user)

    async def find_user_by_email(
            self,
            email: str
    ):
        async with self.uow:
            user = await self.uow.users.find_one(email=email)
            return UserSchema.from_db_model(user)

    async def update_current_user(
            self,
            user_id: uuid.UUID,
            data: UserUpdateSchema
    ):
        async with self.uow:
            user_dict = data.model_dump()
            user = await self.uow.users.edit_one(
                user_dict,
                id=user_id
            )
            return UserSchema.from_db_model(user)

    async def get_user_rooms(
            self,
            user_id: uuid.UUID
    ):
        async with self.uow:
            rooms = await self.uow.rooms.get_user_rooms(user_id)
            rooms = [RoomResponseSchema.model_validate(room) for room in rooms]
            return rooms
