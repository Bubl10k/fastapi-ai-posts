from pydantic.v1 import BaseSettings

from app.common.auth import AuthSettings
from app.common.db import DBSettings


class Settings(BaseSettings):
    db: DBSettings = DBSettings()
    auth: AuthSettings = AuthSettings()


settings = Settings()
