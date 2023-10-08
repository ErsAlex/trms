from datetime import datetime
from datetime import timedelta
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends
from fastapi import HTTPException
from fastapi import status
from config import SECRET_KEY, ALGORITHM
from jose import jwt, JWTError
import uuid

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")


def create_token(data: dict, expiration_delta: timedelta):
    encoded_data = data.copy()
    expire_date = datetime.utcnow() + expiration_delta
    encoded_data.update({"exp": expire_date})
    encoded_jwt = jwt.encode(encoded_data, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_user_from_token(token: str = Depends(oauth2_scheme)):
    exeption = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="invalid credentials")
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        data: str = payload.get('sub')
        if data is None:
            raise exeption
    except JWTError:
        raise exeption
    user_id = uuid.UUID(data)
    return user_id

