import logging
import unittest

import pytest
from mayday.objects import User

logger = logging.getLogger('test')


@pytest.mark.usefixtures()
class Test(unittest.TestCase):

    @pytest.fixture(autouse=True, scope='function')
    def before_all(self):
        pass

    def test_user_object_init(self):
        telegram_info = dict(
            id=123456789,
            username='testcase',
            last_name='pytest',
            first_name='test',
            is_bot=False,
            language_code='ZH'
        )
        profile = User(telegram_info).to_dict()
        assert profile['user_id'] == telegram_info['id']
        assert profile['username'] == telegram_info['username']
        assert profile['last_name'] == telegram_info['last_name']
        assert profile['first_name'] == telegram_info['first_name']
        assert profile['is_bot'] == telegram_info['is_bot']
        assert profile['language_code'] == telegram_info['language_code']
        assert profile['is_admin'] is False
        assert profile['is_blacklist'] is False

    def test_username_blank(self):
        telegram_info = dict(
            id=123456789,
            username='',
            last_name='pytest',
            first_name='test',
            is_bot=False,
            language_code='ZH'
        )
        profile = User(telegram_info)
        assert profile.is_username_blank()

        telegram_info.update(dict(username='testcase'))
        profile = User(telegram_info)
        assert profile.is_username_blank() is False
