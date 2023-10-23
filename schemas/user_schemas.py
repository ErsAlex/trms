import uuid

from pydantic import BaseModel, EmailStr
from models.models import User


class UserSchema(BaseModel):
    id: uuid.UUID
    user_name: str
    user_surname: str
    email: EmailStr

    @classmethod
    async def from_db_model(cls, user: User):
        return cls(
            id=user.id,
            user_name=user.user_name,
            user_surname=user.user_surname,
            email=user.email
        )


class UserUpdateSchema(BaseModel):
    user_name: str
    user_surname: str
    email: str


class UserCreateSchema(BaseModel):
    user_name: str
    user_surname: str
    email: EmailStr
    password: str