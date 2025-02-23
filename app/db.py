from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine

from app.common.settings import settings
from app.models.base import Base

DATABASE_URL = f"postgresql+asyncpg://{settings.db.DB_USER}:{settings.db.DB_PASSWORD}@{settings.db.DB_HOST}:{settings.db.DB_PORT}/{settings.db.DB_NAME}"

engine = create_async_engine(DATABASE_URL, echo=True)
async_session = async_sessionmaker(engine, expire_on_commit=False)


async def init_models():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


async def get_session() -> AsyncSession:
    async with async_session() as session:
        yield session
