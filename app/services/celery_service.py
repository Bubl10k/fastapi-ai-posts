import ssl

from celery import Celery

from app.common.settings import settings
from app.schemas.comment_response_schema import CommentResponseCreate


class CeleryService:
    ssl_options = {"ssl_cert_reqs": ssl.CERT_NONE}

    def __init__(self):
        self.celery_app = Celery(
            settings.celery.CELERY_WORKER_NAME,
            broker=settings.celery.CELERY_BROKER_URL,
            backend=settings.celery.CELERY_RESULT_BACKEND,
        )

    def setup_celery(self):
        self.celery_app.conf.update(
            broker_use_ssl=CeleryService.ssl_options,
            redis_backend_use_ssl=CeleryService.ssl_options,
            task_serializer="json",
            result_serializer="json",
            accept_content=["json"],
            enable_utc=True,
            timezone="Europe/Kiev",
            broker_connection_retry_on_startup=True,
            task_acks_late=True,
            task_reject_on_worker_lost=True,
        )

    @staticmethod
    def create_comment_response_scheduled(
        comment_response: CommentResponseCreate, comment_id: int, user_id: int, delay: int
    ):
        from app.tasks.comment_response_tasks import create_comment_response_scheduled

        create_comment_response_scheduled.apply_async(args=[comment_response, comment_id, user_id], countdown=delay)

    def get_celery_app(self):
        return self.celery_app


def get_celery_service():
    return CeleryService()
