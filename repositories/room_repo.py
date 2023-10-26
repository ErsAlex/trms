from models.models import Room, UserRoomAccess, Task, User
from utils.repository import SQLRepository
from db import async_session_maker
from sqlalchemy import select, insert,and_, delete
import uuid


class RoomRepository(SQLRepository):
    model = Room

    async def get_user_rooms(
            self,
            user_id: uuid.UUID
    ):
        query = select(self.model).join(self.model.room_accesses).where(UserRoomAccess.user_id==user_id)
        res = await self.session.execute(query)
        result = [row[0] for row in res.all()]
        return result


class AccessRepository(SQLRepository):
    model = UserRoomAccess
