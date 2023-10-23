from api.security import create_token
from fastapi import APIRouter, Depends, status, Response
from api.dependencies import UOWDependency
from service.auth_service import AuthService
from fastapi.security import OAuth2PasswordRequestForm
from datetime import timedelta
from schemas.utils_schemas import Token
from fastapi.exceptions import HTTPException

router = APIRouter(
    prefix="/login",
    tags=["Login"],
)


@router.post("", response_model=Token)
async def get_access_token(
        response: Response,
        uow: UOWDependency,
        form_data: OAuth2PasswordRequestForm = Depends()):
    user_id = await AuthService().authenticate_user(uow, form_data)
    if not user_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    access_token_expired = timedelta(minutes=30)
    refresh_token_expired = timedelta(minutes=35)
    user_id = str(user_id)
    access_token = create_token(data={"sub": user_id},
                                expiration_delta=access_token_expired)
    refresh_token = create_token(data={"sub": user_id}, expiration_delta=refresh_token_expired)
    response.set_cookie(key='refresh_token', value=refresh_token, samesite="lax", httponly=True)
    return {"access_token": access_token, "token_type": "bearer"}
