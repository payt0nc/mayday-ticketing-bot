import unittest

import pytest
import sqlalchemy
from sqlalchemy import MetaData

from mayday.db.tables.tickets import TicketsModel
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
        self.db = TicketsModel(engine, metadata)

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
        result = self.db.get_tickets_by_user_id(user_id=123456789)[0]
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

    def test_update_ticket(self):
        updated_ticket = SAMPLES[0].update_field('status', 3)
        result = self.db.update_ticket(updated_ticket)
        assert result
        ticket_in_db = self.db.get_tickets_by_user_id(user_id=123456789)[0]
        assert ticket_in_db.status == updated_ticket.status

    def test_transform_ticket_stats(self):
        sample = dict(
            status_distribution=[
                dict(status=1, amount=2),
                dict(status=2, amount=1),
            ],
            ticket_distribution=[
                dict(category=1, date=503, price_id=1, amount=1),
                dict(category=1, date=503, price_id=2, amount=2),
                dict(category=1, date=503, price_id=3, amount=3),
                dict(category=1, date=504, price_id=1, amount=3),
                dict(category=1, date=504, price_id=2, amount=2),
                dict(category=1, date=504, price_id=3, amount=1),
                dict(category=1, date=505, price_id=1, amount=1),

                dict(category=2, date=503, price_id=1, amount=1),
                dict(category=2, date=503, price_id=2, amount=2),
            ],
            updated_at=0)

        expected = dict(
            status_distribution={1: 2, 2: 1},
            ticket_distribution={
                # category -> price_id -> date -> amount
                1: {
                    1: {503: 1, 504: 3, 505: 1},
                    2: {503: 2, 504: 2},
                    3: {503: 3, 504: 1}
                },
                2: {
                    1: {503: 1},
                    2: {503: 2}
                }
            },
            updated_at=0)

        assert self.db.transform_tickets_stats(sample) == expected
