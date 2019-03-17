import mayday
from mayday import Config
from mayday.controllers import MongoController
from mayday.objects import Query, Ticket, User


class ActionHelper:

    config = Config().schema_config
    DB_NAME = config['cache_db_name']
    COLLECTION_NAME = config['action_collection_name']

    def __init__(self, mongo_controller: MongoController):
        self.logger = mayday.get_default_logger('action_helper')
        if mongo_controller:
            self.mongo = mongo_controller
        else:
            self.mongo = MongoController(mongo_config=Config.mongo_config)

    def load_last_action(self, user: User) -> dict:
        pass

    def save_current_action(self, user: User) -> dict:
        pass

    def reset_current_action(self, user: User) -> dict:
        pass

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
