from pydantic_settings import BaseSettings


class RedisSettings(BaseSettings):
    REDIS_HOST: str
    REDIS_PORT: str

    @property
    def url(self) -> str:
        return f"redis://{self.HOST}:{self.PORT}"
