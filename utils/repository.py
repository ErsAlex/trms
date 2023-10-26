from abc import ABC, abstractmethod
from sqlalchemy import insert, select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession
from db import async_session_maker


class AbstractRepository(ABC):
    @abstractmethod
    async def add_one(self):
        raise NotImplementedError


class SQLRepository(AbstractRepository):

    model = None

    def __init__(self, session: AsyncSession):
        self.session = session

    async def add_one(self, data: dict):
        query = insert(self.model).values(**data).returning(self.model)
        result = await self.session.execute(query)
        return result.scalar_one()

    async def find_one(self, **filter_by):
        stmt = select(self.model).filter_by(**filter_by)
        result = await self.session.execute(stmt)
        result = result.scalar_one()
        return result

    async def find_one_or_none(self, **filter_by):
        stmt = select(self.model).filter_by(**filter_by)
        result = await self.session.execute(stmt)
        result = result.one_or_none()
        return result

    async def delete_one(self, **filter_by):
        stmt = delete(self.model).filter_by(**filter_by)
        res = await self.session.execute(stmt)
        return res

    async def edit_one(self, data: dict, **filter_by):
        stmt = update(self.model).values(**data).filter_by(**filter_by).returning(self.model)
        res = await self.session.execute(stmt)
        res = res.scalar_one()
        return res

    async def find_all(self, **filter_by):
        stmt = select(self.model).filter_by(**filter_by)
        res = await self.session.execute(stmt)
        result = [row[0] for row in res.all()]
        return result

    async def add_all(self, data: list):
        stmt = self.session.add_all(data)
        return None



