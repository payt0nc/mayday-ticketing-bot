import pytest
from mayday import engine, metadata
from mayday.db.tables.users import UsersModel
from mayday.objects.user import User

ADMIN_PROFILE = dict(
    id=123456787,  # in telegram profile
    user_id=123456787,
    username='admin',
    last_name='pytest',
    first_name='test',
    is_bot=False,
    language_code='ZH',
    is_admin=True,
    is_blacklist=False)

BLACKLIST_PROFILE = dict(
    id=123456788,  # in telegram profile
    user_id=123456788,
    username='blacklist',
    last_name='pytest',
    first_name='test',
    is_bot=False,
    language_code='ZH',
    is_admin=False,
    is_blacklist=True)


@pytest.mark.usefixtures()
class Test:

    @pytest.fixture(autouse=True, scope='function')
    def before_all(self):
        self.user_table = UsersModel(engine, metadata, role='writer')

    def test_new_user_auth(self):
        telegram_user_profile = dict(
            user_id=123456789,
            username='testcase',
            last_name='pytest',
            first_name='test',
            is_bot=False,
            language_code='ZH')
        profile_in_db = self.user_table.auth(User(user_profile=telegram_user_profile))
        assert profile_in_db['is_admin'] is False
        assert profile_in_db['is_blacklist'] is False

    def test_admin_auth(self):
        profile_in_db = self.user_table.auth(User(user_profile=ADMIN_PROFILE))
        assert profile_in_db['is_admin']
        assert profile_in_db['is_blacklist'] is False

    def test_blacklist_auth(self):
        profile_in_db = self.user_table.auth(User(user_profile=BLACKLIST_PROFILE))
        assert profile_in_db['is_admin'] is False
        assert profile_in_db['is_blacklist']
