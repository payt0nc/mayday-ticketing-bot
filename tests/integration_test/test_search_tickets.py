from mayday import Config
from mayday.controllers import MongoController
from mayday.helpers.query_helper import QueryHelper
from mayday.objects.query import Query
from mayday.objects.ticket import Ticket


def test_search_ticket_by_date():
    config = Config()
    mongo = MongoController(mongo_config=config.mongo_config)
    helper = QueryHelper(mongo)

    tickets = helper.search_by_date(505)
    assert len(tickets) == 1
    ticket = Ticket().to_obj(tickets[0])
    assert ticket.category == 1
    assert ticket.ticket_id
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
    assert ticket['ticket_id']
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
    assert ticket.ticket_id
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
    assert ticket.ticket_id
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


def test_search_ticket_by_user_id():
    helper = QueryHelper(mongo_controller=None)
    tickets = helper.search_by_user_id(8082)

    assert len(tickets) == 1
    ticket = tickets[0]

    assert ticket.category == 2
    assert ticket.ticket_id
    assert ticket.date == 504
    assert ticket.price == 1
    assert ticket.quantity == 1
    assert ticket.section == 'A1'
    assert ticket.row == ''
    assert ticket.seat == ''
    assert ticket.wish_dates == [504, 505]
    assert ticket.wish_prices == [1, 2]
    assert ticket.wish_quantities == [1]
    assert ticket.source == 1
    assert ticket.remarks == ''
    assert ticket.status == 1
    assert ticket.username == 'test_account_2'
    assert ticket.user_id == 8082


def test_search_ticket_by_ticket_id():
    helper = QueryHelper(mongo_controller=None)
    tickets = helper.search_by_user_id(8082)
    assert tickets
    ticket = helper.search_by_ticket_id(tickets[0].ticket_id)
    assert ticket
    assert ticket.category == 2
    assert ticket.ticket_id
    assert ticket.date == 504
    assert ticket.price == 1
    assert ticket.quantity == 1
    assert ticket.section == 'A1'
    assert ticket.row == ''
    assert ticket.seat == ''
    assert ticket.wish_dates == [504, 505]
    assert ticket.wish_prices == [1, 2]
    assert ticket.wish_quantities == [1]
    assert ticket.source == 1
    assert ticket.remarks == ''
    assert ticket.status == 1
    assert ticket.username == 'test_account_2'
    assert ticket.user_id == 8082
