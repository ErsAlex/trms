import datetime
from models.models import RoomRole, Room, UserRoomAccess
from pydantic import BaseModel, ConfigDict , EmailStr
import uuid
from models.models import RoomRole

class RoomCreateSchema(BaseModel):
    name: str
    description: str


class RoomUpdateSchema(BaseModel):
    name: str
    description: str


class RoomResponseSchema(BaseModel):

    model_config = ConfigDict(from_attributes=True)

    id: int
    owner_id: uuid.UUID
    date_created: datetime.datetime
    name: str
    description: str
    is_active: bool



class UpdateRoleSchema(BaseModel):
    user_id: uuid.UUID
    user_permissions: RoomRole


class UpdatedRoleResponseSchema(BaseModel):
    user_id: uuid.UUID
    new_role: str


class AccessSchema(BaseModel):
    user_id : uuid.UUID


class AccessResponse(BaseModel):

    model_config = ConfigDict(from_attributes=True)
    id: int
    user_permissions: RoomRole
    user_id: uuid.UUID
    room_id: int



class AccessUpdateResponse(BaseModel):

    user_id: uuid.UUID
    room_id: int
    access_granted: bool = False
    access_revoked: bool = False
    role_updated: bool = False
    user_role: RoomRole

    @classmethod
    async def access_granted_response(cls, room_access: UserRoomAccess):
        return cls(
            user_id=room_access.user_id,
            room_id=room_access.room_id,
            access_granted=True,
            access_revoked=False,
            role_updated=False,
            user_role=room_access.user_permissions
        )

    @classmethod
    async def access_revoked_response(cls, room_access: UserRoomAccess):
        return cls(
            user_id=room_access.user_id,
            room_id=room_access.room_id,
            access_granted=False,
            access_revoked=True,
            role_updated=False,
            user_role=room_access.user_permissions
        )

    @classmethod
    async def user_role_response(cls, room_access: UserRoomAccess):
        return cls(
            user_id=room_access.user_id,
            room_id=room_access.room_id,
            access_granted=False,
            access_revoked=False,
            role_updated=True,
            user_role=room_access.user_permissions
        )
