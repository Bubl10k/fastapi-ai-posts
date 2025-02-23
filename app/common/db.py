from pydantic_settings import BaseSettings


class DBSettings(BaseSettings):
    DB_NAME: str
    DB_HOST: str
    DB_USER: str
    DB_PORT: str
    DB_PASSWORD: str
    
