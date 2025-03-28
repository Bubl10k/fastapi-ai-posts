from pydantic.v1 import BaseSettings

from app.common.auth import AuthSettings
from app.common.db import DBSettings
from app.common.gemini import Gemini


class Settings(BaseSettings):
    db: DBSettings = DBSettings()
    auth: AuthSettings = AuthSettings()
    gemini: Gemini = Gemini()


settings = Settings()
