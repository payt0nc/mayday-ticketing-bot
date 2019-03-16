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
        doc = dict(user_id=123456789, username='pytest', test='Do you see me?', text='Yes!')

        # save
        obj = mongo.save(db_name='test', collection_name='uniitest', content=doc)
        assert obj['text'] == doc['text']
        assert obj['test'] == doc['test']

        # count
        assert mongo.count(db_name='test', collection_name='uniitest', query={'text': 'Yes!'}) == 1

        # load
        result = mongo.load(db_name='test', collection_name='uniitest', query={'text': 'Yes!'})
        assert result[0]['text'] == doc['text']
        assert result[0]['test'] == doc['test']

        # upsert
        replace_condition = dict(user_id=123456789, username='pytest')
        doc.update(dict(text='No!'))
        assert mongo.upsert(db_name='test', collection_name='uniitest', filter=replace_condition, update_part=doc)
        new_doc = mongo.load(db_name='test', collection_name='uniitest', query=replace_condition)
        assert new_doc[0]['text'] == 'No!'

        # delete
        assert mongo.delete_one(db_name='test', collection_name='uniitest', object_id=result[0]['_id'])

        # delete
        mongo.save(db_name='test', collection_name='uniitest', content=dict(
            user_id=123456789, username='pytest', test='Do you see me?', text='Yes! 1'))
        mongo.save(db_name='test', collection_name='uniitest', content=dict(
            user_id=123456789, username='pytest', test='Do you see me?', text='No!'))
        assert mongo.delete_all(db_name='test', collection_name='uniitest',
                                query=dict(user_id=123456789, username='pytest'))
