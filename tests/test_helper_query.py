import unittest

import mongomock
import pytest
from mayday.controllers import MongoController
from mayday.helpers import QueryHelper
from mayday.objects import Query


USER_ID = 123456789
USERNAME = 'pytest'


@pytest.mark.usefixtures()
class Test(unittest.TestCase):

    @pytest.fixture(autouse=True, scope='function')
    def before_all(self):
        client = mongomock.MongoClient()
        self.mongo = MongoController(mongo_client=client)
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

    '''
    def test_save_formal_query(self):
        query = Query(user_id=USER_ID, username=USERNAME, category_id=1)
        assert self.helper.save_query(query)

        tickets_in_db = self.mongo.load(
            db_name=self.helper.TICKET_DB_NAME, collection_name=self.helper.COLLECTION_NAME,
            query=dict(user_id=USER_ID, username=USERNAME))

        assert bool(tickets_in_db)
        query_in_db = tickets_in_db[0]

        assert query.category == query_in_db['category']
        assert query.date == query_in_db['date']
        assert query.price == query_in_db['price']
        assert query.quantity == query_in_db['quantity']
        assert query.section == query_in_db['section']
        assert query.row == query_in_db['row']
        assert query.seat == query_in_db['seat']
        assert query.status == query_in_db['status']
        assert query.remarks == query_in_db['remarks']
        assert query.wish_dates == query_in_db['wish_dates']
        assert query.wish_prices == query_in_db['wish_prices']
        assert query.wish_quantities == query_in_db['wish_quantities']
        assert query.user_id == query_in_db['user_id']
        assert query.username == query_in_db['username']
        assert query_in_db['ticket_id']  # can not know the query if before insert
        assert query_in_db['created_at']  # can not know the created ts before create
        assert query_in_db['updated_at']  # always change
    '''
