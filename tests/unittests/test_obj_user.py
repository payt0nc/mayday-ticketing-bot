import logging
import unittest

import pytest
from mayday.objects import User
from telegram import User as TelegramUser

logger = logging.getLogger('test')

TELEGRAM_INFO = dict(
    id=123456789,
    username='',
    last_name='pytest',
    first_name='test',
    is_bot=False,
    language_code='ZH'
)


class Test(unittest.TestCase):

    def test_user_object_init(self):

        profile = User(telegram_info=TELEGRAM_INFO).to_dict()
        assert profile['user_id'] == TELEGRAM_INFO['id']
        assert profile['username'] == TELEGRAM_INFO['username']
        assert profile['last_name'] == TELEGRAM_INFO['last_name']
        assert profile['first_name'] == TELEGRAM_INFO['first_name']
        assert profile['is_bot'] == TELEGRAM_INFO['is_bot']
        assert profile['language_code'] == TELEGRAM_INFO['language_code']
        assert profile['is_admin'] is False
        assert profile['is_blacklist'] is False

    def test_username_blank(self):

        profile = User(telegram_info=TELEGRAM_INFO)
        assert profile.is_username_blank()

        TELEGRAM_INFO.update(dict(username='testcase'))
        profile = User(telegram_info=TELEGRAM_INFO)
        assert profile.is_username_blank() is False

    def test_convert_telegram_user_to_user(self):
        tg_user = TelegramUser(id=123456789, first_name='test', last_name='pytest',
                               username='testcase', language_code='ZH', is_bot=False)

        user = User(telegram_user=tg_user)

        assert user.user_id == tg_user.id
        assert user.username == tg_user.username
        assert user.is_username_blank() is False

    def test_set_user_role(self):
        admin_user = User(telegram_info=TELEGRAM_INFO)
        admin_user.admin_role = True
        assert admin_user.admin_role

        admin_user = User(telegram_info=TELEGRAM_INFO)
        admin_user.blacklist = True
        assert admin_user.blacklist
