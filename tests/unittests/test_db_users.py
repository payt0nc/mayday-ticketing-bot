import unittest

import pytest
import sqlalchemy
from sqlalchemy import MetaData

from mayday.db.tables.users import Users
from mayday.objects.user import User

USER = User(user_profile=dict(
    user_id=123456789,
    username='test',
    first_name='tset',
    last_name='ttset'
))


@pytest.mark.usefixtures()
class TestCase(unittest.TestCase):

    @pytest.fixture(autouse=True, scope='function')
    def before_all(self):
        engine = sqlalchemy.create_engine('sqlite://')
        metadata = MetaData(bind=engine)
        self.db = Users(engine, metadata)

        # Create Table
        self.db.metadata.drop_all()
        self.db.metadata.create_all()
        self.db.role = 'writer'

    def test_get_auth(self):
        result = self.db.auth(USER)
        assert result
        assert result['is_blacklist'] is False
        assert result['is_admin'] is False

    def test_ban_user(self):
        self.db.auth(USER)
        assert self.db.ban_user(USER)

        user = self.db.get_user_profile(USER.user_id)

        assert user
        assert user.blacklist
        assert user.admin_role is False

    def test_get_user_profile(self):
        self.db.auth(USER)
        result = self.db.get_user_profile(USER.user_id)
        assert result
        assert isinstance(result, User)
        assert result.user_id == USER.user_id
        assert result.username == USER.username
