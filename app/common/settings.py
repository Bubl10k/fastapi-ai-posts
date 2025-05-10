from pydantic.v1 import BaseSettings

from app.common.app import AppSettings
from app.common.auth import AuthSettings
from app.common.celery import CelerySettings
from app.common.db import DBSettings
from app.common.gemini import Gemini
from app.common.redis import RedisSettings


class Settings(BaseSettings):
    app: AppSettings = AppSettings()
    db: DBSettings = DBSettings()
    auth: AuthSettings = AuthSettings()
    gemini: Gemini = Gemini()
    redis: RedisSettings = RedisSettings()
    celery: CelerySettings = CelerySettings()


settings = Settings()
