from models.models import User
from utils.repository import SQLRepository


class UserRepository(SQLRepository):
    model = User
