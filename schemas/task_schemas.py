import datetime
from models.models import RoomRole
from pydantic import BaseModel
import uuid


class TaskCreateSchema(BaseModel):
    task_name: str
    description: str


class TaskUpdateSchema(TaskCreateSchema):
    pass