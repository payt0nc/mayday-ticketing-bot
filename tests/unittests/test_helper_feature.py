import unittest

import pytest
from fakeredis import FakeStrictRedis
from mayday.controllers.redis import RedisController
from mayday.helpers.feature_helpers import FeatureHelper
from mayday.objects.ticket import Ticket
from mayday.objects.query import Query

USER_ID = 123456789
USERNAME = 'testcase'


@pytest.mark.usefixtures()
class Test(unittest.TestCase):

    @pytest.fixture(autouse=True, scope='function')
    def before_all(self):
        redis = RedisController(redis_client=FakeStrictRedis())
        self.helper = FeatureHelper(feature='test', redis_controller=redis)

    def test_cache(self):
        assert self.helper.save_cache(USER_ID, 'test')
        assert self.helper.load_cache(USER_ID) == 'test'

    def test_last_choice(self):
        field = 'post_ticket'
        assert self.helper.save_last_choice(user_id=USER_ID, field=field) is False

        field = 'check'
        assert self.helper.save_last_choice(user_id=USER_ID, field=field)
        assert self.helper.load_last_choice(USER_ID) == field

    def test_drafting_ticket(self):
        ticket = Ticket(user_id=USER_ID, username=USERNAME)
        ticket.update_field('date', 503)
        self.helper.save_drafting_ticket(user_id=USER_ID, ticket=ticket)
        ticket_in_cache = self.helper.load_drafting_ticket(user_id=USER_ID)
        assert ticket_in_cache.user_id
        assert ticket_in_cache.user_id == ticket.user_id
        assert ticket_in_cache.username
        assert ticket_in_cache.username == ticket.username
        assert ticket_in_cache.to_dict() == ticket.to_dict()

        # Reset Ticket
        raw_ticket = Ticket(user_id=USER_ID, username=USERNAME)
        ticket_in_cache = self.helper.reset_drafting_ticket(user_id=USER_ID, username=USERNAME)
        assert ticket_in_cache.to_dict() == raw_ticket.to_dict()
        assert ticket_in_cache.username == raw_ticket.username

    def test_drafting_query(self):
        query = Query(category_id=1, user_id=USER_ID, username=USERNAME)
        query.update_field('dates', 503)
        self.helper.save_drafting_query(user_id=USER_ID, query=query)
        query_in_cache = self.helper.load_drafting_query(user_id=USER_ID)
        assert query_in_cache.to_dict() == query.to_dict()

        # Reset Ticket
        raw_query = Query(category_id=1, user_id=USER_ID, username=USERNAME)
        query_in_cache = self.helper.reset_drafting_query(user_id=USER_ID, username=USERNAME, category=1)
        assert query_in_cache.to_dict() == raw_query.to_dict()
