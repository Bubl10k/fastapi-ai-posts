from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DB_NAME: str
    DB_HOST: str
    DB_USER: str
    DB_PORT: str
    DB_PASSWORD: str
    

settings = Settings()
