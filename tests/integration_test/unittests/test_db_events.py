import unittest

import pytest
import sqlalchemy
from sqlalchemy import MetaData

from mayday.db.tables.events import Events

SAMPLES = [
    dict(
        name='fake event',
        type_id=1,
        description='fake support event',
        markdown_path='/tmp/something.md',
        attachment_hex='hexcode',
        attachment_type=1,
        is_deleted=0
    ),
    dict(
        name='fake deleted event',
        type_id=1,
        description='fake support event',
        markdown_path='/tmp/something.md',
        attachment_hex='hexcode',
        attachment_type=1,
        is_deleted=1
    )

]


@pytest.mark.usefixtures()
class TestCase(unittest.TestCase):

    @pytest.fixture(autouse=True, scope='function')
    def before_all(self):
        engine = sqlalchemy.create_engine('sqlite://')
        metadata = MetaData(bind=engine)
        self.db = Events(engine, metadata)

        # Create Table
        self.db.metadata.drop_all()
        self.db.metadata.create_all()
        self.db.role = 'writer'

        for sample in SAMPLES:
            self.db.insert(sample)

    def test_get_events(self):
        events = [x for x in self.db.get_events()]
        assert len(events) == 1
        assert events[0]['name'] == 'fake event'
