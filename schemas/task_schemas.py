import datetime
from models.models import RoomRole
from pydantic import BaseModel, ConfigDict
import uuid
from models.models import Task, TaskAssignment, TaskHistory


class TaskCreateSchema(BaseModel):
    task_name: str
    description: str


class TaskResponseSchema(BaseModel):

    model_config = ConfigDict(from_attributes=True)

    id: int
    task_name: str
    description: str
    date_created: datetime.datetime
    date_updated: datetime.datetime
    owner_id: uuid.UUID
    room_id: int
    is_assigned: bool
    is_active: bool


class TaskUpdateSchema(BaseModel):
    task_name: str
    description: str


class AssignSchema(BaseModel):
    user_id: uuid.UUID
    task_id: int


class AssignResponseSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime.datetime
    task_id: int
    user_id: uuid.UUID


class TaskCommentCreateSchema(BaseModel):
    comment: str


class TaskCommentResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    task_id: int
    comment: str
    author_id: str
    created_at: datetime.datetime
    updated_at: datetime.datetime


