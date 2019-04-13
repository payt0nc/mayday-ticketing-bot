import os

import mayday
from bson.objectid import ObjectId
from mayday.config import ROOT_LOGGER as logger
from pymongo import ASCENDING, DESCENDING, MongoClient


class MongoController:

    def __init__(self, mongo_client: MongoClient = None):
        if mongo_client:
            self.client = mongo_client
        else:
            self.client = MongoClient(
                host=os.environ.get('MONGO_HOST', 'localhost'),
                port=os.environ.get('MONGO_PORT', 27017))

    def count(self, db_name: str, collection_name: str, query: dict) -> int:
        collection = self.client[db_name][collection_name]
        return collection.count_documents(query)

    def delete_one(self, db_name: str, collection_name: str, object_id: str) -> bool:
        collection = self.client[db_name][collection_name]
        logger.info(object_id)
        return bool(collection.delete_one({'_id': ObjectId(object_id)}))

    def delete_all(self, db_name: str, collection_name: str, query: dict) -> bool:
        collection = self.client[db_name][collection_name]
        logger.info(query)
        return bool(collection.delete_many(query))

    def save(self, db_name: str, collection_name: str, content: dict) -> dict:
        collection = self.client[db_name][collection_name]
        logger.debug(content)
        object_id = collection.insert_one(content).inserted_id
        collection.update_one(filter={'_id': ObjectId(object_id)},
                              update={'$set': dict(ticket_id=self.capture_ticket_id(object_id))})
        result = collection.find_one({'_id': ObjectId(object_id)})
        logger.debug(result)
        return result

    def load(self, db_name: str, collection_name: str, query: dict) -> list:
        collection = self.client[db_name][collection_name]
        logger.debug(query)
        return [x for x in collection.find(query).sort('updated_at', DESCENDING)]

    def load_one(self, db_name: str, collection_name: str, query: dict) -> dict:
        collection = self.client[db_name][collection_name]
        logger.debug(query)
        return collection.find_one(query)

    def update(self, db_name: str, collection_name: str, conditions: dict, update_part: dict, upsert=False) -> None:
        collection = self.client[db_name][collection_name]
        logger.debug(conditions)
        logger.debug(update_part)
        result = collection.update_one(filter=conditions, update={'$set': update_part}, upsert=upsert).modified_count
        logger.debug(result)
        return result

    def create_index(self, db_name: str, collection_name: str, field_name: str):
        collection = self.client[db_name][collection_name]
        return collection.create_index((field_name, ASCENDING), unique=True)

    @staticmethod
    def capture_ticket_id(object_id: str) -> str:
        return str(object_id)[-6:]
