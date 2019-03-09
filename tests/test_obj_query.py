import unittest

from mayday.objects import Query


class Test(unittest.TestCase):

    def test_query_init(self):
        user_id = 123456789
        username = 'testcase'
        category_id = 0

        query = Query(user_id, username, category_id)
        self.assertDictEqual(
            query.to_dict(),
            dict(
                category=0,
                dates=list(),
                prices=list(),
                quantities=list(),
                status=0,
                username='testcase',
                user_id=123456789
            )
        )

    def test_query_dict_to_obj(self):
        user_id = 123456789
        username = 'testcase'
        category_id = 0

        query = dict(
            category=0,
            dates=[503, 504],
            prices=[1, 2],
            quantities=[2, 3],
            status=0,
            username='testcase',
            user_id=123456789
        )
        obj = Query(user_id, username, category_id).to_obj(query)
        assert obj.dates == set(query['dates'])
        assert obj.prices == set(query['prices'])
        assert obj.quantities == set(query['quantities'])
        assert obj.status == query['status']
        assert obj.category == query['category']

        assert obj.to_dict() == query

    def test_query_update_field(self):
        user_id = 123456789
        username = 'testcase'
        category_id = 0

        query = Query(user_id, username, category_id)

        query.update_field('category', 1)
        assert isinstance(query.category, int)
        assert query.category == 1

        query.update_field('dates', 503)
        assert isinstance(query.dates, set)
        assert query.dates == {503}

        query.update_field('dates', 504)
        assert isinstance(query.dates, set)
        assert query.dates == {503, 504}

        query.update_field('dates', 505)
        assert isinstance(query.dates, set)
        assert query.dates == {503, 504, 505}

        query.update_field('dates', 510)
        assert isinstance(query.dates, set)
        assert query.dates == {503, 504, 505, 510}

        query.update_field('dates', 511)
        assert isinstance(query.dates, set)
        assert query.dates == {503, 504, 505, 510, 511}

        query.update_field('prices', 1)
        assert isinstance(query.prices, set)
        assert query.prices == {1}

        query.update_field('prices', 2)
        assert isinstance(query.prices, set)
        assert query.prices == {1, 2}

        query.update_field('prices', 3)
        assert isinstance(query.prices, set)
        assert query.prices == {1, 2, 3}

        query.update_field('prices', 4)
        assert isinstance(query.prices, set)
        assert query.prices == {1, 2, 3, 4}

        query.update_field('quantities', 1)
        assert isinstance(query.quantities, set)
        assert query.quantities == {1}

        query.update_field('quantities', 2)
        assert isinstance(query.quantities, set)
        assert query.quantities == {1, 2}

        query.update_field('quantities', 3)
        assert isinstance(query.quantities, set)
        assert query.quantities == {1, 2, 3}

        query.update_field('quantities', 4)
        assert isinstance(query.quantities, set)
        assert query.quantities == {1, 2, 3, 4}

        query.update_field('status', 0)
        assert isinstance(query.status, int)
        assert query.status == 0

        query.update_field('status', 1)
        assert isinstance(query.status, int)
        assert query.status == 1

        # Remove
        query.update_field('quantities', 4, remove=True)
        assert isinstance(query.quantities, set)
        assert query.quantities == {1, 2, 3}

        query.update_field('quantities', 3, remove=True)
        assert isinstance(query.quantities, set)
        assert query.quantities == {1, 2}

        query.update_field('quantities', 2, remove=True)
        assert isinstance(query.quantities, set)
        assert query.quantities == {1}

        query.update_field('dates', 511, remove=True)
        assert isinstance(query.dates, set)
        assert query.dates == {503, 504, 505, 510}

        query.update_field('dates', 510, remove=True)
        assert isinstance(query.dates, set)
        assert query.dates == {503, 504, 505}

        query.update_field('dates', 505, remove=True)
        assert isinstance(query.dates, set)
        assert query.dates == {503, 504}

        query.update_field('dates', 504, remove=True)
        assert isinstance(query.dates, set)
        assert query.dates == {503}

        query.update_field('dates', 503, remove=True)
        assert isinstance(query.dates, set)
        assert query.dates == set()

        query.update_field('prices', 4, remove=True)
        assert isinstance(query.prices, set)
        assert query.prices == {1, 2, 3}

        query.update_field('prices', 3, remove=True)
        assert isinstance(query.prices, set)
        assert query.prices == {1, 2}

        query.update_field('prices', 2, remove=True)
        assert isinstance(query.prices, set)
        assert query.prices == {1}

        query.update_field('prices', 1, remove=True)
        assert isinstance(query.prices, set)
        assert query.prices == set()
