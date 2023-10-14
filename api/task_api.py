from fastapi import APIRouter, HTTPException
from api.dependencies import UOWDependency, CurrentUserDependency
from schemas.task_schemas import TaskCreateSchema, TaskUpdateSchema
from service.task_service import TaskService
from sqlalchemy.exc import IntegrityError
router = APIRouter(
    prefix="/rooms",
    tags=["Tasks"],
)


@router.post("/{room_id}/add")
async def create_task(uow: UOWDependency, current_user: CurrentUserDependency, room_id: int, task: TaskCreateSchema):
    try:
        response = await TaskService().add_task(uow, task, room_id, current_user)
        return response
    except IntegrityError as err:
        raise HTTPException(status_code=503, detail=f"Database error: {err}")


# @router.patch("/{room_id}/{task_id}/update")
# async def update_task(uow: UOWDependency, current_user: CurrentUserDependency,
#                       room_id: int, task_id:int, task: TaskUpdateSchema):
#
#
