from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncEngine

from orienteer.general.config import (DEBUG_DB_ECHO, POSTGRES_ORIENTEER_DBNAME, POSTGRES_ORIENTEER_HOST,
                                      POSTGRES_ORIENTEER_PASSWORD, POSTGRES_ORIENTEER_PORT, POSTGRES_ORIENTEER_USER)

DATABASE_URL = (f'postgresql+asyncpg://{POSTGRES_ORIENTEER_USER}:{POSTGRES_ORIENTEER_PASSWORD}'
                f'@{POSTGRES_ORIENTEER_HOST}:{POSTGRES_ORIENTEER_PORT}/{POSTGRES_ORIENTEER_DBNAME}')


class DatabaseHelper:
    def __init__(self, db_url, echo):
        self.engine: AsyncEngine = create_async_engine(url=db_url, echo=echo, )
        self.session_factory: async_sessionmaker = async_sessionmaker(bind=self.engine, autoflush=False,
                                                                      autocommit=False, expire_on_commit=False, )


database_helper = DatabaseHelper(db_url=DATABASE_URL, echo=DEBUG_DB_ECHO, )
