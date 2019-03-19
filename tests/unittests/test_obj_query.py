import unittest

from mayday.objects import Query

USER_ID = 123456789
USERNAME = 'testcase'
CATEGORY = 1


class Test(unittest.TestCase):

    def test_query_init(self):
        query = Query(user_id=USER_ID, username=USERNAME, category_id=CATEGORY)
        expect = dict(
            category=1,
            dates=list(),
            prices=list(),
            quantities=list(),
            status=1,
            username=USERNAME,
            user_id=USER_ID
        )
        self.assertDictEqual(query.to_dict(), expect)

    def test_query_dict_to_obj(self):
        query = dict(
            category=1,
            dates=[503, 504],
            prices=[1, 2],
            quantities=[2, 3],
            status=1,
            username=USERNAME,
            user_id=USER_ID
        )
        obj = Query(user_id=USER_ID, username=USERNAME, category_id=CATEGORY).to_obj(query)
        assert obj.dates == query['dates']
        assert obj.prices == query['prices']
        assert obj.quantities == query['quantities']
        assert obj.status == query['status']
        assert obj.category == query['category']

        assert obj.to_dict() == query

    def test_query_update_field(self):

        query = Query(user_id=USER_ID, username=USERNAME, category_id=CATEGORY)

        query.update_field('category', 1)
        assert isinstance(query.category, int)
        assert query.category == 1

        query.update_field('dates', 503)
        assert isinstance(query.dates, list)
        assert query.dates == [503]

        query.update_field('dates', 504)
        assert isinstance(query.dates, list)
        assert query.dates == [503, 504]

        query.update_field('dates', 505)
        assert isinstance(query.dates, list)
        assert query.dates == [503, 504, 505]

        query.update_field('dates', 510)
        assert isinstance(query.dates, list)
        assert query.dates == [503, 504, 505, 510]

        query.update_field('dates', 511)
        assert isinstance(query.dates, list)
        assert query.dates == [503, 504, 505, 510, 511]

        query.update_field('prices', 1)
        assert isinstance(query.prices, list)
        assert query.prices == [1]

        query.update_field('prices', 2)
        assert isinstance(query.prices, list)
        assert query.prices == [1, 2]

        query.update_field('prices', 3)
        assert isinstance(query.prices, list)
        assert query.prices == [1, 2, 3]

        query.update_field('prices', 4)
        assert isinstance(query.prices, list)
        assert query.prices == [1, 2, 3, 4]

        query.update_field('quantities', 1)
        assert isinstance(query.quantities, list)
        assert query.quantities == [1]

        query.update_field('quantities', 2)
        assert isinstance(query.quantities, list)
        assert query.quantities == [1, 2]

        query.update_field('quantities', 3)
        assert isinstance(query.quantities, list)
        assert query.quantities == [1, 2, 3]

        query.update_field('quantities', 4)
        assert isinstance(query.quantities, list)
        assert query.quantities == [1, 2, 3, 4]

        query.update_field('status', 1)
        assert isinstance(query.status, int)
        assert query.status == 1

        query.update_field('status', 2)
        assert isinstance(query.status, int)
        assert query.status == 2

        # Remove
        query.update_field('quantities', 4, remove=True)
        assert isinstance(query.quantities, list)
        assert query.quantities == [1, 2, 3]

        query.update_field('quantities', 3, remove=True)
        assert isinstance(query.quantities, list)
        assert query.quantities == [1, 2]

        query.update_field('quantities', 2, remove=True)
        assert isinstance(query.quantities, list)
        assert query.quantities == [1]

        query.update_field('dates', 511, remove=True)
        assert isinstance(query.dates, list)
        assert query.dates == [503, 504, 505, 510]

        query.update_field('dates', 510, remove=True)
        assert isinstance(query.dates, list)
        assert query.dates == [503, 504, 505]

        query.update_field('dates', 505, remove=True)
        assert isinstance(query.dates, list)
        assert query.dates == [503, 504]

        query.update_field('dates', 504, remove=True)
        assert isinstance(query.dates, list)
        assert query.dates == [503]

        query.update_field('dates', 503, remove=True)
        assert isinstance(query.dates, list)
        assert query.dates == list()

        query.update_field('prices', 4, remove=True)
        assert isinstance(query.prices, list)
        assert query.prices == [1, 2, 3]

        query.update_field('prices', 3, remove=True)
        assert isinstance(query.prices, list)
        assert query.prices == [1, 2]

        query.update_field('prices', 2, remove=True)
        assert isinstance(query.prices, list)
        assert query.prices == [1]

        query.update_field('prices', 1, remove=True)
        assert isinstance(query.prices, list)
        assert query.prices == list()

    def test_query_to_human_readable(self):
        sample_query = dict(
            category=1,
            dates=[503, 504],
            prices=[1, 2],
            quantities=[2, 3],
            status=1,
            username=USERNAME,
            user_id=USER_ID
        )
        query = Query(user_id=USER_ID, username=USERNAME, category_id=CATEGORY).to_obj(sample_query)
        query_string = query.to_human_readable()

        assert query_string['category'] == '原價轉讓'
        assert query_string['dates'] == '5.3(Fri), 5.4(Sat)'
        assert query_string['prices'] == '$1180座位, $880座位'
        assert query_string['quantities'] == '2, 3'
        assert query_string['status'] == '待交易'

    def test_query_to_mongo_syntax(self):
        sample_query = dict(
            category=1,
            dates=[503, 504],
            prices=[1, 2],
            quantities=[2, 3],
            status=1,
            username=USERNAME,
            user_id=USER_ID
        )
        query = Query(user_id=USER_ID, username=USERNAME, category_id=CATEGORY).to_obj(sample_query)
        expected = dict(
            category=1,
            date={'$in': [503, 504]},
            price={'$in': [1, 2]},
            quantity={'$in': [2, 3]},
            status=1,
            user_id=USER_ID,
            username=USERNAME
        )
        from pprint import pprint
        pprint(query.to_mongo_syntax())
        self.assertDictEqual(expected, query.to_mongo_syntax())

    def test_query_to_mongo_syntax_2(self):
        sample_query = dict(
            category=1,
            dates=[503, 504],
            prices=[1, 2],
            quantities=[],
            status=1,
            username=USERNAME,
            user_id=USER_ID
        )
        query = Query(user_id=USER_ID, username=USERNAME, category_id=CATEGORY).to_obj(sample_query)
        expected = dict(
            category=1,
            date={'$in': [503, 504]},
            price={'$in': [1, 2]},
            status=1,
            user_id=USER_ID,
            username=USERNAME
        )
        self.assertDictEqual(expected, query.to_mongo_syntax())
