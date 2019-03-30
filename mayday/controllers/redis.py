import json
import logging
import os

import redis

import mayday

logger = logging.getLogger()
logger.setLevel(mayday.get_log_level())
logger.addHandler(mayday.console_handler())


class RedisController:

    def __init__(self, db_name: str = 'search', redis_client: redis.StrictRedis = None):

        if redis_client:
            self.client = redis_client
        else:
            pool = redis.ConnectionPool(
                host=os.environ.get('REDIS_HOST', 'localhost'),
                port=os.environ.get('REDIS_PORT', 6379),
                db=['search', 'post', 'quick_search', 'update', 'events', 'stats'].index(db_name))
            self.client = redis.StrictRedis(connection_pool=pool)

    def _insert(self, key: str, value: str, expiration=3600) -> bool:
        try:
            return bool(self.client.set(key, value, ex=expiration))
        except redis.exceptions.TimeoutError as timeout:
            logger.error(timeout)
        except redis.exceptions.LockError as locked:
            logger.error(locked)

    def _load(self, key: str) -> dict:
        try:
            result = self.client.get(key)
            return json.loads(result.decode()) if result else dict()
        except redis.exceptions.TimeoutError as timeout:
            logger.error(timeout)
        except redis.exceptions.LockError as locked:
            logger.error(locked)

    def _delete(self, key: str) -> int:
        try:
            return self.client.delete(key)
        except redis.exceptions.TimeoutError as timeout:
            logger.error(timeout)
        except redis.exceptions.LockError as locked:
            logger.error(locked)

    def save(self, user_id: int, action: str, content: dict, expiration=3600) -> bool:
        return self._insert(self.get_key(user_id, action), json.dumps(content, ensure_ascii=False), expiration=expiration)

    def load(self, user_id: int, action: str) -> dict:
        return self._load(self.get_key(user_id, action))

    def clean(self, user_id: int, action: str) -> bool:
        key = self.get_key(user_id, action)
        self._delete(key)
        return bool(not self._load(key))

    def direct_read(self, user_id: int, action: str) -> str:
        return self.client.get(self.get_key(user_id, action)).decode()

    @staticmethod
    def get_key(user_id: int, action: str):
        return '{user_id}_{action}'.format(user_id=user_id, action=action)
