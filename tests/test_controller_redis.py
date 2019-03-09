import unittest

import pytest
from fakeredis import FakeStrictRedis
from mayday.controllers.redis import RedisHelper


class TestCase(unittest.TestCase):

    def test_redis_load(self):
        redis = RedisHelper(redis_client=FakeStrictRedis())
        user_profile = dict(user_id=123456789, action='test', content=dict(test='test'))
        redis.save(user_profile)
        result = redis.load(user_profile)

        assert result == user_profile
