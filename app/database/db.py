from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.ext.declarative import declarative_base

from app.core.settings import settings

async_engine = create_async_engine(
    settings.DB_URI,
    pool_pre_ping=True,
    echo=True,
)
async_session = async_sessionmaker(
    bind=async_engine,
    autoflush=False,
    future=True,
)


async def get_session() -> AsyncSession:
    async with async_session() as session:
        async with session.begin():
            try:
                yield session
                await session.commit()
            finally:
                await session.close()


Base = declarative_base()
