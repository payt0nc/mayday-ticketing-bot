import unittest

import pytest
import sqlalchemy
from sqlalchemy import MetaData

from mayday.db.tables.tickets import Tickets
from mayday.objects.ticket import Ticket

SAMPLES = [
    dict(
        id=1,
        category=2,
        date=512,
        price_id=4,
        quantity=2,
        section='',
        row='',
        status=1,
        remarks='test',
        wish_dates=[503, 504, 505, 510, 511, 512],
        wish_price_ids=[1, 2, 3, 4, 5],
        wish_quantities=[1, 2],
        user_id=123456789,
        username='test',
    )
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
        assert result
        assert result['id'] == SAMPLES[0]['id']
        assert result['category'] == SAMPLES[0]['category']
        assert result['date'] == SAMPLES[0]['date']
        assert result['price_id'] == SAMPLES[0]['price_id']
        assert result['quantity'] == SAMPLES[0]['quantity']
        assert result['section'] == SAMPLES[0]['section']
        assert result['row'] == SAMPLES[0]['row']
        assert result['status'] == SAMPLES[0]['status']
        assert result['wish_dates'] == SAMPLES[0]['wish_dates']
        assert result['wish_price_ids'] == SAMPLES[0]['wish_price_ids']
        assert result['wish_quantities'] == SAMPLES[0]['wish_quantities']
        assert result['user_id'] == SAMPLES[0]['user_id']
        assert result['username'] == SAMPLES[0]['username']
        assert result['remarks'] == SAMPLES[0]['remarks']

    def test_get_tickets_by_user_id(self):
        result = self.db.get_tickets_by_user_id(user_id=123456789).__next__()
        assert result
        assert result['id'] == SAMPLES[0]['id']
        assert result['category'] == SAMPLES[0]['category']
        assert result['date'] == SAMPLES[0]['date']
        assert result['price_id'] == SAMPLES[0]['price_id']
        assert result['quantity'] == SAMPLES[0]['quantity']
        assert result['section'] == SAMPLES[0]['section']
        assert result['row'] == SAMPLES[0]['row']
        assert result['status'] == SAMPLES[0]['status']
        assert result['wish_dates'] == SAMPLES[0]['wish_dates']
        assert result['wish_price_ids'] == SAMPLES[0]['wish_price_ids']
        assert result['wish_quantities'] == SAMPLES[0]['wish_quantities']
        assert result['user_id'] == SAMPLES[0]['user_id']
        assert result['username'] == SAMPLES[0]['username']
        assert result['remarks'] == SAMPLES[0]['remarks']
