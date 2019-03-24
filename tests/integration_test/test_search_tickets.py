from mayday import Config
from mayday.controllers import MongoController
from mayday.helpers import QueryHelper
from mayday.objects import Query, Ticket


def test_search_ticket_by_date():
    config = Config()
    mongo = MongoController(mongo_config=config.mongo_config)
    helper = QueryHelper(mongo)

    tickets = helper.search_by_date(505)
    assert len(tickets) == 1
    ticket = Ticket().to_obj(tickets[0])
    assert ticket.category == 1
    assert ticket.ticket_id == ''
    assert ticket.date == 505
    assert ticket.price == 2
    assert ticket.quantity == 1
    assert ticket.section == 'C1'
    assert ticket.row == ''
    assert ticket.seat == ''
    assert ticket.wish_dates == list()
    assert ticket.wish_prices == list()
    assert ticket.wish_quantities == list()
    assert ticket.source == 1
    assert ticket.remarks == ''
    assert ticket.status == 1
    assert ticket.username == 'test_account_1'
    assert ticket.user_id == 8081


def test_search_ticket_by_section():
    config = Config()
    mongo = MongoController(mongo_config=config.mongo_config)
    helper = QueryHelper(mongo)

    tickets = helper.search_by_section('C1')
    assert len(tickets) == 1
    ticket = tickets[0]
    assert ticket['category'] == 1
    assert ticket['ticket_id'] == ''
    assert ticket['date'] == 505
    assert ticket['price'] == 2
    assert ticket['quantity'] == 1
    assert ticket['section'] == 'C1'
    assert ticket['row'] == ''
    assert ticket['seat'] == ''
    assert ticket['wish_dates'] == list()
    assert ticket['wish_prices'] == list()
    assert ticket['wish_quantities'] == list()
    assert ticket['source'] == 1
    assert ticket['remarks'] == ''
    assert ticket['status'] == 1
    assert ticket['username'] == 'test_account_1'
    assert ticket['user_id'] == 8081


def test_search_ticket_by_query():
    config = Config()
    mongo = MongoController(mongo_config=config.mongo_config)
    helper = QueryHelper(mongo)

    tickets = helper.search_by_query(Query(category_id=1).to_obj(dict(prices=[2])))
    assert len(tickets) == 1
    ticket = tickets[0]
    assert ticket.category == 1
    assert ticket.ticket_id == ''
    assert ticket.date == 505
    assert ticket.price == 2
    assert ticket.quantity == 1
    assert ticket.section == 'C1'
    assert ticket.row == ''
    assert ticket.seat == ''
    assert ticket.wish_dates == list()
    assert ticket.wish_prices == list()
    assert ticket.wish_quantities == list()
    assert ticket.source == 1
    assert ticket.remarks == ''
    assert ticket.status == 1
    assert ticket.username == 'test_account_1'
    assert ticket.user_id == 8081

    tickets = helper.search_by_query(Query(category_id=1).to_obj(dict(prices=[2])))
    assert len(tickets) == 1
    ticket = tickets[0]
    assert ticket.category == 1
    assert ticket.ticket_id == ''
    assert ticket.date == 505
    assert ticket.price == 2
    assert ticket.quantity == 1
    assert ticket.section == 'C1'
    assert ticket.row == ''
    assert ticket.seat == ''
    assert ticket.wish_dates == list()
    assert ticket.wish_prices == list()
    assert ticket.wish_quantities == list()
    assert ticket.source == 1
    assert ticket.remarks == ''
    assert ticket.status == 1
    assert ticket.username == 'test_account_1'
    assert ticket.user_id == 8081
