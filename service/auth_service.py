
from utils.uow import AbstractUOW
from service.hashing import verify_password
from fastapi.security import OAuth2PasswordRequestForm



class AuthService:


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
