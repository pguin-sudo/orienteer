from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from orienteer.general.config.local import (DEBUG_MODE, POSTGRES_ORIENTEER_DBNAME, POSTGRES_ORIENTEER_HOST,
                                            POSTGRES_ORIENTEER_PASSWORD, POSTGRES_ORIENTEER_PORT, POSTGRES_ORIENTEER_USER)

DATABASE_URL = f'postgresql+asyncpg://{POSTGRES_ORIENTEER_USER}:{POSTGRES_ORIENTEER_PASSWORD}@{
    POSTGRES_ORIENTEER_HOST}:{POSTGRES_ORIENTEER_PORT}/{POSTGRES_ORIENTEER_DBNAME}'

async_engine = create_async_engine(DATABASE_URL, echo=DEBUG_MODE, future=True)


async_session = sessionmaker(
    bind=async_engine,
    class_=AsyncSession,
    expire_on_commit=False,
)
