
import mayday
from mayday import Config
from mayday.controllers import RedisController
from mayday.objects import Query, Ticket


class ActionHelper:

    def __init__(self, redis_controller: RedisController):
        self.logger = mayday.get_default_logger('action_helper')
        if redis_controller:
            self.redis = redis_controller
        else:
            config = Config().redis_config
            self.redis = RedisController(redis_db=config['dbs'].index('actions'), redis_config=config)

    # Last Choice

    def load_last_choice(self, user_id: int) -> dict:
        result = self.redis.load(user_id=user_id, action='last_choice')
        self.logger.debug(dict(user_id=user_id, result=result))
        return result

    def save_last_choice(self, user_id: int, field=None) -> bool:
        self.logger.debug(dict(user_id=user_id, action='last_choice', content=dict(field=field)))
        return self.redis.save(user_id=user_id, action='last_choice', content=dict(field=field))

    # Ticket

    def load_drafting_ticket(self, user_id: int) -> Ticket:
        result = self.redis.load(user_id=user_id, action='ticket')
        self.logger.debug(result)
        return Ticket(user_id=user_id).to_obj(result)

    def save_drafting_ticket(self, user_id: int, ticket: Ticket) -> bool:
        self.logger.debug(ticket.to_dict())
        return self.redis.save(user_id=user_id, action='ticket', content=ticket.to_dict())

    def reset_drafting_ticket(self, user_id: int, username: str) -> Ticket:
        self.redis.clean(user_id=user_id, action='ticket')
        self.redis.save(user_id=user_id, action='ticket', content=Ticket(user_id=user_id, username=username).to_dict())
        ticket = self.redis.load(user_id=user_id, action='ticket')
        return Ticket(user_id=user_id, username=username).to_obj(ticket)

    # Query

    def load_drafting_query(self, user_id: int) -> Query:
        result = self.redis.load(user_id=user_id, action='query')
        self.logger.debug(result)
        return Query(category_id=-1, user_id=user_id).to_obj(result)

    def save_drafting_query(self, user_id: int, query: Query) -> bool:
        self.logger.debug(query.to_dict())
        return self.redis.save(user_id=user_id, action='query', content=query.to_dict())

    def reset_drafting_query(self, user_id: int, username: str, category: int) -> Ticket:
        self.redis.clean(user_id=user_id, action='query')
        self.redis.save(user_id=user_id, action='query',
                        content=Query(category_id=category, user_id=user_id, username=username).to_dict())
        query = self.redis.load(user_id=user_id, action='query')
        return Query(category_id=-1, user_id=user_id, username=username).to_obj(query)
