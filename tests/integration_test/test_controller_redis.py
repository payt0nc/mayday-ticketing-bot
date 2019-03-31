import json

import pytest
from mayday.controllers.redis import RedisController


USER_ID = 123456789
ACTION = 'test'


@pytest.mark.usefixtures()
class Test:

    @pytest.fixture(autouse=True, scope='function')
    def before_all(self):
        pass

    def test_redis_key(self):
        redis = RedisController()
        assert redis.get_key(USER_ID, ACTION) == '123456789_test'

    def test_redis(self):
        redis = RedisController()
        user_profile = dict(test='test')
        assert redis.save(USER_ID, ACTION, user_profile)
        assert user_profile == redis.load(USER_ID, ACTION)
        # Delete
        assert redis.clean(USER_ID, ACTION)

    def test_redis_direct_read(self):
        redis = RedisController()
        user_profile = dict(test='test')
        assert redis.save(USER_ID, ACTION, user_profile)
        assert redis.direct_read(USER_ID, ACTION) == json.dumps(user_profile)
