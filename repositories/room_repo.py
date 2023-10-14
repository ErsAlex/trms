from models.models import Room, RoomAccess
from utils.repository import SQLRepository
from db import async_session_maker
from sqlalchemy import select, insert,and_, delete
import uuid


class RoomRepository(SQLRepository):
    model = Room


class AccessRepository(SQLRepository):
    model = RoomAccess

    async def delete_access(self, user_id, **filter_by):
        stmt = delete(self.model).filter_by(**filter_by).filter(and_(self.model.user_id == user_id))\
            .returning(self.model.user_id)
        res = await self.session.execute(stmt)
        res = res.scalar_one()
        return res