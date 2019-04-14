import mayday
<<<<<<< HEAD
=======
from mayday.config import AUTH_LOGGER as auth_logger
>>>>>>> 589487b7c59176c1e1cd4bd9d287bafb4b3f94b3
from mayday.config import EVENT_LOGGER as event_logger
from mayday.config import ROOT_LOGGER as logger
from mayday.controllers.redis import RedisController
from mayday.db.tables.tickets import TicketsModel
from mayday.objects.query import Query
from mayday.objects.ticket import Ticket


class QueryHelper:

    def __init__(self, table: TicketsModel):
        self.tickets_table = table
        self.redis = RedisController(db_name='quick_search')

    # Quick Search
    # FIXME: Implement on Redis
    def save_quick_search(self, query: Query) -> bool:
        logger.debug(query.to_dict())
        return self.redis.save(query.user_id, 'quick_search', query.to_dict())

    def load_quick_search(self, user_id: int) -> Query:
        result = self.redis.load(user_id, 'quick_search')
        logger.debug(result)
        return Query(category_id=-1).to_obj(result)

    # Search Ticket
    def search_by_section(self, section: str) -> list:
        return self.tickets_table.get_ticket_by_section(section)

    def search_by_user_id(self, user_id: int) -> list:
        return self.tickets_table.get_tickets_by_user_id(user_id)

    def search_by_ticket_id(self, ticket_id: str) -> Ticket:
        return self.tickets_table.get_ticket_by_ticket_id(ticket_id)

    def search_by_query(self, query: Query) -> list:
        return self.tickets_table.get_tickets_by_conditions(query.to_dict())

    def search_by_date(self, date: str) -> list:
        return self.tickets_table.get_tickets_by_date(date)

    # Util
    @staticmethod
    def split_tickets_traits(tickets: list, size: int = 5) -> list:
        trait = [ticket.to_human_readable() for ticket in tickets]
        return [trait[i: i+size] for i in range(0, len(trait), size)]
