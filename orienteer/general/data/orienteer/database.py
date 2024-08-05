from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from orienteer.general.config import (DEBUG_MODE, POSTGRES_ORIENTEER_DBNAME, POSTGRES_ORIENTEER_HOST,
                                      POSTGRES_ORIENTEER_PASSWORD, POSTGRES_ORIENTEER_PORT, POSTGRES_ORIENTEER_USER)

DATABASE_URL = (f'postgresql+asyncpg://{POSTGRES_ORIENTEER_USER}:{POSTGRES_ORIENTEER_PASSWORD}'
                f'@{POSTGRES_ORIENTEER_HOST}:{POSTGRES_ORIENTEER_PORT}/{POSTGRES_ORIENTEER_DBNAME}')

async_engine = create_async_engine(DATABASE_URL, echo=DEBUG_MODE, future=True)

# async_session = AsyncSession(async_engine, expire_on_commit=False)

async_session = sessionmaker(async_engine, expire_on_commit=False, class_=AsyncSession)