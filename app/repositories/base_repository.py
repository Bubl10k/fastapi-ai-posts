from datetime import datetime
from typing import Generic, TypeVar
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete
from sqlalchemy.orm import selectinload

from app.models.base import Base


ModelType = TypeVar("ModelType", bound=Base)


class BaseRepository(Generic[ModelType]):
    def __init__(self, session: AsyncSession, model: Generic[ModelType]):
        self.session = session
        self.model = model

    async def create(self, data: dict) -> ModelType:
        row = self.model(**data)

        self.session.add(row)
        await self.session.commit()
        await self.session.refresh(row)
        return row

    async def get_one(self, preload: list | None = None, **params) -> ModelType:
        query = select(self.model).filter_by(**params)

        if preload:
            for relation in preload:
                query = query.options(selectinload(relation))

        result = await self.session.execute(query)
        return result.scalar_one_or_none()

    async def get_many(self, preload: list | None = None, **params) -> list[ModelType]:
        query = select(self.model).filter_by(**params)

        if preload:
            for relation in preload:
                query = query.options(selectinload(relation))

        result = await self.session.execute(query)
        return result.scalars().all()

    async def update(self, model_id: int, data: dict) -> ModelType:
        query = (
            update(self.model)
            .where(self.model.id == model_id)
            .values(**data)
            .returning(self.model)
        )
        result = await self.session.execute(query)
        result.updated_at = datetime.now()
        await self.session.commit()
        return result.scalar_one()

    async def delete(self, model_id: int) -> ModelType:
        query = (
            delete(self.model).where(self.model.id == model_id).returning(self.model)
        )
        result = await self.session.execute(query)
        await self.session.commit()
        return result.scalar_one()
