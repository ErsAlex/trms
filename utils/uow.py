from abc import ABC, abstractmethod
from typing import Type
from repositories.user_repo import UserRepository
from repositories.room_repo import RoomRepository, AccessRepository
from repositories.task_repo import TaskHistoryRepository, TaskAssignmentRepository, TaskRepository
from db import async_session_maker


class AbstractUOW(ABC):
    users: Type[UserRepository]
    rooms: Type[RoomRepository]
    access: Type[AccessRepository]
    task: Type[TaskRepository]
    task_assignment: Type[TaskAssignmentRepository]
    task_history: Type[TaskHistoryRepository]


    @abstractmethod
    def __init__(self):
        ...

    @abstractmethod
    async def __aenter__(self):
        ...

    @abstractmethod
    async def __aexit__(self, *args):
        ...

    @abstractmethod
    async def commit(self):
        ...

    @abstractmethod
    async def rollback(self):
        ...

    @abstractmethod
    async def flush(self):
        ...


class UnitOfWork:
    def __init__(self):
        self.session_factory = async_session_maker

    async def __aenter__(self):
        self.session = self.session_factory()

        self.users = UserRepository(self.session)
        self.rooms = RoomRepository(self.session)
        self.access = AccessRepository(self.session)
        self.task = TaskRepository(self.session)
        self.task_assignment = TaskAssignmentRepository(self.session)
        self.task_history = TaskHistoryRepository(self.session)



    async def __aexit__(self, *args):
        await self.rollback()
        await self.session.close()

    async def commit(self):
        await self.session.commit()

    async def flush(self):
        await self.session.flush()

    async def rollback(self):
        await self.session.rollback()

