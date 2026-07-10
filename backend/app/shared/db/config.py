from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


class DatabaseConnection:
    def __init__(self) -> None:
        self.__string_connection = "sqlite+aiosqlite:///./tickets.db"
        self.__engine = create_async_engine(self.__string_connection)
        self.__session_factory = async_sessionmaker(self.__engine, expire_on_commit=False)

    @property
    def string_connection(self) -> str:
        return self.__string_connection

    async def create_all(self) -> None:
        async with self.__engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

    @asynccontextmanager
    async def managed_session(self) -> AsyncGenerator[AsyncSession]:
        async with self.__session_factory() as session:
            yield session

    async def get_session(self) -> AsyncGenerator[AsyncSession]:
        async with self.managed_session() as session:
            yield session
