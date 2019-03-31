import json
import logging
import os

import redis

import mayday

logger = logging.getLogger()
logger.setLevel(mayday.get_log_level())
logger.addHandler(mayday.console_handler())


class RedisController:

    db_mapping = dict(search=1, post=1, quick_search=1, update=1, events=2, stats=2)

    def __init__(self, db_name: str = 'search', redis_client: redis.StrictRedis = None):

        if redis_client:
            self.client = redis_client
        else:
            self.db = self.db_mapping.get(db_name, 1)
            pool = redis.ConnectionPool(
                host=os.environ.get('REDIS_HOST', 'localhost'),
                port=os.environ.get('REDIS_PORT', 6379),
                db=self.db)
            self.client = redis.StrictRedis(connection_pool=pool)

    def _insert(self, key: str, value: str, expiration: int) -> bool:
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

    def clean(self, user_id: int, action: str) -> bool:
        key = self.get_key(user_id, action)
        self._delete(key)
        return bool(not self._load(key))

    def clean_all(self, user_id: int, module_name: str) -> int:
        assert 'start' in module_name
        for key in self.client.keys('{}_*'.format(user_id)):
            self.client.delete(key)

    def count(self, user_id: str) -> int:
        return len(self.client.keys('{}_*'.format(user_id)))

    def direct_read(self, user_id: int, action: str) -> str:
        return self.client.get(self.get_key(user_id, action)).decode()

    def save(self, user_id: int, action: str, content: dict, expiration=600) -> bool:
        return self._insert(self.get_key(user_id, action), json.dumps(content, ensure_ascii=False), expiration=expiration)

    def load(self, user_id: int, action: str) -> dict:
        return self._load(self.get_key(user_id, action))

    @staticmethod
    def get_key(user_id: int, action: str):
        return '{user_id}_{action}'.format(user_id=user_id, action=action)
