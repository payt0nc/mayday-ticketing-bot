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
        self.mongo = MongoController(mongo_client=client)
        self.helper = TicketHelper(mongo_controller=self.mongo)

    def test_save_formal_ticket(self):
        ticket = Ticket(user_id=USER_ID, username=USERNAME)
        assert self.helper.save_ticket(ticket)

        tickets_in_db = self.mongo.load(
            db_name=self.helper.TICKET_DB_NAME, collection_name=self.helper.TICKET_COLLECTION_NAME,
            query=dict(user_id=USER_ID, username=USERNAME))

        assert bool(tickets_in_db)
        ticket_in_db = Ticket(user_id=USER_ID, username=USERNAME).to_obj(tickets_in_db[0])

        assert ticket.category == ticket_in_db.category
        assert ticket.date == ticket_in_db.date
        assert ticket.price == ticket_in_db.price
        assert ticket.quantity == ticket_in_db.quantity
        assert ticket.section == ticket_in_db.section
        assert ticket.row == ticket_in_db.row
        assert ticket.seat == ticket_in_db.seat
        assert ticket.status == ticket_in_db.status
        assert ticket.remarks == ticket_in_db.remarks
        assert ticket.wish_dates == ticket_in_db.wish_dates
        assert ticket.wish_prices == ticket_in_db.wish_prices
        assert ticket.wish_quantities == ticket_in_db.wish_quantities
        assert ticket.user_id == ticket_in_db.user_id
        assert ticket.username == ticket_in_db.username
        assert ticket_in_db.ticket_id  # can not know the ticket if before insert
        assert ticket_in_db.created_at  # can not know the created ts before create
        assert ticket_in_db.updated_at  # always change
