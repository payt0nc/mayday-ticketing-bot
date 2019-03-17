import unittest
import pytest
import mongomock

from mayday.controllers.mongo import MongoController
from mayday.helpers.auth_helper import AuthHelper
from mayday.objects import User


@pytest.mark.usefixtures()
class Test(unittest.TestCase):

    @pytest.fixture(autouse=True, scope='function')
    def before_all(self):
        client = mongomock.MongoClient()
        mongo = MongoController(mongo_client=client)
        self.admin_user = User(dict(
            id=0,
            username='testcase',
            last_name='pytest',
            first_name='test',
            is_bot=False,
            language_code='ZH'
        ))
        self.admin_user.admin_role = True

        self.blacklist_user = User(dict(
            id=1,
            username='testcase',
            last_name='pytest',
            first_name='test',
            is_bot=False,
            language_code='ZH'
        ))
        self.blacklist_user.blacklist = True

        mongo.save('user', 'users', self.admin_user.to_dict())
        mongo.save('user', 'users', self.blacklist_user.to_dict())
        self.helper = AuthHelper(mongo_controller=mongo)

    def test_new_user(self):
        new_user = User(dict(
            id=123456789,
            username='testcase',
            last_name='pytest',
            first_name='test',
            is_bot=False,
            language_code='ZH'
        ))
        profile = self.helper.auth(new_user)

        assert profile['is_admin'] is False
        assert profile['is_blacklist'] is False

    def test_admin_user(self):
        profile = self.helper.auth(self.admin_user)
        assert profile['is_admin'] is True
        assert profile['is_blacklist'] is False

    def test_blacklist_user(self):
        profile = self.helper.auth(self.blacklist_user)
        assert profile['is_admin'] is False
        assert profile['is_blacklist'] is True
