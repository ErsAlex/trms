from fastapi import APIRouter, HTTPException, Depends
from api.dependencies import UOWDependency, CurrentUserDependency
from schemas.task_schemas import TaskCommentCreateSchema, TaskUpdateSchema, AssignSchema, TaskCreateSchema
from service.task_service import TaskService
from sqlalchemy.exc import IntegrityError


router = APIRouter(
    prefix="/rooms",
    tags=["Tasks"],
)


@router.post("/{room_id}/tasks/add")
async def create_task(
        uow: UOWDependency,
        current_user: CurrentUserDependency,
        room_id: int,
        task: TaskCreateSchema

):
    try:
        response = await TaskService(uow).add_task(
            room_id,
            task,
            current_user
        )
        if not response:
            raise HTTPException(status_code=403, detail="Forbidden")
        return response
    except IntegrityError as err:
        raise HTTPException(status_code=503, detail=f"Database error: {err}")


@router.patch("/{room_id}/tasks/{task_id}update")
async def update_task(
        task_id: int,
        room_id: int,
        uow: UOWDependency,
        current_user: CurrentUserDependency,
        task_data: TaskUpdateSchema
):

    try:
        task = await TaskService(uow).update_task(
            task_id,
            task_data,
            current_user,
            room_id
)
        if not task:
            raise HTTPException(status_code=403, detail="Forbidden")
        return task
    except IntegrityError as err:
        raise HTTPException(status_code=503, detail=f"Database error: {err}")


@router.post("/{room_id}/tasks/assign")
async def assign_task(
        room_id: int,
        uow: UOWDependency,
        current_user: CurrentUserDependency,
        assign_data: AssignSchema = Depends()
):
    try:
        response = await TaskService(uow).assign_task(
            assign_data,
            current_user,
            room_id
        )
        if not response:
            raise HTTPException(status_code=403, detail="Forbidden")
        return response
    except IntegrityError as err:
        raise HTTPException(status_code=503, detail=f"Database error: {err}")


@router.delete("/{room_id}/tasks/revoke")
async def revoke_assignment(
        room_id: int,
        uow: UOWDependency,
        current_user: CurrentUserDependency,
        assign_data: AssignSchema = Depends()
):
    try:
        response = await TaskService(uow).revoke_assignment(
            assign_data,
            current_user,
            room_id
        )
        if not response:
            raise HTTPException(status_code=403, detail="Forbidden")
        return response
    except IntegrityError as err:
        raise HTTPException(status_code=503, detail=f"Database error: {err}")


@router.post("{room_id}/tasks/{task_id}/comment")
async def task_comment(
        uow: UOWDependency,
        room_id: int,
        current_user: CurrentUserDependency,
        task_id: int,
        comment: TaskCommentCreateSchema
):
    try:
        response = await TaskService(uow).add_comment(
            room_id,
            current_user,
            task_id,
            comment
        )
        if not response:
            raise HTTPException(status_code=403, detail="Forbidden")
        return response
    except IntegrityError as err:
        raise HTTPException(status_code=503, detail=f"Database error: {err}")
