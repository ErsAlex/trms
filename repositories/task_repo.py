from models.models import TaskAssignment, Task, TaskHistory
from utils.repository import SQLRepository


class TaskRepository(SQLRepository):
    model = Task


class TaskAssignmentRepository(SQLRepository):
    model = TaskAssignment


class TaskHistoryRepository(SQLRepository):
    model = TaskHistory