import uuid

from sqlalchemy import create_engine, select, text, types
from sqlalchemy.orm import Mapped, mapped_column, declarative_base

from schemas.user_schemas import UserSchema


Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    id: Mapped[uuid.UUID] = mapped_column(types.UUID, primary_key=True, default=uuid.uuid4)
    user_name: Mapped[str] = mapped_column(nullable=False)
    user_surname: Mapped[str] = mapped_column(nullable=False)
    email: Mapped[str] = mapped_column(unique=True ,nullable=False)
    is_active: Mapped[bool] = mapped_column(default=True, nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
