import logging

import mayday
from mayday.constants.replykeyboards import KEYBOARDS
from mayday.controllers.redis import RedisController
from mayday.objects.query import Query
from mayday.objects.ticket import Ticket


logger = logging.getLogger()
logger.setLevel(mayday.get_log_level())
logger.addHandler(mayday.console_handler())


class FeatureHelper:

    def __init__(self, feature: str, redis_controller: RedisController = None):

        self._feature = feature
        if redis_controller:
            self.redis = redis_controller
        else:
            self.redis = RedisController()

    # Feature Cache
    def load_cache(self, user_id: int):
        result = self.redis.load(user_id=user_id, action='{}_cache'.format(self._feature))
        logger.debug(dict(user_id=user_id, result=result))
        return result['field']

    def save_cache(self, user_id: int, field=None) -> bool:
        logger.debug(dict(user_id=user_id, action='{}_cache'.format(self._feature), content=dict(field=field)))
        return self.redis.save(user_id=user_id, action='{}_cache'.format(self._feature), content=dict(field=field))

    def reset_cache(self, user_id: int, username: str):
        raise NotImplementedError

    def update_cache(self, user_id: int, value: (str, int)):
        raise NotImplementedError

    # Last Choice
    def load_last_choice(self, user_id: int) -> str:
        result = self.redis.load(user_id=user_id, action='{}_last_choice'.format(self._feature))
        logger.debug(dict(user_id=user_id, result=result))
        return result['field']

    def save_last_choice(self, user_id: int, field=None) -> bool:
        if field in {'reset', 'check'} | set(KEYBOARDS.conditions_keyboard_mapping.keys()):
            logger.debug(dict(user_id=user_id, action='{}_last_choice'.format(self._feature), content=dict(field=field)))
            return self.redis.save(user_id=user_id, action='{}_last_choice'.format(self._feature), content=dict(field=field))
        return False

    # Ticket
    def load_posting_ticket_category(self, user_id: int) -> int:
        return self.redis.load(user_id=user_id, action='ticket_category')['category']

    def save_posting_ticket_cateogry(self, user_id: int, category: int) -> bool:
        return self.redis.save(user_id=user_id, action='ticket_category', content=dict(category=category))

    def load_drafting_ticket(self, user_id: int) -> Ticket:
        result = self.redis.load(user_id=user_id, action='ticket')
        logger.debug(result)
        return Ticket(user_id=user_id).to_obj(result)

    def save_drafting_ticket(self, user_id: int, ticket: Ticket) -> bool:
        logger.debug(ticket.to_dict())
        return self.redis.save(user_id=user_id, action='ticket', content=ticket.to_dict())

    def reset_drafting_ticket(self, user_id: int, username: str) -> Ticket:
        self.redis.clean(user_id=user_id, action='ticket')
        self.redis.save(user_id=user_id, action='ticket', content=Ticket(user_id=user_id, username=username).to_dict())
        ticket = self.redis.load(user_id=user_id, action='ticket')
        return Ticket(user_id=user_id, username=username).to_obj(ticket)

    # Query
    def load_drafting_query(self, user_id: int) -> Query:
        result = self.redis.load(user_id=user_id, action='query')
        logger.debug(result)
        return Query(category_id=-1, user_id=user_id).to_obj(result)

    def save_drafting_query(self, user_id: int, query: Query) -> bool:
        logger.debug(query.to_dict())
        return self.redis.save(user_id=user_id, action='query', content=query.to_dict())

    def reset_drafting_query(self, user_id: int, username: str, category: int) -> Ticket:
        self.redis.clean(user_id=user_id, action='query')
        self.redis.save(user_id=user_id, action='query',
                        content=Query(category_id=category, user_id=user_id, username=username).to_dict())
        query = self.redis.load(user_id=user_id, action='query')
        return Query(category_id=-1, user_id=user_id, username=username).to_obj(query)

    # Util
    def tickets_tostr(self, tickets: list, string_template: str) -> str:
        results = []
        for ticket in tickets:
            logger.debug(type(ticket))
            logger.debug(ticket)
            logger.debug(type(string_template))
            tmplate = string_template.format_map(ticket)
            logger.debug(tmplate)
            results.append(tmplate)
        logger.debug(results)
        return '\n'.join(results)
