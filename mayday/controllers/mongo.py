from bson.objectid import ObjectId
from pymongo import DESCENDING, MongoClient

import mayday


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

    def delete_one(self, db_name: str, collection_name: str, object_id: str) -> bool:
        collection = self.client[db_name][collection_name]
        self.logger.info(object_id)
        return bool(collection.delete_one({'_id': ObjectId(object_id)}))

    def delete_all(self, db_name: str, collection_name: str, query: dict) -> bool:
        collection = self.client[db_name][collection_name]
        self.logger.info(query)
        return bool(collection.delete_many(query))

    def save(self, db_name: str, collection_name: str, content: dict) -> dict:
        collection = self.client[db_name][collection_name]
        self.logger.debug(content)
        object_id = collection.insert_one(content).inserted_id
        return collection.find_one({'_id': ObjectId(object_id)})

    def load(self, db_name: str, collection_name: str, query: dict) -> list:
        collection = self.client[db_name][collection_name]
        self.logger.debug(query)
        return [x for x in collection.find(query).sort('updated_at', DESCENDING)]

    def upsert(self, db_name: str, collection_name: str, conditions: dict, update_part: dict) -> None:
        collection = self.client[db_name][collection_name]
        self.logger.debug(conditions)
        self.logger.debug(update_part)
        collection.update_one(filter=conditions, update={'$set': update_part}, upsert=True)
