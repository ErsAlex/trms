import uuid
from models.models import Task, UserRoomAccess, TaskHistory
from utils.uow import AbstractUOW
from config import can_give_tasks
from schemas.task_schemas import TaskCreateSchema,TaskCommentCreateSchema, TaskUpdateSchema, TaskResponseSchema, TaskCommentResponse, AssignSchema, AssignResponseSchema


class TaskService:
    def __init__(self, uow: AbstractUOW):
        self.uow = uow

    async def add_task(
            self,
            room_id: int,
            task: TaskCreateSchema,
            owner: uuid.UUID
    ):
        async with self.uow:
            current_user_access: UserRoomAccess = await self.uow.access.find_one(
                room_id=room_id,
                user_id=owner
            )
            if current_user_access.user_permissions in can_give_tasks:
                task_data = task.model_dump()
                task_data["room_id"], task_data["owner_id"] = room_id, owner
                new_task: Task = await self.uow.task.add_one(task_data)

                history_data = {
                    "task_id": new_task.id,
                    "author_id": new_task.owner_id,
                    "comment": "task created"
                }

                await self.uow.task_history.add_one(history_data)
                await self.uow.commit()
                return TaskResponseSchema.model_validate(new_task)
            else:
                return None

    async def update_task(
            self,
            task_id: int,
            task_data: TaskUpdateSchema,
            current_user: uuid.UUID,
            room_id: int
    ):
        async with self.uow:
            current_user_access: UserRoomAccess = await self.uow.access.find_one(
                room_id=room_id,
                user_id=current_user
            )
            if current_user_access.user_permissions in can_give_tasks:
                task_dict = task_data.model_dump()
                task: Task = await self.uow.task.edit_one(
                    task_dict,
                    id=task_id
                )
                history_data = {
                    "task_id": task.id,
                    "author_id": task.owner_id,
                    "comment": "task updated"
                }
                await self.uow.task_history.add_one(history_data)
                await self.uow.commit()

                return TaskResponseSchema.model_validate(task)
            return None

    async def assign_task(
            self,
            assign_data: AssignSchema,
            current_user: uuid.UUID,
            room_id: int
    ):
        async with self.uow:
            current_user_profile: UserRoomAccess = await self.uow.access.find_one(
                room_id=room_id,
                user_id=current_user
            )
            if current_user_profile.user_permissions in can_give_tasks:
                assign = assign_data.model_dump()
                assignment = await self.uow.task_assignment.add_one(assign)
                history_dict = {
                    "task_id": assign_data.task_id,
                    "author_id": current_user,
                    "comment": f"user: {assign_data.user_id} assigned to task"
                }
                await self.uow.task_history.add_one(history_dict)
                await self.uow.commit()

                return AssignResponseSchema.model_validate(assignment)

            return None

    async def revoke_assignment(
            self,
            assign_data: AssignSchema,
            current_user: uuid.UUID,
            room_id: int

    ):
        async with self.uow:
            current_user_access: UserRoomAccess = await self.uow.access.find_one(
                room_id=room_id,
                user_id=current_user
            )
            if current_user_access.user_permissions in can_give_tasks:
                revoke_assignment = await self.uow.task_assignment.delete_one(
                    user_id=assign_data.user_id,
                    task_id=assign_data.task_id
                )
                return {"user_id": assign_data.user_id,
                        "status": "assignment revoked"
                        }
            return None

    async def add_comment(
            self,
            room_id: int,
            current_user: uuid.UUID,
            task_id: int,
            comment: TaskCommentCreateSchema
    ):
        current_user_access: UserRoomAccess = await self.uow.access.find_one(
            room_id=room_id,
            user_id=current_user
        )
        if current_user_access:
            history_dict = comment.model_dump()
            history_dict["task_id"], history_dict["author_id"] = task_id, current_user
            comment: TaskHistory = await self.uow.task_history.add_one(history_dict)
            return TaskCommentResponse.model_validate(comment)
        return None

    async def get_tasks(
            self,
            room_id: int | None,
            current_user: uuid.UUID
    ):
        if room_id:
            async with self.uow:
                current_user_access: UserRoomAccess = await self.uow.access.find_one(
                    room_id=room_id,
                    user_id=current_user
                )
                if current_user_access:
                    tasks = await self.uow.task.find_all(room_id=room_id)
                return None
        else:
            tasks = await self.uow.task.find_all(owner_id=current_user)
        tasks = [TaskResponseSchema.model_validate(task) for task in tasks]
        return tasks

    async def get_user_tasks(
            self,
            user_id: uuid.UUID
    ):
        async with self.uow:
            tasks = await self.uow.task.get_user_assigns(user_id)
            tasks = [TaskResponseSchema.model_validate(task) for task in tasks]
            return tasks