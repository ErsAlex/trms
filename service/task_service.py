
from utils.uow import AbstractUOW
from service.access import can_invite, can_promote,can_give_tasks, can_update, can_kick
from models.models import User, RoomAccess, Room
from schemas.task_schemas import TaskCreateSchema, TaskUpdateSchema

class TaskService:

    async def add_task(self, uow: AbstractUOW,  task: TaskCreateSchema, room_id, owner):
        async with uow:
            task_dict = task.model_dump()
            task_dict["room_id"], task_dict["user_id"] = room_id, owner
            task_id = await uow.task.add_one(task_dict)
            await uow.flush()
            history_dict = {"task_id": task_id, "comment": "task created", "author": owner}
            task_history_id = await uow.task_history.add_one(history_dict)
            await uow.commit()
            return {"created task id": task_id}

    async def update_task(self, uow: AbstractUOW, task: TaskUpdateSchema, room_id, owner):
        async with uow:
            task_dict = task.model_dump()
