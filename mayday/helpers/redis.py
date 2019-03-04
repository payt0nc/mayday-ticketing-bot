import json
import logging
import traceback

import redis

logger = logging.getLogger(__name__)


class NoRedisConfigException(Exception):
    pass


class RedisHelper:

    def __init__(self, config: dict = None, redis_client: redis.StrictRedis = None):
        if redis_client:
            self._redis = redis_client
        elif config:
            pool = redis.ConnectionPool(host=config.get('redis_host', 'localhost'), db=config.get('redis_db', 0))
            self._redis = redis.StrictRedis(connection_pool=pool)
        else:
            raise NoRedisConfigException

    def _insert(self, key: str, value: str, expiration=3600) -> bool:
        try:
            return bool(self._redis.set(key, value, ex=expiration))
        except redis.exceptions.TimeoutError as timeout:
            logger.error(timeout)
        except redis.exceptions.LockError as locked:
            logger.error(locked)

    def _load(self, key: str) -> dict:
        try:
            result = self._redis.get(key)
            return json.loads(result.decode()) if result else dict()
        except redis.exceptions.TimeoutError as timeout:
            logger.error(timeout)
        except redis.exceptions.LockError as locked:
            logger.error(locked)

    def _delete(self, key: str) -> int:
        try:
            return self._redis.delete(key)
        except redis.exceptions.TimeoutError as timeout:
            logger.error(timeout)
        except redis.exceptions.LockError as locked:
            logger.error(locked)

    def save(self, profile: dict, expiration=3600) -> int:
        key = self.get_key(profile['user_id'], profile['action'])
        return self._insert(key, json.dumps(profile, ensure_ascii=False), expiration=expiration)

    def load(self, profile: dict) -> dict:
        key = self.get_key(profile['user_id'], profile['action'])
        return self._load(key)

    def clean(self, profile: dict) -> bool:
        key = self.get_key(profile['user_id'], profile['action'])
        self._delete(key)
        return bool(self._load(key))

    def direct_read(self, key: str) -> str:
        return self._redis.get(key).decode()

    @staticmethod
    def get_key(user_id: int, action: str):
        return '{user_id}_{action}'.format(user_id=user_id, action=action)
