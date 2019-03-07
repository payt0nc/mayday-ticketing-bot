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
                price_ids=list(),
                quantities=list(),
                status=0,
                username='testcase',
                user_id=123456789
            )
        )
