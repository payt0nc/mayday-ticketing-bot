import mayday
from mayday import Config
from mayday.controllers import MongoController
from mayday.objects import User


class AuthHelper:

    config = Config().schema_config

    DB_NAME = config['user_db_name']
    COLLECTION_NAME = config['user_collection_name']

    def __init__(self, mongo_controller: MongoController):
        self.logger = mayday.get_default_logger('auth_helper')
        if mongo_controller:
            self.mongo = mongo_controller
        else:
            self.mongo = MongoController(mongo_config=Config().mongo_config)

    def _create_new_profile(self, user: User) -> dict:
        profile = user.to_dict()
        profile.update(dict(is_admin=False, is_blacklist=False))
        return self.mongo.save(db_name=self.DB_NAME, collection_name=self.COLLECTION_NAME, content=profile)

    def auth(self, user: User) -> dict:
        profile = self.mongo.load(db_name=self.DB_NAME, collection_name=self.COLLECTION_NAME,
                                  query=dict(user_id=user.user_id))
        self.logger.debug(profile)
        if profile:
            return profile[0]
        return self._create_new_profile(user)
