import json

import redis
import mayday


class NoRedisConfigException(Exception):
    pass


class RedisController:

    def __init__(self, redis_db: int, redis_client: redis.StrictRedis = None, redis_config: dict = None):
        self.logger = mayday.get_default_logger(log_name='redis_controller')
        if redis_client:
            self.client = redis_client
        elif redis_config:
            pool = redis.ConnectionPool(host=redis_config['host'], port=redis_config['port'], db=redis_db)
            self.client = redis.StrictRedis(connection_pool=pool)
        else:
            raise NoRedisConfigException

    def _insert(self, key: str, value: str, expiration=3600) -> bool:
        try:
            return bool(self.client.set(key, value, ex=expiration))
        except redis.exceptions.TimeoutError as timeout:
            self.logger.error(timeout)
        except redis.exceptions.LockError as locked:
            self.logger.error(locked)

    def _load(self, key: str) -> dict:
        try:
            result = self.client.get(key)
            return json.loads(result.decode()) if result else dict()
        except redis.exceptions.TimeoutError as timeout:
            self.logger.error(timeout)
        except redis.exceptions.LockError as locked:
            self.logger.error(locked)

    def _delete(self, key: str) -> int:
        try:
            return self.client.delete(key)
        except redis.exceptions.TimeoutError as timeout:
            self.logger.error(timeout)
        except redis.exceptions.LockError as locked:
            self.logger.error(locked)

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
