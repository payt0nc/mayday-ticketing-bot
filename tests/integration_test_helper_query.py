import unittest

import pytest
from mayday import Config
from mayday.controllers import MongoController
from mayday.helpers import QueryHelper
from mayday.objects import Query
from mayday.objects import Ticket

USER_ID = 123456789
USERNAME = 'pytest'


@pytest.mark.usefixtures()
class Test(unittest.TestCase):

    @pytest.fixture(autouse=True, scope='function')
    def before_all(self):
        config = Config().mongo_config
        self.mongo = MongoController(mongo_config=config)
        self.helper = QueryHelper(mongo_controller=self.mongo)

    def test_create_cache_query(self):
        query = Query(user_id=USER_ID, username=USERNAME, category_id=1)
        query_in_cache = self.helper.create_blank_query(query)

        assert query_in_cache.category == query.category

        assert query_in_cache.dates == query.dates
        assert query_in_cache.prices == query.prices
        assert query_in_cache.quantities == query.quantities
        assert query_in_cache.status == query.status
        assert query_in_cache.user_id == query.user_id
        assert query_in_cache.username == query.username

        assert query_in_cache.created_at  # can not know the created ts before create
        assert query_in_cache.updated_at  # always change

    def test_update_cache_query(self):
        query = Query(user_id=USER_ID, username=USERNAME, category_id=1)
        query = self.helper.update_cache_query(query)
        assert query.dates == list()

        query.update_field('dates', 503)
        query_in_cache = self.helper.update_cache_query(query)
        assert query_in_cache.dates == query.dates

        query.update_field('dates', 504)
        assert query.dates == [503, 504]
        query_in_cache = self.helper.update_cache_query(query)
        assert query_in_cache.dates == [503, 504]

        query_in_cache = self.helper.load_cache_ticket(user_id=USER_ID, username=USERNAME)
        assert query_in_cache.dates == [503, 504]

    def test_reset_cache_query_with_query_in_cache(self):
        query = Query(user_id=USER_ID, username=USERNAME, category_id=1)
        query = self.helper.create_blank_query(query)
        query.update_field('dates', 503)

        query = self.helper.update_cache_query(query)
        assert query.dates == [503]

        query_in_cache = self.helper.reset_cache_query(query)
        assert query_in_cache.dates == list()

    def test_reset_cache_query_without_query_in_cache(self):
        query = Query(user_id=USER_ID, username=USERNAME, category_id=1)
        query_in_cache = self.helper.reset_cache_query(query)
        assert query_in_cache.dates == list()

    def test_save_and_load_quick_search_query(self):
        query = Query(user_id=USER_ID, username=USERNAME, category_id=1)
        query.update_field('dates', 503)
        query.update_field('dates', 504)
        query.update_field('prices', 1)

        assert self.helper.save_quick_search(query)

        quick_search_queries = self.mongo.load(
            db_name=self.helper.QUICK_SEARCH_QUERY_DB_NAME, collection_name=self.helper.QUICK_SEARCH_COLLECTION_NAME,
            query=dict(user_id=USER_ID, username=USERNAME))

        assert bool(quick_search_queries)
        quick_search_query = quick_search_queries[0]
        assert quick_search_query['dates'] == query.dates
        assert quick_search_query['prices'] == query.prices

        quick_search_query = self.helper.load_quick_search(USER_ID, USERNAME)
        assert quick_search_query.dates == query.dates
        assert quick_search_query.prices == query.prices

    def test_search_by_conditions(self):
        query = Query(user_id=USER_ID, username=USERNAME, category_id=1)
        query.update_field('dates', 503)
        query.update_field('dates', 504)
        query.update_field('prices', 1)

        ticket = Ticket(username=USERNAME, user_id=USER_ID)
        ticket.category = 1
        ticket.date = 503
        ticket.price = 1
        ticket.quantity = 2
        ticket.status = 1
        ticket.section = 'D3'
        assert ticket.validate()['status']
        self.mongo.save(
            db_name=self.helper.TICKET_DB_NAME, collection_name=self.helper.TICKET_COLLECTION_NAME,
            content=ticket.to_dict())

        # By one query
        result = self.helper.search_by_query(query)[0]
        assert result['category'] == ticket.category
        assert result['date'] == ticket.date
        assert result['price'] == ticket.price
        assert result['quantity'] == ticket.quantity
        assert result['status'] == ticket.status

        # By Section
        result = self.helper.search_by_section('D3')[0]
        assert result['section'] == ticket.section
        assert result['category'] == ticket.category
        assert result['date'] == ticket.date
        assert result['price'] == ticket.price
        assert result['quantity'] == ticket.quantity
        assert result['status'] == ticket.status

        # By Date
        result = self.helper.search_by_date(503)[0]
        assert result['section'] == ticket.section
        assert result['category'] == ticket.category
        assert result['date'] == ticket.date
        assert result['price'] == ticket.price
        assert result['quantity'] == ticket.quantity
        assert result['status'] == ticket.status
