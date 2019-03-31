import unittest
import pytest

from sqlalchemy import create_engine, MetaData
from mayday.objects.user import User
from mayday.db.tables.users import UsersModel


@pytest.mark.usefixtures()
class Test(unittest.TestCase):

    @pytest.fixture(autouse=True, scope='function')
    def before_all(self):
        engine = create_engine('sqlite://')
        metadata = MetaData(bind=engine)
        self.db = UsersModel(engine, metadata)

        # Create Table
        self.db.metadata.drop_all()
        self.db.metadata.create_all()
        self.db.role = 'writer'

        self.admin_user = User(user_profile=dict(
            user_id=1,
            username='testcase',
            last_name='pytest',
            first_name='unittest',
            is_bot=False,
            language_code='ZH'
        ))
        self.admin_user.admin_role = True
        self.db.raw_insert(self.admin_user.to_dict())

        self.blacklist_user = User(user_profile=dict(
            user_id=2,
            username='testcase',
            last_name='pytest',
            first_name='unittest',
            is_bot=False,
            language_code='ZH'
        ))
        self.blacklist_user.blacklist = True
        self.db.raw_insert(self.blacklist_user.to_dict())

    def test_new_user(self):
        new_user = User(user_profile=dict(
            user_id=123456789,
            username='testcase',
            last_name='pytest',
            first_name='unittest',
            is_bot=False,
            language_code='ZH'
        ))
        profile = self.db.auth(new_user)

        assert profile['is_admin'] is False
        assert profile['is_blacklist'] is False

    def test_admin_user(self):
        profile = self.db.auth(self.admin_user)
        assert profile['is_admin']
        assert profile['is_blacklist'] is False

    def test_blacklist_user(self):
        profile = self.db.auth(self.blacklist_user)
        assert profile['is_admin'] is False
        assert profile['is_blacklist']
