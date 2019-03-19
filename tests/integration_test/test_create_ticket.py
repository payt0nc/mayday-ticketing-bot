from mayday import Config
from mayday.controllers import MongoController
from mayday.helpers import TicketHelper
from mayday.objects import Ticket

USER_ID = 123456789
USERNAME = 'it_search_ticket'


def test_create_ticket():
    config = Config()
    mongo = MongoController(mongo_config=config.mongo_config)
    helper = TicketHelper(mongo)
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
    assert helper.save_ticket(ticket)
