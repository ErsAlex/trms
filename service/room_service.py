
from utils.uow import AbstractUOW
from schemas.room_schemas import RoomCreateSchema, RoomUpdateSchema, RoomSchema, UserAppealSchema, UpdateRoleSchema, UpdatedRoleResponseSchema
from service.access import can_invite, can_promote,can_give_tasks, can_update, can_kick
from models.models import User, RoomAccess, Room

class RoomService:
    async def add_room(self, uow: AbstractUOW, room_data: RoomCreateSchema, owner):
        room_dict = room_data.model_dump()
        room_dict["owner_id"] = owner
        async with uow:
            room_id = await uow.rooms.add_one(room_dict)
            access_dict = {"user_id": owner, "room_id": room_id, 'user_permissions': "ROOM_ADMIN"}
            await uow.access.add_one(access_dict)
            await uow.commit()
            return room_id

    async def update_room(self, uow:AbstractUOW, room_id,
                          room_data: RoomUpdateSchema, current_user):
        # тут сначала должен идти запрос в редис и только потом в бд
        async with uow:
            params = {"room_id": room_id, "user_id": current_user}
            access: RoomAccess = await uow.access.find_one(**params)
            if access.user_permissions in can_update:
                room_dict = room_data.model_dump()
                room = await uow.rooms.edit_one(room_dict, id=room_id)
                await uow.commit()
                room = RoomSchema(id=room.id, name=room.name, description=room.description,
                                      date_created=room.date_created, is_active=room.is_active)
                return room
            else:
                return None

    async def give_access(self, uow:AbstractUOW, room_id,
                          current_user, access_data: UserAppealSchema):
        access_dict = access_data.model_dump()
        access_dict["room_id"] = room_id
        # тут сначала должен идти запрос в редис и только потом в бд
        # добавить проверку может юзер уже имеет доступ
        async with uow:
            params = {"room_id": room_id, "user_id": current_user}
            access: RoomAccess = await uow.access.add_one(**params)
            if access.user_permissions in can_invite:
                conn_id = await uow.access.add_one(access_dict)
                await uow.commit()
                return conn_id
            else:
                return None

    async def kick_user(self, uow: AbstractUOW, room_id, current_user, access_data: UserAppealSchema):
        access_dict = access_data.model_dump()
        user_for_kick = access_dict.get("user_id")
        async with uow:
            params = {"room_id": room_id, "user_id": current_user}
            access: RoomAccess = await uow.access.add_one(**params)
            # расширить функцию только админ может кикать лида, админа кикать нельзя.
            if access.user_permissions in can_kick:
                kicked_user_id = uow.access.delete_access(room_id, user_id=user_for_kick)
                await uow.commit()
                return kicked_user_id
            else:
                return None

    async def update_role_user(self, uow: AbstractUOW, room_id, current_user, role_data: UpdateRoleSchema, user):
        async with uow:
            role_dict = role_data.model_dump()
            params = {"room_id": room_id, "user_id": current_user}
            access: RoomAccess = await uow.access.add_one(**params)
            if access.user_permissions in can_promote:
                params["user_id"] = user
                promoted_user_id = await uow.access.edit_one(role_dict, **params)
                await uow.commit()
                res = UpdatedRoleResponseSchema(user_id=promoted_user_id.user_id,
                                                new_role=promoted_user_id.user_permissions)
                return res
            else:
                return None



