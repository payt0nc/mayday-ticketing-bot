import mayday
import unittest
import pytest

from mayday.controllers.redis import RedisController
from mayday.helpers.feature_helpers import FeatureHelper
from mayday.helpers.query_helper import QueryHelper
from mayday.db.tables.tickets import TicketsModel
from mayday.objects.query import Query

USER_ID = 8081
USERNAME = 'test_account_1'


@pytest.mark.usefixtures()
class Test(unittest.TestCase):

    @pytest.fixture(autouse=True, scope='function')
    def before_all(self):
        pass

    def test_generate_query(self):
        redis = RedisController(db_name='search')
        helper = FeatureHelper(feature='search', redis_controller=redis)

        query = Query(category_id=1, user_id=USER_ID, username=USERNAME)
        assert helper.save_drafting_query(USER_ID, query)

        cached_query = helper.load_drafting_query(USER_ID)

        assert cached_query.category == 1
        assert cached_query.user_id == USER_ID
        assert cached_query.username == USERNAME

        # Update Field
        query = cached_query
        query.update_field('dates', 504)
        helper.save_drafting_query(USER_ID, query)
        cached_query = helper.load_drafting_query(USER_ID)
        assert cached_query.dates == query.dates

        # Update Field
        query = cached_query
        query.update_field('dates', 505)
        helper.save_drafting_query(USER_ID, query)
        cached_query = helper.load_drafting_query(USER_ID)
        assert cached_query.dates == query.dates
        assert cached_query.to_human_readable() == dict(
            category='原價轉讓',
            dates='5.4(Sat), 5.5(Sun)',
            prices='',
            quantities='',
            status='待交易',
            user_id=8081,
            username='test_account_1')

        # Save to Quick Search
        query_helper = QueryHelper(TicketsModel(mayday.engine, mayday.metadata, role='writer'))

        quick_search = helper.load_drafting_query(USER_ID)
        assert query_helper.save_quick_search(quick_search)

        quick_search_query = query_helper.load_quick_search(user_id=USER_ID)
        assert query.category == quick_search_query.category
        assert query.dates == quick_search_query.dates
        assert query.to_dict() == quick_search_query.to_dict()
