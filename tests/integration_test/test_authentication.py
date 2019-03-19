import pytest
from mayday import Config
from mayday.helpers import AuthHelper
from mayday.controllers import MongoController
from mayday.objects import User

ADMIN_PROFILE = dict(
    id=123456787,
    user_id=123456787,
    username='admin',
    last_name='pytest',
    first_name='test',
    is_bot=False,
    language_code='ZH',
    is_admin=True,
    is_blacklist=False
)

BLACKLIST_PROFILE = dict(
    id=123456788,
    user_id=123456788,
    username='blacklist',
    last_name='pytest',
    first_name='test',
    is_bot=False,
    language_code='ZH',
    is_admin=False,
    is_blacklist=True
)


@pytest.fixture
def init_auth_db():
    config = Config()
    mongo = MongoController(mongo_config=config.mongo_config)
    helper = AuthHelper(mongo)
    mongo.delete_all(
        db_name=helper.DB_NAME, collection_name=helper.COLLECTION_NAME, query=dict())
    mongo.save(
        db_name=helper.DB_NAME, collection_name=helper.COLLECTION_NAME, content=ADMIN_PROFILE)
    mongo.save(
        db_name=helper.DB_NAME, collection_name=helper.COLLECTION_NAME, content=BLACKLIST_PROFILE)
    return mongo, helper


def test_new_user_auth(init_auth_db):
    mongo, helper = init_auth_db
    telegram_user_profile = dict(
        id=123456789,
        username='testcase',
        last_name='pytest',
        first_name='test',
        is_bot=False,
        language_code='ZH'
    )
    user = User(telegram_user_profile)
    profile_in_db = helper.auth(user)
    assert profile_in_db['user_id'] == telegram_user_profile['id']
    assert profile_in_db['username'] == telegram_user_profile['username']
    assert profile_in_db['is_admin'] is False
    assert profile_in_db['is_blacklist'] is False


def test_admin_auth(init_auth_db):
    mongo, helper = init_auth_db
    user = User(ADMIN_PROFILE)
    profile_in_db = helper.auth(user)
    assert profile_in_db['user_id'] == ADMIN_PROFILE['id']
    assert profile_in_db['username'] == ADMIN_PROFILE['username']
    assert profile_in_db['is_admin']
    assert profile_in_db['is_blacklist'] is False


def test_blacklist_auth(init_auth_db):
    mongo, helper = init_auth_db
    profile_in_db = helper.auth(User(BLACKLIST_PROFILE))
    assert profile_in_db['user_id'] == BLACKLIST_PROFILE['id']
    assert profile_in_db['username'] == BLACKLIST_PROFILE['username']
    assert profile_in_db['is_admin'] is False
    assert profile_in_db['is_blacklist']
