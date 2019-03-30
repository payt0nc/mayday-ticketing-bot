import unittest

import pytest
import sqlalchemy
from sqlalchemy import MetaData

from mayday.db.tables.tickets import Tickets
from mayday.objects.ticket import Ticket

SAMPLES = [Ticket().to_obj(dict(
    id=1,
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


@pytest.mark.usefixtures()
class TestCase(unittest.TestCase):

    @pytest.fixture(autouse=True, scope='function')
    def before_all(self):
        engine = sqlalchemy.create_engine('sqlite://')
        metadata = MetaData(bind=engine)
        self.db = Tickets(engine, metadata)

        # Create Table
        self.db.metadata.drop_all()
        self.db.metadata.create_all()
        self.db.role = 'writer'

        for sample in SAMPLES:
            self.db.create_ticket(sample)

    def test_get_tickets_by_ticket_id(self):
        result = self.db.get_ticket_by_ticket_id(ticket_id=1)
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

    def test_get_tickets_by_user_id(self):
        result = self.db.get_tickets_by_user_id(user_id=123456789).__next__()
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
