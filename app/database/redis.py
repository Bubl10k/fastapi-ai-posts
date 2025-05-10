import redis.asyncio as redis

from app.common.settings import settings


class RedisPool:
    def __init__(self):
        self.pool = None
        self.redis = None

    async def init_redis(self):
        if self.pool is None:
            self.pool = redis.ConnectionPool.from_url(settings.redis.url)
            self.redis = redis.Redis.from_pool(self.pool)

    async def get_redis(self):
        if self.redis is None:
            await self.init_redis()
        return self.redis

    async def close(self) -> None:
        if self.redis:
            await self.redis.close()
        if self.pool:
            await self.pool.disconnect()
        self.redis = None
        self.pool = None
