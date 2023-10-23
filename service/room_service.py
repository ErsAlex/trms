import uuid
from utils.uow import AbstractUOW
from schemas.room_schemas import RoomCreateSchema, RoomUpdateSchema,\
    RoomResponseSchema, UpdateRoleSchema, AccessResponse, AccessSchema
from config import can_invite, can_promote, can_update, can_kick
from models.models import Room, UserRoomAccess, RoomRole


class RoomService:
    def __init__(self, uow: AbstractUOW):
        self.uow = uow

    async def add_room(
            self,
            room_data: RoomCreateSchema,
            current_user: uuid.UUID
    ):
        async with self.uow:
            new_room_data = room_data.model_dump()
            new_room_data["owner_id"] = current_user
            new_room: Room = await self.uow.rooms.add_one(new_room_data)
            access_data = {
                "room_id": new_room.id,
                "user_id": current_user,
                "user_permissions": RoomRole.ROOM_ADMIN
            }
            await self.uow.access.add_one(access_data)
            await self.uow.commit()
            return RoomResponseSchema.model_validate(new_room)

    async def update_room(
            self,
            room_id: int,
            room_data: RoomUpdateSchema,
            current_user: uuid.UUID
    ):
        async with self.uow:
            user_access: UserRoomAccess = await self.uow.access.find_one(
                room_id=room_id,
                user_id=current_user
            )
            if user_access.user_permissions in can_update:
                room_dict = room_data.model_dump()
                room = await self.uow.rooms.edit_one(
                    room_dict,
                    id=room_id
                )
                await self.uow.commit()
                return RoomResponseSchema.model_validate(room)
            return None

    async def give_access(
            self,
            room_id: int,
            access_data: AccessSchema,
            current_user: uuid.UUID,

    ):
        async with self.uow:
            user_access: UserRoomAccess = await self.uow.access.find_one(
                room_id=room_id,
                user_id=current_user
            )
            if user_access.user_permissions in can_invite:
                data = {
                    "user_id": access_data.user_id,
                    "room_id": room_id
                }
                invited_user_access = await self.uow.access.find_one(**data)
                if invited_user_access:
                    return AccessResponse.model_validate(invited_user_access)

                new_user_access: UserRoomAccess = await self.uow.access.add_one(data)
                await self.uow.commit()
                return AccessResponse.model_validate(new_user_access)

            return None

    async def kick_user(
            self,
            access_data: AccessSchema,
            current_user: uuid.UUID,
            room_id: int

    ):
        async with self.uow:
            current_user_access: UserRoomAccess = await self.uow.access.find_one(
                room_id=room_id,
                user_id=current_user
            )
            if current_user_access.user_permissions in can_kick:
                data = {
                    "room_id": room_id,
                    "user_id": access_data.user_id
                }

                user_for_del: UserRoomAccess = await self.uow.access.find_one(**data)
                if user_for_del.user_permissions in can_kick:
                    return None
                kicked_user: UserRoomAccess = await self.uow.access.delete_one(**data)

                await self.uow.commit()
                return AccessResponse.model_validate(kicked_user)

            return None

    async def update_role(
            self,
            current_user: uuid.UUID,
            role_data: UpdateRoleSchema,
            room_id: int
    ):
        async with self.uow:
            current_user_access: UserRoomAccess = await self.uow.access.find_one(
                room_id=room_id,
                user_id=current_user
            )
            if current_user_access.user_permissions in can_promote:
                user_for_update: UserRoomAccess = await self.uow.access.find_one(
                    room_id=room_id,
                    user_id=role_data.user_id
                )
                if user_for_update.user_permissions in can_kick:
                    return None

                role_dict = role_data.model_dump()

                updated_access = await self.uow.access.edit_one(
                    role_dict,
                    id=user_for_update.id
                )
                await self.uow.commit()
                return AccessResponse.model_validate(updated_access)

            return None



