import json
import unittest

# from mayday.utils import query_util, ticket_util
from mayday import helpers
from mayday.constants import Query, Ticket

USER_ID = 12345678
USERNAME = 'Mayday'


class Test(unittest.TestCase):

    def test_init_ticket(self):
        ticket = Ticket(user_id=USER_ID, username=USERNAME).to_dict()
        helper = helpers.Helper('test')
        result = helper.flatten(ticket)
        expect = {
            'category_id': '',
            'date': '',
            'price_id': '',
            'quantity': '',
            'section': '',
            'row': '',
            'seat': '',
            'status_id': '待交易',
            'remarks': '',
            'user_id': int(USER_ID),
            'username': str(USERNAME),
            'wish_date': '',
            'wish_price_id': '',
            'wish_quantity': ''
        }
        self.assertDictEqual(result, expect)

    def test_flatten_ticket_remark(self):
        ticket = Ticket(user_id=USER_ID, username=USERNAME).to_dict()
        helper = helpers.Helper('test')
        ticket['remarks'] = '123456ABC'
        result = helper.flatten(ticket)
        expect = {
            'category_id': '',
            'date': '',
            'price_id': '',
            'quantity': '',
            'section': '',
            'row': '',
            'seat': '',
            'status_id': '待交易',
            'remarks': '123456ABC',
            'user_id': int(USER_ID),
            'username': str(USERNAME),
            'wish_date': '',
            'wish_price_id': '',
            'wish_quantity': ''
        }
        self.assertDictEqual(result, expect)

    def test_init_query(self):
        query = Query(user_id=USER_ID, username=USERNAME).to_dict()
        helper = helpers.Helper('test')
        result = helper.flatten(query)
        expect = {
            'category_id': '',
            'date': '',
            'price_id': '',
            'quantity': '',
            'status_id':  '',
            'user_id': int(USER_ID),
            'username': str(USERNAME),
        }
        self.assertDictEqual(result, expect)

    def test_flatten_query_category(self):
        source = {
            'category_id': 1,
            'date': [],
            'price_id': [],
            'quantity': [],
            'status_id':  '',
            'user_id': int(USER_ID),
            'username': str(USERNAME),
        }
        helper = helpers.Helper('test')
        result = helper.flatten(source)
        expect = {
            'category_id': '原價轉讓',
            'date': '',
            'price_id': '',
            'quantity': '',
            'status_id':  '',
            'user_id': int(USER_ID),
            'username': str(USERNAME),
        }
        self.assertEqual(json.dumps(result, ensure_ascii=False, sort_keys=True),
                         json.dumps(expect, ensure_ascii=False, sort_keys=True))

    def test_flatten_query_date_1(self):
        helper = helpers.Helper('test')
        source = {
            'category_id': 1,
            'date': [504],
            'price_id': [],
            'quantity': [],
            'status_id':  '',
            'user_id': int(USER_ID),
            'username': str(USERNAME),
        }
        result = helper.flatten(source)
        expect = {
            'category_id': '原價轉讓',
            'date': '5.4(Fri)',
            'price_id': '',
            'quantity': '',
            'status_id':  '',
            'user_id': int(USER_ID),
            'username': str(USERNAME),
        }
        self.assertEqual(json.dumps(result, ensure_ascii=False, sort_keys=True),
                         json.dumps(expect, ensure_ascii=False, sort_keys=True))

    def test_flatten_query_date_2(self):
        helper = helpers.Helper('test')
        source = {
            'category_id': 1,
            'date': [504, 511],
            'price_id': [],
            'quantity': [],
            'status_id':  '',
            'user_id': int(USER_ID),
            'username': str(USERNAME),
        }
        result = helper.flatten(source)
        expect = {
            'category_id': '原價轉讓',
            'date': '5.4(Fri), 5.11(Fri)',
            'price_id': '',
            'quantity': '',
            'status_id':  '',
            'user_id': int(USER_ID),
            'username': str(USERNAME),
        }
        self.assertEqual(json.dumps(result, ensure_ascii=False, sort_keys=True),
                         json.dumps(expect, ensure_ascii=False, sort_keys=True))

    def test_flatten_query_date_3(self):
        helper = helpers.Helper('test')
        source = {
            'category_id': 1,
            'date': [504, 511, 512],
            'price_id': [],
            'quantity': [],
            'status_id':  '',
            'user_id': int(USER_ID),
            'username': str(USERNAME),
        }
        result = helper.flatten(source)
        expect = {
            'category_id': '原價轉讓',
            'date': '5.4(Fri), 5.11(Fri), 5.12(Sat)',
            'price_id': '',
            'quantity': '',
            'status_id':  '',
            'user_id': int(USER_ID),
            'username': str(USERNAME),
        }
        self.assertEqual(json.dumps(result, ensure_ascii=False, sort_keys=True),
                         json.dumps(expect, ensure_ascii=False, sort_keys=True))

    def test_generate_tickets_traits_ls_trait_len(self):
        helper = helpers.Helper('test')
        tickets = [
            {
                "category_id": 2,
                "date": 511,
                "id": 20,
                "price_id": 2,
                "quantity": 2,
                "remarks": None,
                "row": "",
                "section": "",
                "status_id": 1,
                "update_at": "2018-03-28 11:47:16",
                "user_id": USER_ID,
                "username": USERNAME,
                "wish_date": "511,512,513",
                "wish_price_id": "4,2",
                "wish_quantity": "1,2"
            }
        ]
        expect = [[{
            'category_id': '換飛',
            'date': '5.11(Fri)',
            'id': 20,
            'price_id': '$880座位',
            'quantity': '2',
            'row': '',
            'section': '',
            "remarks": '',
            'status_id': '待交易',
            'update_at': '2018-03-28 11:47:16',
            'username': USERNAME,
            "wish_date": "5.11(Fri), 5.12(Sat), 5.13(Sun)",
            "wish_price_id": "$880座位, $680企位",
            "wish_quantity": "1, 2"
        }]]
        result = helper.generate_tickets_traits(tickets)
        self.assertEqual(expect, result)

    def test_generate_tickets_traits_gt_trait_len(self):
        helper = helpers.Helper('test')
        tickets = []
        ticket = {
            "category_id": 2,
            "date": 511,
            "id": 20,
            "price_id": 2,
            "quantity": 2,
            "remarks": None,
            "row": "",
            "section": "",
            "status_id": 1,
            "update_at": "2018-03-28 11:47:16",
            "user_id": USER_ID,
            "username": USERNAME,
            "wish_date": "511,512,513",
            "wish_price_id": "4,2",
            "wish_quantity": "1,2"
        }

        for i in range(0, 6):
            tickets.append(ticket)

        expect_ticket = {
            'category_id': '換飛',
            'date': '5.11(Fri)',
            'id': 20,
            'price_id': '$880座位',
            'quantity': '2',
            'row': '',
            'section': '',
            "remarks": '',
            'status_id': '待交易',
            'update_at': '2018-03-28 11:47:16',
            'username': USERNAME,
            "wish_date": "5.11(Fri), 5.12(Sat), 5.13(Sun)",
            "wish_price_id": "$880座位, $680企位",
            "wish_quantity": "1, 2"
        }
        expect = [[expect_ticket, expect_ticket, expect_ticket, expect_ticket, expect_ticket], [expect_ticket]]

        result = helper.generate_tickets_traits(tickets)
        # self.assertCountEqual(expect, result)
        self.assertEqual(expect, result)

    def test_error_case(self):
        ticket = {
            "category_id": 2,
            "date": 504,
            "price_id": 4,
            "quantity": 2,
            "section": "F2",
            "row": "p",
            "seat": "",
            "status_id": 1,
            "remarks": "",
            "wish_date": [506],
            "wish_price_id": [3],
            "wish_quantity": [],
            "user_id": USER_ID,
            "username": USERNAME
        }
        expected = {
            'category_id': '換飛',
            'date': '5.4(Fri)',
            'price_id': '$680企位',
            'quantity': '2',
            'section': 'F2',
            'row': 'p',
            'seat': '',
            'status_id': '待交易',
            'remarks': '',
            'wish_date': '5.6(Sun)',
            'wish_price_id': '$680座位',
            'wish_quantity': '',
            'user_id': USER_ID,
            'username': USERNAME
        }
        helper = helpers.Helper('test')
        result = helper.flatten(ticket)
        self.assertDictEqual(expected, result)


if __name__ == '__main__':
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
