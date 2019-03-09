from mayday.controllers.redis import RedisHelper
from mayday.controllers.request import RequestHelper
from mayday.objects import Query, Ticket


class CacheHelper:

    DB_NAME = 'cache'
    COLLECTION_NAME = 'actions'

    def __init__(self, feature: str, redis_helper: RedisHelper, request_helper: RequestHelper):
        self._feature = feature
        self._last_choice = '{}_last_choice'.format(feature)
        self.redis = redis_helper
        self.request_helper = request_helper

    def init(self, user_id: int, username: username, category_id: int):
        self.reset(user_id, username, category_id)
        return self.get(user_id=user_id, username=username)

    def reset(self, user_id: int, username: str, category_id: int) -> dict:
        if self._feature == 'search_ticket':
            content = Query(user_id=user_id, username=username, category_id=category_id).to_dict()
            self.set(user_id, content)
        elif self._feature == 'post_ticket':
            content = Ticket(user_id=user_id, username=username).to_dict()
            self.set(user_id, content)
        elif self._feature == 'update_ticket':
            ticket_id = self.get(user_id=user_id, username=username).get('id')
            content = self.request_helper.get_ticket_by_ticket_id(ticket_id=ticket_id).get('info')
            self.set(user_id=user_id, content=content)
        return content

    def get(self, user_id: int, username: str) -> dict:
        result = self.redis.load(dict(user_id=user_id, action=self._feature))
        return result.value if result else self.reset(user_id=user_id, username=username)

    def set(self, user_id, content):
        redis.save(dict(
            user_id=user_id,
            action=self._feature,
            value=content
        ))

    def get_last_choice(self, user_id):
        return redis.read(dict(
            user_id=user_id,
            action=self._last_choice)).value

    def set_last_choice(self, user_id, content):
        redis.save(dict(
            user_id=user_id,
            action=self._last_choice,
            value=content))
