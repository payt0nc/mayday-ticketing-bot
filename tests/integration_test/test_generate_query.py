from mayday.objects import Query
from mayday.helpers import QueryHelper
from mayday import Config
from mayday.controllers import MongoController

USER_ID = 8081
USERNAME = 'test_account_1'


def test_generate_query():
    config = Config()
    mongo = MongoController(mongo_config=config.mongo_config)
    helper = QueryHelper(mongo)

    query = Query(category_id=1, user_id=USER_ID, username=USERNAME)
    cached_query = helper.create_blank_query(query)

    assert cached_query.category == 1
    assert cached_query.user_id == USER_ID
    assert cached_query.username == USERNAME

    # Update Field
    query = cached_query
    query.update_field('dates', 504)
    cached_query = helper.update_cache_query(query)
    assert cached_query.dates == query.dates

    # Update Field
    query = cached_query
    query.update_field('dates', 505)
    cached_query = helper.update_cache_query(query)
    assert cached_query.dates == query.dates
    assert cached_query.to_human_readable() == dict(
        category='原價轉讓',
        dates='5.4(Sat), 5.5(Sun)',
        prices='',
        quantities='',
        status='待交易',
        user_id=8081,
        username='test_account_1'
    )

    # Save to Quick Search
    query = cached_query
    assert helper.save_quick_search(cached_query)
    cached_query = helper.load_quick_search(user_id=USER_ID, username=USERNAME)
    assert query.category == cached_query.category
    assert query.dates == cached_query.dates
    assert query.to_dict() == cached_query.to_dict()
