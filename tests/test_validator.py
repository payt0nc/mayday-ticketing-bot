import unittest

from mayday.objects import Ticket
from mayday.item_validator import ItemValidator

USERNAME = 'Mayday'
USER_ID = 123456789


class Test(unittest.TestCase):

    def test_validator_success(self):
        ticket = Ticket(username=USERNAME, user_id=USER_ID).to_dict()
        ticket['category'] = 1
        ticket['date'] = 508
        ticket['price'] = 1
        ticket['quantity'] = 2
        ticket['status'] = 1
        validator = ItemValidator(ticket)
        result = validator.check_ticket()
        print(result)
        self.assertTrue(result.get('status'))

    def test_validator_missing_category(self):
        ticket = Ticket(username=USERNAME, user_id=USER_ID).to_dict()
        ticket['date'] = 508
        ticket['price'] = 1
        ticket['quantity'] = 2
        ticket['status'] = 1
        validator = ItemValidator(ticket)
        result = validator.check_ticket()
        self.assertFalse(result.get('status'))

    def test_validator_missing_date(self):
        ticket = Ticket(username=USERNAME, user_id=USER_ID).to_dict()
        ticket['category'] = 1
        ticket['price'] = 1
        ticket['quantity'] = 2
        ticket['status'] = 1
        validator = ItemValidator(ticket)
        result = validator.check_ticket()
        self.assertFalse(result.get('status'))

    def test_validator_missing_price(self):
        ticket = Ticket(username=USERNAME, user_id=USER_ID).to_dict()
        ticket['category'] = 1
        ticket['date'] = 508
        ticket['quantity'] = 2
        ticket['status'] = 1
        validator = ItemValidator(ticket)
        result = validator.check_ticket()
        self.assertFalse(result.get('status'))

    def test_validator_missing_quantity(self):
        ticket = Ticket(username=USERNAME, user_id=USER_ID).to_dict()
        ticket['category'] = 1
        ticket['date'] = 508
        ticket['price'] = 1
        ticket['status'] = 1
        validator = ItemValidator(ticket)
        result = validator.check_ticket()
        self.assertFalse(result.get('status'))

    def test_validator_error_message(self):
        ticket = Ticket(username=USERNAME, user_id=USER_ID).to_dict()
        validator = ItemValidator(ticket)
        result = validator.check_ticket()
        expected = '門票類別未填喔\n門票狀態未填喔\n日期未填喔\n價錢未填喔\n數量未填喔'
        self.assertEqual(expected, result['info'])


if __name__ == '__main__':
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
