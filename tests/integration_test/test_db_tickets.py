import pytest

from mayday.objects.query import Query
from mayday.objects.ticket import Ticket

SAMPLES = [
    Ticket().to_obj(dict(
        id=10,
        category=2,
        date=512,
        price_id=4,
        quantity=2,
        section='',
        row='',
        status=1,
        source=1,
        remarks='test',
        wish_dates=[503, 504, 505, 510, 511, 512],
        wish_price_ids=[1, 2, 3, 4, 5],
        wish_quantities=[1, 2],
        user_id=123456789,
        username='test'))
]


@pytest.mark.usefixtures('database')
class Test:

    @pytest.fixture(autouse=True)
    def before_all(self, database: dict):
        self.db = database['ticket_table']
        self.db.raw_insert(SAMPLES[0].to_dict())

    def test_get_tickets_by_user_id(self):
        results = self.db.get_tickets_by_user_id(user_id=123456789)

        assert results
        result = results.__next__()
        ticket = SAMPLES[0]
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

    def test_get_tickets_by_ticket_id(self):
        result = self.db.get_ticket_by_ticket_id(ticket_id=10)
        assert result
        ticket = SAMPLES[0]
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

    def test_get_ticket_by_conditions(self):
        query = Query(category_id=2, user_id=123456789, username='test')
        query.update_field('prices', 4)
        results = self.db.get_tickets_by_conditions(query.to_dict())

        result = results.__next__()
        assert result

        ticket = SAMPLES[0]
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
