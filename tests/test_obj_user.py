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
        profile = User(telegram_info)
        self.assertDictEqual(telegram_info, profile.to_dict())

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
        self.assertFalse(profile.is_username_blank())

        telegram_info.update(dict(username='testcase'))
        profile = User(telegram_info)
        self.assertTrue(profile.is_username_blank())
