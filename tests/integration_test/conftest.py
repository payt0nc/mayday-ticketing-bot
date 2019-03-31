import pytest
import time
from mayday import engine, metadata
from mayday.db.tables.tickets import TicketsModel
from mayday.db.tables.users import UsersModel
from mayday.db.tables.events import EventsModel


TICKET_1 = dict(
    category=1,
    date=505,
    price_id=2,
    quantity=1,
    section='C1',
    row='',
    seat='',
    wish_dates=list(),
    wish_price_ids=list(),
    wish_quantities=list(),
    source_id=1,
    remarks='',
    status=1,
    username='test_account_1',
    user_id=8081,
    created_at=int(time.time()))

TICKET_2 = dict(
    category=2,
    date=504,
    price_id=1,
    quantity=1,
    section='A1',
    row='',
    seat='',
    wish_dates=[504, 505],
    wish_price_ids=[1, 2],
    wish_quantities=[1],
    source_id=1,
    remarks='',
    status=1,
    username='test_account_2',
    user_id=8082,
    created_at=int(time.time()))


@pytest.fixture
def database():
    # Create User Table
    event_table = EventsModel(engine, metadata, role='writer')
    event_table.metadata.drop_all()
    event_table.metadata.create_all()

    # Create User Table
    user_table = UsersModel(engine, metadata, role='writer')
    user_table.metadata.drop_all()
    user_table.metadata.create_all()

    # Create Ticket Table
    ticket_table = TicketsModel(engine, metadata, role='writer')
    ticket_table.metadata.drop_all()
    ticket_table.metadata.create_all()

    ticket_table.raw_upsert(TICKET_1)
    ticket_table.raw_upsert(TICKET_2)

    return dict(ticket_table=ticket_table, user_table=user_table)
