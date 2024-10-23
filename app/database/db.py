from typing import List

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.ext.declarative import declarative_base

from app.core.settings import settings

async_engines = [
    create_async_engine(
        settings.DB_URI_MASTER,
        pool_pre_ping=True,
        echo=True,
    ),
    create_async_engine(
        settings.DB_URI_SLAVE_1,
        pool_pre_ping=True,
        echo=True,
    ),
    create_async_engine(
        settings.DB_URI_SLAVE_2,
        pool_pre_ping=True,
        echo=True,
    ),
]
async_sessions = [
    async_sessionmaker(
        bind=async_engine,
        autoflush=False,
        future=True,
    )
    for async_engine in async_engines
]


async def get_session() -> List[AsyncSession]:
    async with async_sessions[0]() as session_master, async_sessions[
        1
    ]() as session_slave_1, async_sessions[2]() as session_slave_2:
        async with session_master.begin(), session_slave_1.begin(), session_slave_2.begin():
            try:
                yield [
                    session_master,
                    session_slave_1,
                    session_slave_2,
                ]
                await session_master.commit()
                await session_slave_1.commit()
                await session_slave_2.commit()
            finally:
                await session_master.close()
                await session_slave_1.close()
                await session_slave_2.close()


Base = declarative_base()
