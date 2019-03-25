import mayday
from mayday.helpers import FeatureHelper
from mayday.objects import Query

logger = mayday.get_default_logger('search_helper')


class SearchHelper(FeatureHelper):

    def update_cache(self, user_id: int, value: (str, int)) -> Query:
        query = self.load_drafting_query(user_id)
        last_choice = self.load_last_choice(user_id)
        self.logger.debug(last_choice)
        query.update_field(last_choice, value)
        self.save_drafting_query(user_id, query)
        return query

    def reset_cache(self, user_id: int) -> Query:
        query = Query(category_id=1, user_id=user_id)
        self.save_drafting_query(user_id, query)
        return self.load_drafting_query(user_id)
