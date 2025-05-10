import asyncio

from app.database.db import async_session
from app.schemas.comment_response_schema import CommentResponseCreate
from app.services.celery_service import CeleryService
from app.services.comment_response_service import get_comment_response_service

celery_app = CeleryService().get_celery_app()


@celery_app.task(name="create_comment_response_scheduled")
def create_comment_response_scheduled(
    comment_response_create: CommentResponseCreate,
    comment_id: int,
    user_id: int,
):
    async def _create_response():
        async with async_session() as session:
            service = get_comment_response_service(session=session)
            await service.create_comment_response(
                comment_response_create=comment_response_create,
                user_id=user_id,
                comment_id=comment_id,
                auto_response=True,
            )

    asyncio.create_task(_create_response())
