
import pytest

from mayday.helpers.query_helper import QueryHelper
from mayday.objects.query import Query


@pytest.mark.usefixtures('database')
class Test:

    @pytest.fixture(autouse=True)
    def before_all(self, database: dict):
        self.db = database['ticket_table']

    def test_search_ticket_by_date(self):
        helper = QueryHelper(self.db)

        ticket = helper.search_by_date(505)[0]

        assert ticket
        assert ticket.category == 1
        assert ticket.id
        assert ticket.date == 505
        assert ticket.price_id == 2
        assert ticket.quantity == 1
        assert ticket.section == 'C1'
        assert ticket.row == ''
        assert ticket.seat == ''
        assert ticket.wish_dates == list()
        assert ticket.wish_price_ids == list()
        assert ticket.wish_quantities == list()
        assert ticket.source_id == 1
        assert ticket.remarks == ''
        assert ticket.status == 1
        assert ticket.username == 'test_account_1'
        assert ticket.user_id == 8081

    def test_search_ticket_by_section(self):
        helper = QueryHelper(self.db)
        ticket = helper.search_by_section('C1')[0]

        assert ticket
        assert ticket.category == 1
        assert ticket.id
        assert ticket.date == 505
        assert ticket.price_id == 2
        assert ticket.quantity == 1
        assert ticket.section == 'C1'
        assert ticket.row == ''
        assert ticket.seat == ''
        assert ticket.wish_dates == list()
        assert ticket.wish_price_ids == list()
        assert ticket.wish_quantities == list()
        assert ticket.source_id == 1
        assert ticket.remarks == ''
        assert ticket.status == 1
        assert ticket.username == 'test_account_1'
        assert ticket.user_id == 8081

    def test_search_ticket_by_query(self):
        helper = QueryHelper(self.db)

        ticket = helper.search_by_query(Query(category_id=1).to_obj(dict(prices=[2])))[0]
        print(ticket.to_dict())
        assert ticket
        assert ticket.category == 1
        assert ticket.id
        assert ticket.date == 505
        assert ticket.price_id == 2
        assert ticket.quantity == 1
        assert ticket.section == 'C1'
        assert ticket.row == ''
        assert ticket.seat == ''
        assert ticket.wish_dates == list()
        assert ticket.wish_price_ids == list()
        assert ticket.wish_quantities == list()
        assert ticket.source_id == 1
        assert ticket.remarks == ''
        assert ticket.status == 1
        assert ticket.username == 'test_account_1'
        assert ticket.user_id == 8081

    def test_search_ticket_by_user_id(self):
        helper = QueryHelper(self.db)
        ticket = helper.search_by_user_id(8082)[0]
        assert ticket
        assert ticket.category == 2
        assert ticket.id
        assert ticket.date == 504
        assert ticket.price_id == 1
        assert ticket.quantity == 1
        assert ticket.section == 'A1'
        assert ticket.row == ''
        assert ticket.seat == ''
        assert ticket.wish_dates == [504, 505]
        assert ticket.wish_price_ids == [1, 2]
        assert ticket.wish_quantities == [1]
        assert ticket.source_id == 1
        assert ticket.remarks == ''
        assert ticket.status == 1
        assert ticket.username == 'test_account_2'
        assert ticket.user_id == 8082

    def test_search_ticket_by_ticket_id(self):
        helper = QueryHelper(self.db)
        ticket = helper.search_by_user_id(8082)[0]
        assert ticket
        assert ticket.category == 2
        assert ticket.id
        assert ticket.date == 504
        assert ticket.price_id == 1
        assert ticket.quantity == 1
        assert ticket.section == 'A1'
        assert ticket.row == ''
        assert ticket.seat == ''
        assert ticket.wish_dates == [504, 505]
        assert ticket.wish_price_ids == [1, 2]
        assert ticket.wish_quantities == [1]
        assert ticket.source_id == 1
        assert ticket.remarks == ''
        assert ticket.status == 1
        assert ticket.username == 'test_account_2'
        assert ticket.user_id == 8082
