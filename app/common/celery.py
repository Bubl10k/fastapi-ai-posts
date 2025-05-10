from pydantic_settings import BaseSettings


class CelerySettings(BaseSettings):
    CELERY_WORKER_NAME: str
    CELERY_BROKER_URL: str
    CELERY_RESULT_BACKEND: str
