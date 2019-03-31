import pytest

from mayday.objects.query import Query
from mayday.objects.ticket import Ticket
from .conftest import TICKET_1


@pytest.mark.usefixtures('database')
class Test:

    @pytest.fixture(autouse=True)
    def before_all(self, database: dict):
        self.db = database['ticket_table']

    def test_get_tickets_by_user_id(self):
        results = self.db.get_tickets_by_user_id(user_id=8081)

        assert results
        result = results[0]
        ticket = Ticket().to_obj(TICKET_1)
        assert result
        assert result.id
        assert result.category == ticket.category
        assert result.date == ticket.date
        assert result.price_id == ticket.price_id
        assert result.quantity == ticket.quantity
        assert result.section == ticket.section
        assert result.row == ticket.row
        assert result.status == ticket.status
        assert result.wish_dates == ticket.wish_dates
        assert result.wish_price_ids == ticket.wish_price_ids
        assert result.wish_quantities == ticket.wish_quantities
        assert result.user_id == ticket.user_id
        assert result.username == ticket.username
        assert result.remarks == ticket.remarks

    def test_get_ticket_by_conditions(self):
        query = Query(category_id=1, user_id=8081, username='test_account_1')
        query.update_field('prices', 2)
        results = self.db.get_tickets_by_conditions(query.to_dict())

        result = results[0]
        assert result

        ticket = Ticket().to_obj(TICKET_1)
        assert result
        assert result.id
        assert result.category == ticket.category
        assert result.date == ticket.date
        assert result.price_id == ticket.price_id
        assert result.quantity == ticket.quantity
        assert result.section == ticket.section
        assert result.row == ticket.row
        assert result.status == ticket.status
        assert result.wish_dates == ticket.wish_dates
        assert result.wish_price_ids == ticket.wish_price_ids
        assert result.wish_quantities == ticket.wish_quantities
        assert result.user_id == ticket.user_id
        assert result.username == ticket.username
        assert result.remarks == ticket.remarks

    '''
    def test_get_tickets_by_ticket_id(self):
        result = self.db.get_ticket_by_ticket_id(ticket_id=10)
        assert result
        ticket = TICKET_1
        assert result
        assert result.id == ticket.id
        assert result.category == ticket.category
        assert result.date == ticket.date
        assert result.price_id == ticket.price_id
        assert result.quantity == ticket.quantity
        assert result.section == ticket.section
        assert result.row == ticket.row
        assert result.status == ticket.status
        assert result.wish_dates == ticket.wish_dates
        assert result.wish_price_ids == ticket.wish_price_ids
        assert result.wish_quantities == ticket.wish_quantities
        assert result.user_id == ticket.user_id
        assert result.username == ticket.username
        assert result.remarks == ticket.remarks
    '''
