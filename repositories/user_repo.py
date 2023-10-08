from models.models import User
from utils.repository import SQLRepository
from db import async_session_maker
from sqlalchemy import select
import uuid


class UserRepository(SQLRepository):
    model = User
