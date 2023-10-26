import uuid

from models.models import User, UserRoomAccess
from utils.repository import SQLRepository
from sqlalchemy import select, join

class UserRepository(SQLRepository):
    model = User

    async def get_room_users(self, room_id: int):
        query = select(self.model).join(self.model.room_accesses).where(UserRoomAccess.room_id==room_id)
        res = await self.session.execute(query)
        result = [row[0] for row in res.all()]
        return result

