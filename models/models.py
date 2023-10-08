import uuid
import enum
from sqlalchemy import create_engine, select, text, types, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, declarative_base, relationship
from typing import Annotated
from schemas.user_schemas import UserSchema
from datetime import datetime

Base = declarative_base()

created_at = Annotated[datetime, mapped_column(server_default=text("TIMEZONE('utc', now())"))]
updated_at = Annotated[datetime, mapped_column(
        server_default=text("TIMEZONE('utc', now())"),
        onupdate=datetime.utcnow,
    )]


class User(Base):
    __tablename__ = "users"

    id: Mapped[uuid.UUID] = mapped_column(types.UUID, primary_key=True, default=uuid.uuid4)
    user_name: Mapped[str] = mapped_column(nullable=False)
    user_surname: Mapped[str] = mapped_column(nullable=False)
    email: Mapped[str] = mapped_column(unique=True ,nullable=False)
    is_active: Mapped[bool] = mapped_column(default=True, nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    created_rooms = relationship("Room", back_populates="owner")
    room_accesses = relationship("RoomAccess", back_populates="user")


class Room(Base):
    __tablename__ = "rooms"
    id: Mapped[int] = mapped_column(primary_key=True)
    owner_id: Mapped[uuid.UUID] = mapped_column(types.UUID, ForeignKey("users.id"))
    date_created: Mapped[created_at]
    name: Mapped[str] = mapped_column(nullable=False)
    description: Mapped[str] = mapped_column(nullable=True)
    is_active: Mapped[bool] = mapped_column(nullable=False, default=True)
    owner = relationship("User", back_populates="created_rooms")
    room_accesses = relationship("RoomAccess", back_populates="room")

class RoomRole(enum.Enum):
    # can assign, invite, promote
    ROOM_CREATOR = "ROOM_CREATOR"
    # can assign task to users and invite users
    ROME_LEAD = "ROME_LEAD"
    # can only take tasks
    ROOM_USER = "ROOM_USER"


class RoomAccess(Base):
    __tablename__ = "room_access"
    id: Mapped[int] = mapped_column(primary_key=True)
    user_permissions: Mapped[RoomRole]
    user_id: Mapped[uuid.UUID] = mapped_column(types.UUID, ForeignKey("users.id"))
    room_id: Mapped[int] = mapped_column(ForeignKey("rooms.id"))
    user = relationship("User", back_populates="room_accesses")
    room = relationship("Room", back_populates="room_accesses")