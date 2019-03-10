import mayday
from mayday import Config
from mayday.controllers import MongoController
from mayday.objects import Query
from mayday.objects import Ticket


class QueryHelper:

    DB_NAME = 'cache'
    COLLECTION_NAME = 'queries'
    QUICK_SEARCH_COLLECTION_NAME = 'quick_searchs'

    def __init__(self, mongo_controller: MongoController):
        self.logger = mayday.get_default_logger('query_helper')
        if mongo_controller:
            self.mongo = mongo_controller
        else:
            self.mongo = MongoController(mongo_config=Config.mongo_config)

    # Form Query

    def update_query(self, query: Query) -> Query:
        # TODO: Do it.
        pass

    def reset_query(self, query: Query) -> bool:
        # TODO: Do it.
        pass

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
