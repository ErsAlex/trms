import uuid

from pydantic import BaseModel, EmailStr, ConfigDict
from models.models import User


class UserSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    user_name: str
    user_surname: str
    email: str
    is_active: bool



class UserUpdateSchema(BaseModel):
    user_name: str
    user_surname: str
    email: str


class UserCreateSchema(BaseModel):
    user_name: str
    user_surname: str
    email: EmailStr
    password: str