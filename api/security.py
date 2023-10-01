from datetime import datetime
from datetime import timedelta
from config import SECRET_KEY, ALGORITHM
from jose import jwt


def create_token(data: dict, expiration_delta: timedelta):
    encoded_data = data.copy()
    expire_date = datetime.utcnow() + expiration_delta
    encoded_data.update({"exp": expire_date})
    encoded_jwt = jwt.encode(encoded_data, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

