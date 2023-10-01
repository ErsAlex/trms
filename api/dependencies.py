

from typing import Annotated

from fastapi import Depends

from utils.uow import AbstractUOW, UnitOfWork
from api.security import get_user_from_token


UOWDependency = Annotated[AbstractUOW, Depends(UnitOfWork)]

CurrentUserDependency = Annotated[str, Depends(get_user_from_token)]