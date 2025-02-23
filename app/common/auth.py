from pydantic_settings import BaseSettings


class AuthSettings(BaseSettings):
    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str
