from mayday import Config
from mayday.controllers import MongoController
from mayday.helpers.auth_helper import AuthHelper
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
    is_blacklist=False
)

BLACKLIST_PROFILE = dict(
    id=123456788,  # in telegram profile
    user_id=123456788,
    username='blacklist',
    last_name='pytest',
    first_name='test',
    is_bot=False,
    language_code='ZH',
    is_admin=False,
    is_blacklist=True
)


def test_new_user_auth():
    config = Config()
    mongo = MongoController(mongo_config=config.mongo_config)
    helper = AuthHelper(mongo)
    telegram_user_profile = dict(
        user_id=123456789,
        username='testcase',
        last_name='pytest',
        first_name='test',
        is_bot=False,
        language_code='ZH'
    )
    user = User(telegram_user_profile)
    profile_in_db = helper.auth(user)
    assert profile_in_db['user_id'] == telegram_user_profile['user_id']
    assert profile_in_db['username'] == telegram_user_profile['username']
    assert profile_in_db['is_admin'] is False
    assert profile_in_db['is_blacklist'] is False


def test_admin_auth():
    config = Config()
    mongo = MongoController(mongo_config=config.mongo_config)
    helper = AuthHelper(mongo)
    mongo.save(db_name=helper.DB_NAME, collection_name=helper.COLLECTION_NAME, content=ADMIN_PROFILE)
    profile_in_db = helper.auth(User(ADMIN_PROFILE))
    assert mongo.count(
        db_name=config.schema_config['user_db_name'],
        collection_name=config.schema_config['user_collection_name'],
        query=dict(user_id=ADMIN_PROFILE['id'])) == 1
    assert profile_in_db['user_id'] == ADMIN_PROFILE['id']
    assert profile_in_db['username'] == ADMIN_PROFILE['username']
    assert profile_in_db['is_admin']
    assert profile_in_db['is_blacklist'] is False


def test_blacklist_auth():
    config = Config()
    mongo = MongoController(mongo_config=config.mongo_config)
    helper = AuthHelper(mongo)
    mongo.save(db_name=helper.DB_NAME, collection_name=helper.COLLECTION_NAME, content=BLACKLIST_PROFILE)
    profile_in_db = helper.auth(User(BLACKLIST_PROFILE))
    assert mongo.count(
        db_name=config.schema_config['user_db_name'],
        collection_name=config.schema_config['user_collection_name'],
        query=dict(user_id=BLACKLIST_PROFILE['id'])) == 1
    assert profile_in_db['user_id'] == BLACKLIST_PROFILE['id']
    assert profile_in_db['username'] == BLACKLIST_PROFILE['username']
    assert profile_in_db['is_admin'] is False
    assert profile_in_db['is_blacklist']
