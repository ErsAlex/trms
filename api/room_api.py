from fastapi import APIRouter
from schemas.room_schemas import RoomCreateSchema, RoomResponseSchema, RoomUpdateSchema,  UpdateRoleSchema, AccessSchema
from api.dependencies import UOWDependency, CurrentUserDependency
from service.room_service import RoomService
from fastapi import HTTPException, Depends
from sqlalchemy.exc import IntegrityError


router = APIRouter(
    prefix="/rooms",
    tags=["Rooms"],
)


@router.post("/new")
async def create_room(
        room_data: RoomCreateSchema,
        uow: UOWDependency,
        current_user: CurrentUserDependency
):

    try:
        room: RoomResponseSchema = await RoomService(uow).add_room(
            room_data,
            current_user
        )
        return room

    except IntegrityError as err:
        raise HTTPException(status_code=503, detail=f"Database error: {err}")


@router.patch("/{room_id}/update")
async def update_room(
        data: RoomUpdateSchema,
        uow: UOWDependency,
        current_user: CurrentUserDependency,
        room_id: int
):

    try:
        updated_room: RoomResponseSchema = await RoomService(uow).update_room(
            room_id,
            data,
            current_user
        )
        if not updated_room:
            raise HTTPException(status_code=403, detail="Forbidden")
        return updated_room
    except IntegrityError as err:
        raise HTTPException(status_code=503, detail=f"Database error: {err}")


@router.post("/{room_id}/invite")
async def invite_user(
        room_id: int,
        uow: UOWDependency,
        current_user: CurrentUserDependency,
        new_access_data: AccessSchema
):
    try:
        response = await RoomService(uow).give_access(
            room_id,
            new_access_data,
            current_user
        )
        if not response:
            raise HTTPException(status_code=403, detail="Forbidden")

        return response
    except IntegrityError as err:
        raise HTTPException(status_code=503, detail=f"Database error: {err}")


@router.delete("/{room_id}/kick")
async def kick_user(
        room_id: int,
        uow: UOWDependency,
        current_user: CurrentUserDependency,
        access_data: AccessSchema = Depends()
):

    try:
        response = await RoomService(uow).kick_user(
            access_data,
            current_user,
            room_id
        )
        if not response:
            raise HTTPException(status_code=403, detail="Forbidden")
        return response
    except IntegrityError as err:
        raise HTTPException(status_code=503, detail=f"Database error: {err}")


@router.patch("/{room_id}/promote")
async def update_user_role(
        room_id: int,
        uow: UOWDependency,
        current_user: CurrentUserDependency,
        role_data: UpdateRoleSchema = Depends()
):
    try:
        response = await RoomService(uow).update_role(
            current_user,
            role_data,
            room_id
        )
        if not response:
            raise HTTPException(status_code=403, detail="Forbidden")
        return response
    except IntegrityError as err:
        raise HTTPException(status_code=503, detail=f"Database error: {err}")






