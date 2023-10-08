from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase, declarative_base
from config import DATABASE_URL
from sqlalchemy import create_engine
SQl_DATABASE_URL = DATABASE_URL


engine = create_async_engine(SQl_DATABASE_URL, echo=True)


async_session_maker = async_sessionmaker(engine, expire_on_commit=False)


async def get_async_session():
    async with async_session_maker() as session:
        yield session