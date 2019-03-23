import mayday
from mayday import Config
from mayday.controllers import MongoController
from mayday.objects import Query


class QueryHelper:

    config = Config().schema_config

    QUICK_SEARCH_QUERY_DB_NAME = config['query_db_name']
    QUICK_SEARCH_COLLECTION_NAME = config['quick_search_collection_name']

    TICKET_DB_NAME = config['ticket_db_name']
    TICKET_COLLECTION_NAME = config['ticket_collection_name']

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

    def load_quick_search(self, user_id: int, username: str) -> Query:
        query = self.mongo.load(
            db_name=self.QUICK_SEARCH_QUERY_DB_NAME, collection_name=self.QUICK_SEARCH_COLLECTION_NAME, query=dict(user_id=user_id, username=username))[0]
        self.logger.debug(query)
        return Query(user_id=user_id, username=username, category_id=query['category']).to_obj(query)

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

    def search_by_query(self, query: Query) -> list:
        self.logger.info(query.to_dict())
        results = self.mongo.load(
            db_name=self.TICKET_DB_NAME, collection_name=self.TICKET_COLLECTION_NAME, query=query.to_mongo_syntax())
        self.logger.debug(results)
        return results

    # Util

    @staticmethod
    def split_tickets_traits(tickets: list, size: int = 5) -> list:
        trait = [ticket.to_human_readable() for ticket in tickets]
        if len(trait) <= size:
            return [trait]
        return [trait[i: i+size] for i in range(0, len(trait), size)]
