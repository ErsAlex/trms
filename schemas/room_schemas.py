import datetime
from models.models import RoomRole
from pydantic import BaseModel
import uuid



class RoomCreateSchema(BaseModel):
    name: str
    description: str


class RoomUpdateSchema(RoomCreateSchema):
    pass


class RoomSchema(BaseModel):
    id: int
    name: str
    description: str
    date_created: datetime.datetime
    is_active: bool


class UserAppealSchema(BaseModel):
    user_id: uuid.UUID


class UpdateRoleSchema(BaseModel):
    user_permissions: RoomRole


class UpdatedRoleResponseSchema(BaseModel):
    user_id: uuid.UUID
    new_role: str