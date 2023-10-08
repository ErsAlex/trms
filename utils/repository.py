from abc import ABC, abstractmethod

from sqlalchemy import insert, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from db import async_session_maker,get_async_session


class AbstractRepository(ABC):
    @abstractmethod
    async def add_one(self):
        raise NotImplementedError


class SQLRepository(AbstractRepository):

    model = None

    def __init__(self, session: AsyncSession):
        self.session = session

    async def add_one(self, data: dict) -> int:
        query = insert(self.model).values(**data).returning(self.model.id)
        result = await self.session.execute(query)
        return result.scalar_one()

    async def find_one(self, **filter_by):
        stmt = select(self.model).filter_by(**filter_by)
        res = await self.session.execute(stmt)
        res = res.scalar_one()
        return res

    async def edit_one(self, data: dict, **filter_by):
        stmt = update(self.model).values(**data).filter_by(**filter_by).returning(self.model)
        res = await self.session.execute(stmt)
        res = res.scalar_one()
        return res