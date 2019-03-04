import unittest

from mayday.constants import Ticket
from mayday.validators.ticket_validator import TicketValidator

USERNAME = 'Mayday'
USER_ID = 123456789


class Test(unittest.TestCase):

    def test_validator_SUCESS(self):
        ticket = Ticket(username=USERNAME, user_id=USER_ID).to_dict()
        ticket['category_id'] = 1
        ticket['date'] = 508
        ticket['price_id'] = 1
        ticket['quantity'] = 2
        validator = TicketValidator(ticket)
        result = validator.check_ticket()
        self.assertTrue(result.get('status'))

    def test_validator_missing_date(self):
        ticket = Ticket(username=USERNAME, user_id=USER_ID).to_dict()
        ticket['category_id'] = 1
        ticket['price_id'] = 1
        ticket['quantity'] = 2
        validator = TicketValidator(ticket)
        result = validator.check_ticket()
        self.assertFalse(result.get('status'))

    def test_validator_missing_category_id(self):
        ticket = Ticket(username=USERNAME, user_id=USER_ID).to_dict()
        ticket['date'] = 508
        ticket['price_id'] = 1
        ticket['quantity'] = 2
        validator = TicketValidator(ticket)
        result = validator.check_ticket()
        self.assertFalse(result.get('status'))

    def test_validator_missing_price_id(self):
        ticket = Ticket(username=USERNAME, user_id=USER_ID).to_dict()
        ticket['category_id'] = 1
        ticket['date'] = 508
        ticket['quantity'] = 2
        validator = TicketValidator(ticket)
        result = validator.check_ticket()
        self.assertFalse(result.get('status'))

    def test_validator_missing_quantity(self):
        ticket = Ticket(username=USERNAME, user_id=USER_ID).to_dict()
        ticket['category_id'] = 1
        ticket['date'] = 508
        ticket['price_id'] = 1
        validator = TicketValidator(ticket)
        result = validator.check_ticket()
        self.assertFalse(result.get('status'))

    def test_validator_error_message(self):
        ticket = Ticket(username=USERNAME, user_id=USER_ID).to_dict()
        validator = TicketValidator(ticket)
        result = validator.check_ticket()
        expected = '門票類別未填喔\n日期未填喔\n價錢未填喔\n數量未填喔'
        self.assertEqual(expected, result['info'])


if __name__ == '__main__':
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
