from typing import Tuple
from tracardi.service.storage.redis_client import RedisClient


class Limiter:

    def __init__(self, limit: int, ttl: int):
        self._ttl = ttl
        self._limit = limit
        self._redis = RedisClient()

    def limit(self, key: str) -> Tuple[bool, int]:

        key = f"throttle:{key}"

        req = self._redis.client.incr(key)
        if req == 1:
            self._redis.client.expire(key, self._ttl)
            ttl = self._ttl
        else:
            ttl = self._redis.client.ttl(key)

        return req <= self._limit, ttl
