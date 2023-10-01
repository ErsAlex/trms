import uuid

from pydantic import BaseModel, EmailStr


class UserSchema(BaseModel):
    id: uuid.UUID
    user_name: str
    user_surname: str
    email: EmailStr

    class Config:
        from_attributes = True


class UserCreateSchema(BaseModel):
    user_name: str
    user_surname: str
    email: EmailStr
    password: str