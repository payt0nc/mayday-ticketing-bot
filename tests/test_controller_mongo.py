import unittest
import pytest
import mongomock

from mayday.controllers.mongo import MongoController


@pytest.mark.usefixtures()
class Test(unittest.TestCase):

    @pytest.fixture(autouse=True, scope='function')
    def before_all(self):
        self.client = mongomock.MongoClient()

    def test_mongo(self):
        mongo = MongoController(mongo_client=self.client)
        doc = dict(test='Do you see me?', text='Yes!')
        obj = mongo.save(db_name='test', collection_name='uniitest', content=doc)
        assert obj['text'] == doc['text']
        assert obj['test'] == doc['test']
        result = mongo.load(db_name='test', collection_name='uniitest', query={'text': 'Yes!'})
        assert result[0]['text'] == doc['text']
        assert result[0]['test'] == doc['test']
        assert mongo.count(db_name='test', collection_name='uniitest', query={'text': 'Yes!'}) == 1
