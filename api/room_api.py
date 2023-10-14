from fastapi import APIRouter
from schemas.room_schemas import RoomCreateSchema, RoomUpdateSchema, UserAppealSchema, UpdateRoleSchema
from api.dependencies import UOWDependency, CurrentUserDependency
from service.room_service import RoomService
from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
import uuid

router = APIRouter(
    prefix="/rooms",
    tags=["Rooms"],
)


@router.post("")
async def create_room(data: RoomCreateSchema, uow: UOWDependency, current_user: CurrentUserDependency):
    try:
        room_id = await RoomService().add_room(uow=uow, room_data=data, owner=current_user)
        return {"room_id": room_id}

    except IntegrityError as err:
        raise HTTPException(status_code=503, detail=f"Database error: {err}")


@router.patch("/{room_id}/update")
async def update_room(data: RoomUpdateSchema, uow: UOWDependency, current_user: CurrentUserDependency, room_id: int):
    try:
        updated_room = await RoomService().update_room(uow=uow, room_id=room_id, current_user=current_user, room_data=data)
        if not updated_room:
            raise HTTPException(status_code=403, detail="Forbidden")
        return updated_room
    except IntegrityError as err:
        raise HTTPException(status_code=503, detail=f"Database error: {err}")


@router.post("/{room_id}/invite")
async def invite_user(uow: UOWDependency, current_user: CurrentUserDependency, data: UserAppealSchema, room_id: int):
    try:
        access_id = await RoomService().give_access(uow, room_id, current_user, data)
        if not access_id:
            raise HTTPException(status_code=403, detail="Forbidden")
    #placeholder
        return {"status": "ok"}
    except IntegrityError as err:
        raise HTTPException(status_code=503, detail=f"Database error: {err}")

@router.delete("/{room_id}/kick")
async def kick_user(uow: UOWDependency, current_user: CurrentUserDependency, data: UserAppealSchema, room_id: int):
    try:
        kicked_user_id = await RoomService().kick_user(uow, room_id, current_user, data)
        if not kicked_user_id:
            raise HTTPException(status_code=403, detail="Forbidden")
        return {"kicked_user": kicked_user_id}
    except IntegrityError as err:
        raise HTTPException(status_code=503, detail=f"Database error: {err}")


@router.patch("/{room_id}/promote")
async def update_user_role(uow: UOWDependency, current_user: CurrentUserDependency,
                           role_data: UpdateRoleSchema, user_id: uuid.UUID, room_id: int):
    try:
        updated_user_resp = await RoomService().update_role_user(uow, room_id, current_user, role_data, user_id)
        if not updated_user_resp:
            raise HTTPException(status_code=403, detail="Forbidden")
        return updated_user_resp
    except IntegrityError as err:
        raise HTTPException(status_code=503, detail=f"Database error: {err}")






