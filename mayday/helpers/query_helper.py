import mayday
from mayday import Config
from mayday.controllers import MongoController
from mayday.objects import Query, Ticket


class QueryHelper:

    config = Config().schema_config

    QUICK_SEARCH_QUERY_DB_NAME = config['query_db_name']
    QUICK_SEARCH_COLLECTION_NAME = config['quick_search_collection_name']

    TICKET_DB_NAME = config['ticket_db_name']
    TICKET_COLLECTION_NAME = config['ticket_collection_name']

    EVENT_DB_NAME = config['event_db_name']
    EVENT_COLLECTION_NAME = config['event_collection_name']

    def __init__(self, mongo_controller: MongoController):
        self.logger = mayday.get_default_logger('query_helper')
        if mongo_controller:
            self.mongo = mongo_controller
        else:
            self.mongo = MongoController(mongo_config=Config.mongo_config)

    # Quick Search
    def save_quick_search(self, query: Query) -> bool:
        self.logger.debug(query.to_dict())
        return bool(self.mongo.save(db_name=self.QUICK_SEARCH_QUERY_DB_NAME, collection_name=self.QUICK_SEARCH_COLLECTION_NAME, content=query.to_dict()))

    def load_quick_search(self, user_id: int) -> Query:
        queries = self.mongo.load(
            db_name=self.QUICK_SEARCH_QUERY_DB_NAME, collection_name=self.QUICK_SEARCH_COLLECTION_NAME, query=dict(user_id=user_id))
        self.logger.debug(queries)
        if queries:
            return Query(user_id=user_id, category_id=queries[0]['category']).to_obj(queries[0])

    def update_quick_search(self, query: Query) -> bool:
        self.logger.debug(query.to_dict())
        return bool(self.mongo.update(
            db_name=self.QUICK_SEARCH_QUERY_DB_NAME,
            collection_name=self.QUICK_SEARCH_COLLECTION_NAME,
            conditions=dict(user_id=query.user_id, username=query.username),
            update_part=query.to_dict()))

    # Search Ticket
    def search_by_section(self, section: str) -> list:
        results = self.mongo.load(
            db_name=self.TICKET_DB_NAME, collection_name=self.TICKET_COLLECTION_NAME, query=dict(section=section))
        self.logger.debug(results)
        return results

    def search_by_date(self, ticket_date: int) -> list:
        results = self.mongo.load(
            db_name=self.TICKET_DB_NAME, collection_name=self.TICKET_COLLECTION_NAME, query=dict(date={'$in': [ticket_date]}))
        self.logger.debug(results)
        return results

    def search_by_user_id(self, user_id: int) -> list:
        results = self.mongo.load(
            db_name=self.TICKET_DB_NAME, collection_name=self.TICKET_COLLECTION_NAME, query=dict(user_id=user_id))
        self.logger.debug(results)
        return [Ticket().to_obj(ticket) for ticket in results]

    def search_by_ticket_id(self, ticket_id: str) -> Ticket:
        results = self.mongo.load(
            db_name=self.TICKET_DB_NAME, collection_name=self.TICKET_COLLECTION_NAME, query=dict(ticket_id=ticket_id))
        self.logger.debug(results)
        return Ticket().to_obj(results[0])

    def search_by_query(self, query: Query) -> list:
        self.logger.info(query.to_dict())
        results = self.mongo.load(
            db_name=self.TICKET_DB_NAME, collection_name=self.TICKET_COLLECTION_NAME, query=query.to_mongo_syntax())
        self.logger.debug(results)
        return [Ticket().to_obj(ticket) for ticket in results]

    # Events
    def list_all_events(self) -> list:
        return self.mongo.load(db_name=self.EVENT_DB_NAME, collection_name=self.EVENT_COLLECTION_NAME, query=dict())

    # Util

    @staticmethod
    def split_tickets_traits(tickets: list, size: int = 5) -> list:
        trait = [ticket.to_human_readable() for ticket in tickets]
        return [trait[i: i+size] for i in range(0, len(trait), size)]
