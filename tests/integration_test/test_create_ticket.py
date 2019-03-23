from mayday import Config
from mayday.controllers import MongoController
from mayday.helpers import TicketHelper, QueryHelper
from mayday.objects import Ticket, Query

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
    ticket = Ticket(user_id=USER_ID, username=USERNAME).to_obj(dumpy_ticket)
    assert helper.save_ticket(ticket)


'''
def test_update_ticket():
    config = Config()
    mongo = MongoController(mongo_config=config.mongo_config)
    ticket_helper = TicketHelper(mongo)
    query_helper = QueryHelper(mongo)

    query = Query(category_id=1, user_id=USER_ID, username=USERNAME)
    tickets = query_helper.search_by_query(query)
    assert len(tickets) == 1
    ticket = Ticket().to_obj(tickets[0])
    ticket.update_field('status', 4)
    assert isinstance(ticket, Ticket)
    new_ticket = ticket_helper.update_ticket(ticket)

    assert new_ticket.category == ticket.category
    assert new_ticket.ticket_id == ticket.ticket_id
    assert new_ticket.date == ticket.date
    assert new_ticket.price == ticket.price
    assert new_ticket.quantity == ticket.quantity
    assert new_ticket.section == ticket.section
    assert new_ticket.row == ticket.row
    assert new_ticket.seat == ticket.seat
    assert new_ticket.wish_dates == ticket.wish_dates
    assert new_ticket.wish_prices == ticket.wish_prices
    assert new_ticket.wish_quantities == ticket.wish_quantities
    assert new_ticket.source == ticket.source
    assert new_ticket.remarks == ticket.remarks
    assert new_ticket.status == ticket.status
    assert new_ticket.username == ticket.username
    assert new_ticket.user_id == ticket.user_id
'''
