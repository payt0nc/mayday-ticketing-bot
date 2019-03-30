import unittest

import pytest
import sqlalchemy
from sqlalchemy import MetaData

from mayday.db.tables.tickets import Tickets

SAMPLES = [
    dict(
        id=1,
        category_id=2,
        date=512,
        price_id=4,
        quantity=2,
        section='',
        row='',
        status_id=1,
        wish_date=[504, 505, 506, 511, 512, 513],
        wish_price_id=[1, 2, 3, 4, 5],
        wish_quantity=[1, 2],
        user_id=123456789,
        username='test',
        remarks='test'
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
        assert result['category_id'] == SAMPLES[0]['category_id']
        assert result['date'] == SAMPLES[0]['date']
        assert result['price_id'] == SAMPLES[0]['price_id']
        assert result['quantity'] == SAMPLES[0]['quantity']
        assert result['section'] == SAMPLES[0]['section']
        assert result['row'] == SAMPLES[0]['row']
        assert result['status_id'] == SAMPLES[0]['status_id']
        assert result['wish_date'] == SAMPLES[0]['wish_date']
        assert result['wish_price_id'] == SAMPLES[0]['wish_price_id']
        assert result['wish_quantity'] == SAMPLES[0]['wish_quantity']
        assert result['user_id'] == SAMPLES[0]['user_id']
        assert result['username'] == SAMPLES[0]['username']
        assert result['remarks'] == SAMPLES[0]['remarks']

    def test_get_tickets_by_user_id(self):
        result = self.db.get_tickets_by_user_id(user_id=123456789).__next__()
        assert result
        assert result['id'] == SAMPLES[0]['id']
        assert result['category_id'] == SAMPLES[0]['category_id']
        assert result['date'] == SAMPLES[0]['date']
        assert result['price_id'] == SAMPLES[0]['price_id']
        assert result['quantity'] == SAMPLES[0]['quantity']
        assert result['section'] == SAMPLES[0]['section']
        assert result['row'] == SAMPLES[0]['row']
        assert result['status_id'] == SAMPLES[0]['status_id']
        assert result['wish_date'] == SAMPLES[0]['wish_date']
        assert result['wish_price_id'] == SAMPLES[0]['wish_price_id']
        assert result['wish_quantity'] == SAMPLES[0]['wish_quantity']
        assert result['user_id'] == SAMPLES[0]['user_id']
        assert result['username'] == SAMPLES[0]['username']
        assert result['remarks'] == SAMPLES[0]['remarks']
