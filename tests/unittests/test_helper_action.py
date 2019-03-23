import unittest

import pytest
from fakeredis import FakeStrictRedis
from mayday.controllers import RedisController
from mayday.helpers.action_helper import ActionHelper
from mayday.objects import Ticket, Query

USER_ID = 123456789
USERNAME = 'testcase'


@pytest.mark.usefixtures()
class Test(unittest.TestCase):

    @pytest.fixture(autouse=True, scope='function')
    def before_all(self):
        redis = RedisController(redis_client=FakeStrictRedis())
        self.helper = ActionHelper(redis_controller=redis)

    def test_last_choice(self):
        field = 'post_ticket'
        self.helper.save_last_choice(user_id=USER_ID, field=field)
        assert self.helper.load_last_choice(USER_ID) == dict(field=field)

    def test_drafting_ticket(self):
        ticket = Ticket(user_id=USER_ID, username=USERNAME)
        ticket.update_field('date', 503)
        self.helper.save_drafting_ticket(user_id=USER_ID, ticket=ticket)
        ticket_in_cache = self.helper.load_drafting_ticket(user_id=USER_ID)
        assert ticket_in_cache.to_dict() == ticket.to_dict()

        # Reset Ticket
        raw_ticket = Ticket(user_id=USER_ID, username=USERNAME)
        ticket_in_cache = self.helper.reset_drafting_ticket(user_id=USER_ID, username=USERNAME)
        assert ticket_in_cache.to_dict() == raw_ticket.to_dict()

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
