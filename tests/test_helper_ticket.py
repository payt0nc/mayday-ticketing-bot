import unittest

import mongomock
import pytest
from mayday.controllers import MongoController
from mayday.helpers import TicketHelper
from mayday.objects import Ticket


USER_ID = 123456789
USERNAME = 'pytest'


@pytest.mark.usefixtures()
class Test(unittest.TestCase):

    @pytest.fixture(autouse=True, scope='function')
    def before_all(self):
        client = mongomock.MongoClient()
        mongo = MongoController(mongo_client=client)
        self.helper = TicketHelper(mongo_controller=mongo)

    def test_create_cache_ticket(self):

        ticket = Ticket(user_id=USER_ID, username=USERNAME)
        ticket_in_cache = self.helper.create_blank_ticket(ticket)

        assert ticket_in_cache['category'] == ticket.category
        assert ticket_in_cache['ticket_id']  # can not know the ticket if before insert
        assert ticket_in_cache['date'] == ticket.date
        assert ticket_in_cache['price'] == ticket.price
        assert ticket_in_cache['quantity'] == ticket.quantity
        assert ticket_in_cache['section'] == ticket.section
        assert ticket_in_cache['row'] == ticket.row
        assert ticket_in_cache['seat'] == ticket.seat
        assert ticket_in_cache['status'] == ticket.status
        assert ticket_in_cache['remarks'] == ticket.remarks
        assert ticket_in_cache['wish_dates'] == ticket.wish_dates
        assert ticket_in_cache['wish_prices'] == ticket.wish_prices
        assert ticket_in_cache['wish_quantities'] == ticket.wish_quantities
        assert ticket_in_cache['user_id'] == ticket.user_id
        assert ticket_in_cache['username'] == ticket.username
        assert ticket_in_cache['created_at']  # can not know the created ts before create
        assert ticket_in_cache['updated_at']  # always change

    def test_update_cache_ticket(self):
        pass
