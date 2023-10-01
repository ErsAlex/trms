

from typing import Annotated

from fastapi import Depends

from utils.uow import AbstractUOW, UnitOfWork

UOWDependency = Annotated[AbstractUOW, Depends(UnitOfWork)]