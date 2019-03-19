import pytest
from mayday import Config
from mayday.controllers import MongoController


TICKET_1 = dict(
    category=1,
    ticket_id='',
    date=506,
    price=2,
    quantity=1,
    section='C1',
    row='',
    seat='',
    wish_dates=list(),
    wish_prices=list(),
    wish_quantities=list(),
    source=1,
    remarks='',
    status=1,
    username='test_account_2',
    user_id=8081,
)

TICKET_2 = dict(
    category=2,
    ticket_id='',
    date=504,
    price=1,
    quantity=1,
    section='A1',
    row='',
    seat='',
    wish_dates=[504, 505],
    wish_prices=[1, 2],
    wish_quantities=[1],
    source=1,
    remarks='',
    status=1,
    username='test_account_1',
    user_id=8082,
)


@pytest.fixture(scope="session", autouse=True)
def init_ticket_db():
    config = Config()
    mongo = MongoController(mongo_config=config.mongo_config)
    schema_config = config.schema_config

    # Cache - Action
    mongo.delete_all(
        db_name=schema_config['cache_db_name'],
        collection_name=schema_config['action_collection_name'],
        query=dict())

    #  Cache - Query
    mongo.delete_all(
        db_name=schema_config['cache_db_name'],
        collection_name=schema_config['query_collection_name'],
        query=dict())

    # Cache - Quick Search
    mongo.delete_all(
        db_name=schema_config['cache_db_name'],
        collection_name=schema_config['quick_search_collection_name'],
        query=dict())

    # Cache - Ticket
    mongo.delete_all(
        db_name=schema_config['cache_db_name'],
        collection_name=schema_config['ticket_collection_name'],
        query=dict())

    # Ticket - Tickets
    mongo.delete_all(
        db_name=schema_config['ticket_db_name'],
        collection_name=schema_config['ticket_collection_name'],
        query=dict())

    mongo.save(
        db_name=schema_config['ticket_db_name'],
        collection_name=schema_config['ticket_collection_name'],
        content=TICKET_1)

    mongo.save(
        db_name=schema_config['ticket_db_name'],
        collection_name=schema_config['ticket_collection_name'],
        content=TICKET_2)

    # Query - Queries
    mongo.delete_all(
        db_name=schema_config['query_db_name'],
        collection_name=schema_config['quick_search_collection_name'],
        query=dict())

    # User - Users
    mongo.delete_all(
        db_name=schema_config['user_db_name'],
        collection_name=schema_config['user_collection_name'],
        query=dict())
