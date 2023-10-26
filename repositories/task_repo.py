import uuid

from models.models import TaskAssignment, Task, TaskHistory
from utils.repository import SQLRepository
from sqlalchemy import select


class TaskRepository(SQLRepository):
    model = Task

    async def get_user_assigns(
            self,
            user_id: uuid.UUID
    ):
        query = select(self.model).join(self.model.assignments).where(TaskAssignment.user_id==user_id)
        res = await self.session.execute(query)
        result = [row[0] for row in res.all()]
        return result

class TaskAssignmentRepository(SQLRepository):
    model = TaskAssignment


class TaskHistoryRepository(SQLRepository):
    model = TaskHistory