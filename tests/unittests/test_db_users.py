import unittest

import pytest
import sqlalchemy
from sqlalchemy import MetaData

from mayday.db.tables.users import Users

USER = dict(
    user_id=123456789,
    username='test',
    first_name='tset',
    last_name='ttset'
)


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
        result = self.db.get_auth(USER)
        assert result
        assert result['is_banned'] is False
        assert result['is_admin'] is False

    def test_ban_user(self):
        self.db.get_auth(USER)
        result = self.db.ban_user(USER)

        assert result
        assert result['is_banned'] is True
        assert result['is_admin'] is False

    def test_get_user_profile(self):
        self.db.get_auth(USER)
        result = self.db.get_user_profile(USER)
        assert result
        assert {x for x in result.keys()} == {'id', 'first_name', 'last_name', 'is_banned',
                                              'is_admin', 'created_at', 'updated_at', 'user_id', 'username'}
