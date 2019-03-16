import mayday
from mayday import Config
from mayday.controllers import MongoController
from mayday.objects import Query, Ticket


class QueryHelper:

    CACHE_DB_NAME = 'cache'
    CACHE_COLLECTION_NAME = 'queries'

    QUERY_DB_NAME = 'query'
    COLLECTION_NAME = 'quick_searches'

    def __init__(self, mongo_controller: MongoController):
        self.logger = mayday.get_default_logger('query_helper')
        if mongo_controller:
            self.mongo = mongo_controller
        else:
            self.mongo = MongoController(mongo_config=Config.mongo_config)

    # Form Query

    def create_blank_query(self, query: Query) -> Query:
        cached_query = self.mongo.save(
            db_name=self.CACHE_DB_NAME, collection_name=self.CACHE_COLLECTION_NAME, content=query.to_dict())
        query = Query(
            user_id=query.user_id, username=query.username, category_id=query.category).to_obj(cached_query)
        self.logger.debug(query.to_dict())
        query_dict = self.mongo.save(
            db_name=self.CACHE_DB_NAME, collection_name=self.CACHE_COLLECTION_NAME, content=query.to_dict())
        return Query(user_id=query.user_id, username=query.username, category_id=query.category).to_obj(query_dict)

    def load_cache_ticket(self, user_id: int, username: str) -> Ticket:
        query = self.mongo.load(
            db_name=self.CACHE_DB_NAME, collection_name=self.CACHE_COLLECTION_NAME,
            query=dict(user_id=user_id, username=username)
        )[0]
        self.logger.debug(query)
        return Query(user_id=user_id, username=username, category_id=query['category']).to_obj(query)

    def update_cache_query(self, query: Query) -> Query:
        self.mongo.upsert(
            db_name=self.CACHE_DB_NAME, collection_name=self.CACHE_COLLECTION_NAME,
            filter=dict(user_id=query.user_id, username=query.username), update_part=query.to_dict())
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

    # Search Ticket

    def search_by_query(self, query: Query) -> list:
        # TODO: Do it.
        pass

    # Quick Search

    def save_quick_search(self, query: Query) -> bool:
        # TODO: Do it.
        pass

    def update_quick_search(self, query: Query) -> Query:
        # TODO: Do it.
        pass

    # TODO: Quick Search by Date

    # TODO: Quick Search by Area
