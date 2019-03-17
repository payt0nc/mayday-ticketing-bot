import mayday
from mayday import Config
from mayday.controllers import MongoController
from mayday.objects import Query


class QueryHelper:

    config = Config().schema_config

    CACHE_DB_NAME = config['cache_db_name']
    CACHE_COLLECTION_NAME = config['query_collection_name']

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

    # Form Query

    def create_blank_query(self, query: Query) -> Query:
        self.logger.debug(query.to_dict())
        new_query = self.mongo.save(
            db_name=self.CACHE_DB_NAME, collection_name=self.CACHE_COLLECTION_NAME, content=query.to_dict())
        return Query(query.user_id, query.username, query.category).to_obj(new_query)

    def load_cache_query(self, user_id: int, username: str) -> Query:
        query = self.mongo.load(
            db_name=self.CACHE_DB_NAME, collection_name=self.CACHE_COLLECTION_NAME,
            query=dict(user_id=user_id, username=username))[0]
        self.logger.debug(query)
        return Query(user_id=user_id, username=username, category_id=query['category']).to_obj(query)

    def update_cache_query(self, query: Query) -> Query:
        self.mongo.update(
            db_name=self.CACHE_DB_NAME, collection_name=self.CACHE_COLLECTION_NAME,
            conditions=dict(user_id=query.user_id, username=query.username), update_part=query.to_dict(), upsert=True)
        cached_query = self.mongo.load(
            db_name=self.CACHE_DB_NAME, collection_name=self.CACHE_COLLECTION_NAME, query=dict(user_id=query.user_id, username=query.username))
        self.logger.debug(cached_query)
        return Query(user_id=query.user_id, username=query.username, category_id=query.category).to_obj(cached_query[0])

    def reset_cache_query(self, query: Query) -> bool:
        self.logger.debug(query.to_dict())
        querys = self.mongo.load(
            db_name=self.CACHE_DB_NAME, collection_name=self.CACHE_COLLECTION_NAME,
            query=dict(user_id=query.user_id))
        if querys:
            result = self.mongo.delete_all(
                db_name=self.CACHE_DB_NAME, collection_name=self.CACHE_COLLECTION_NAME, query=dict(user_id=query.user_id))
            if result is False:
                self.logger.warning(dict(info='Cant delete query', query=query.to_dict()))
        return self.create_blank_query(Query(user_id=query.user_id, username=query.username, category_id=query.category))

    # Custom Quick Search

    def save_quick_search(self, query: Query) -> bool:
        self.logger.debug(query.to_dict())
        return bool(self.mongo.save(
            db_name=self.QUICK_SEARCH_QUERY_DB_NAME, collection_name=self.QUICK_SEARCH_COLLECTION_NAME, content=query.to_dict()))

    def load_quick_search(self, user_id: int, username: str) -> Query:
        query = self.mongo.load(
            db_name=self.QUICK_SEARCH_QUERY_DB_NAME, collection_name=self.QUICK_SEARCH_COLLECTION_NAME,
            query=dict(user_id=user_id, username=username))[0]
        self.logger.debug(query)
        return Query(user_id=user_id, username=username, category_id=query['category']).to_obj(query)

    def update_quick_search(self, query: Query) -> Query:
        # TODO: Do it.
        pass

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
