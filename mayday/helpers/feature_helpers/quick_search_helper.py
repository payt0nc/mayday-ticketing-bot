import mayday
from mayday import MONGO_CONTROLLER
from mayday.helpers import FeatureHelper, QueryHelper
from mayday.objects import Query

logger = mayday.get_default_logger('search_helper')
query_helper = QueryHelper(MONGO_CONTROLLER)


class QuickSearchHelper(FeatureHelper):

    def match_my_tickets(self, user_id: int) -> list:
        query = Query(category_id=2, user_id=user_id)
        for ticket in query_helper.search_by_user_id(user_id):
            if ticket.category == 2:
                query.update_field('date', ticket.wish_dates)
                query.update_field('price', ticket.wish_prices)
                query.update_field('quantity', ticket.wish_quantities)
        self.save_drafting_query(user_id, query)
        return query_helper.search_by_query(query)

    @staticmethod
    def split_tickets_traits(tickets: list) -> list:
        return query_helper.split_tickets_traits(tickets)
