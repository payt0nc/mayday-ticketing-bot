import mayday
from bson.objectid import ObjectId
from pymongo import DESCENDING, MongoClient


class NoClientAndConfigProvided(Exception):
    pass


class MongoController:

    def __init__(self, mongo_client: MongoClient = None, mongo_config: dict = None):
        self.logger = mayday.get_default_logger(log_name='mongo_controller')
        if mongo_client:
            self.client = mongo_client
        elif mongo_config:
            self.client = MongoClient(host=mongo_config['host'], port=mongo_config.get('port', 27017))
        else:
            raise NoClientAndConfigProvided

    def count(self, db_name: str, collection_name: str, query: dict) -> int:
        collection = self.client[db_name][collection_name]
        return collection.count_documents(query)

    def delete(self, db_name: str, collection_name: str, object_id: str) -> bool:
        collection = self.client[db_name][collection_name]
        self.logger.info(object_id)
        return bool(collection.delete_one({'_id': ObjectId(object_id)}))

    def save(self, db_name: str, collection_name: str, content: dict) -> dict:
        collection = self.client[db_name][collection_name]
        self.logger.debug(content)
        object_id = collection.insert_one(content).inserted_id
        return collection.find_one({'_id': ObjectId(object_id)})

    def load(self, db_name: str, collection_name: str, query: dict) -> list:
        collection = self.client[db_name][collection_name]
        self.logger.debug(query)
        return [x for x in collection.find(query).sort('updated_at', DESCENDING)]

    def upsert(self, db_name: str, collection_name: str, content: dict, replace_condition: dict) -> bool:
        collection = self.client[db_name][collection_name]
        self.logger.debug(content)
        return bool(collection.replace_one(filter=replace_condition, replacement=content, upsert=True).modified_count)
