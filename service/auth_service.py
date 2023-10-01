
from utils.uow import AbstractUOW
from service.hashing import verify_password
from fastapi.security import OAuth2PasswordRequestForm


from jose import jwt, JWTError
from fastapi.exceptions import HTTPException
from fastapi import status
from config import ALGORITHM, SECRET_KEY


class AuthService:

    async def get_user_from_token(self, uow: AbstractUOW, token):
        exeption = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="invalid credentials")
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            email: str = payload.get('sub')
            if email is None:
                raise exeption
        except JWTError:
            raise exeption
        async with uow:
            user_id = await uow.users.find_one(email=email)
            user_id = user_id.id

    async def authenticate_user(self, uow: AbstractUOW, form_data: OAuth2PasswordRequestForm):
        user_email = form_data.username
        user_password = form_data.password
        async with uow:
            user = await uow.users.find_one(email=user_email)
            if not verify_password(user_password, user.password):
                return
            else:
                email = user.email
                return email
