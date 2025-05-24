from datetime import datetime
from typing import Generic, TypeVar

from sqlalchemy import delete, or_, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from sqlalchemy.orm.interfaces import LoaderOption

from app.models.base import Base

ModelType = TypeVar("ModelType", bound=Base)


class BaseRepository(Generic[ModelType]):
    def __init__(self, session: AsyncSession, model: Generic[ModelType]):
        self.session = session
        self.model = model

    def _get_model_field(self, field_name: str):
        try:
            return getattr(self.model, field_name)
        except AttributeError:
            return ValueError(f"Field {field_name} does not exist in {self.model}")

    @staticmethod
    async def construct_preload(query, preload: list | None):
        if preload:
            for relation in preload:
                if isinstance(relation, LoaderOption):
                    query = query.options(relation)
                else:
                    query = query.options(selectinload(relation))
        return query

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

    async def get_many(
        self, preload: list | None = None, filters: list | None = None, order_by: list | None = None, **params
    ) -> list[ModelType]:
        query = select(self.model).filter_by(**params)

        if filters:
            query = query.filter(*filters)

        if order_by:
            query = query.order_by(*order_by)

        if preload:
            for relation in preload:
                query = query.options(selectinload(relation))

        result = await self.session.execute(query)
        return result.scalars().all()

    async def update(self, model_id: int, data: dict, preload: list | None = None) -> ModelType:
        query = update(self.model).where(self.model.id == model_id).values(**data).returning(self.model)

        if preload:
            query = await self.construct_preload(query, preload)

        result = await self.session.execute(query)
        result.updated_at = datetime.now()
        await self.session.commit()
        return result.scalar_one()

    async def delete(self, model_id: int) -> ModelType:
        query = delete(self.model).where(self.model.id == model_id).returning(self.model)
        result = await self.session.execute(query)
        await self.session.commit()
        return result.scalar_one()

    async def search_in_field(
        self,
        fields: list[str],
        search_query: str,
        preload: list | None = None,
        order_by: list | None = None,
    ) -> list[ModelType]:
        """
        Generic search method for models based on query in specified fields (field names passed as strings).
        """
        where_clauses = []
        if search_query and fields:
            search_clause = or_(*[self._get_model_field(field).ilike(f"%{search_query}%") for field in fields])
            where_clauses.append(search_clause)

        results = await self.get_many(preload=preload, order_by=order_by, filters=where_clauses)
        return results
