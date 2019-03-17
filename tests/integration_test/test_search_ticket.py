import unittest

import pytest
from mayday import Config
from mayday.controllers import MongoController
from mayday.helpers import QueryHelper, TicketHelper
from mayday.objects import Query, Ticket

USER_ID = 123456789
USERNAME = 'it_search_ticket'


@pytest.mark.usefixtures()
class Test(unittest.TestCase):

    @pytest.fixture(autouse=True, scope='function')
    def before_all(self):
        config = Config()
        self.mongo = MongoController(mongo_config=config.mongo_config)
        self.helper = QueryHelper(self.mongo)
        self.mongo.delete_all(db_name=self.helper.CACHE_DB_NAME,
                              collection_name=self.helper.TICKET_COLLECTION_NAME, query=dict())
        self.mongo.delete_all(db_name=self.helper.TICKET_DB_NAME,
                              collection_name=self.helper.TICKET_COLLECTION_NAME, query=dict())

    def test_search_ticket(self):
        dumpy_ticket = dict(
            category=1,
            ticket_id='',
            date=504,
            price=1,
            quantity=1,
            section='A1',
            row='',
            seat='',
            wish_dates=list(),
            wish_prices=list(),
            wish_quantities=list(),
            source=1,
            remarks='',
            status=1,
            username=USERNAME,
            user_id=USER_ID,
        )
        ticket = Ticket(USER_ID, USERNAME).to_obj(dumpy_ticket)
        ticket_helper = TicketHelper(self.mongo)
        assert ticket_helper.save_ticket(ticket)

        query = Query(user_id=USER_ID, username=USERNAME, category_id=1)
        results = self.helper.search_by_query(query)
        assert len(results) == 1

        ticket = Ticket(USER_ID, USERNAME).to_obj(results[0])

        assert str(results[0]['_id'])[-6:] == ticket.ticket_id
        assert ticket.category == 1
        assert ticket.date == 504
        assert ticket.price == 1
        assert ticket.quantity == 1
        assert ticket.section == 'A1'
        assert ticket.row == ''
        assert ticket.seat == ''
        assert ticket.wish_dates == list()
        assert ticket.wish_prices == list()
        assert ticket.wish_quantities == list()
        assert ticket.source == 1
        assert ticket.remarks == ''
        assert ticket.status == 1
