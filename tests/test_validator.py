import unittest

from mayday.objects import Ticket
from mayday.item_validator import ItemValidator

USERNAME = 'Mayday'
USER_ID = 123456789


class Test(unittest.TestCase):

    def test_validator_success(self):
        ticket = Ticket(username=USERNAME, user_id=USER_ID)
        ticket.category = 1
        ticket.date = 508
        ticket.price = 1
        ticket.quantity = 2
        ticket.status = 1
        result = ticket.validate()
        assert result['status']

        validator = ItemValidator(ticket.to_dict())
        result = validator.check_ticket()
        assert result['status']

    def test_validator_missing_category(self):
        ticket = Ticket(username=USERNAME, user_id=USER_ID)
        ticket.date = 508
        ticket.price = 1
        ticket.quantity = 2
        ticket.status = 1
        result = ticket.validate()
        assert result['status'] is False
        assert result['info'] == '門票類別未填喔'

        validator = ItemValidator(ticket.to_dict())
        result = validator.check_ticket()
        assert result['status'] is False
        assert result['info'] == '門票類別未填喔'

    def test_validator_missing_date(self):
        ticket = Ticket(username=USERNAME, user_id=USER_ID)
        ticket.category = 1
        ticket.price = 1
        ticket.quantity = 2
        ticket.status = 1
        result = ticket.validate()
        assert result['status'] is False
        assert result['info'] == '日期未填喔'

        validator = ItemValidator(ticket.to_dict())
        result = validator.check_ticket()
        assert result['status'] is False
        assert result['info'] == '日期未填喔'

    def test_validator_missing_price(self):
        ticket = Ticket(username=USERNAME, user_id=USER_ID)
        ticket.category = 1
        ticket.date = 508
        ticket.quantity = 2
        ticket.status = 1
        result = ticket.validate()
        assert result['status'] is False
        assert result['info'] == '價錢未填喔'

        validator = ItemValidator(ticket.to_dict())
        result = validator.check_ticket()
        assert result['status'] is False
        assert result['info'] == '價錢未填喔'

    def test_validator_missing_quantity(self):
        ticket = Ticket(username=USERNAME, user_id=USER_ID)
        ticket.category = 1
        ticket.date = 508
        ticket.price = 1
        ticket.status = 1
        result = ticket.validate()
        assert result['status'] is False
        assert result['info'] == '數量未填喔'

        validator = ItemValidator(ticket.to_dict())
        result = validator.check_ticket()
        assert result['status'] is False
        assert result['info'] == '數量未填喔'

    def test_validator_error_message(self):
        ticket = Ticket(username=USERNAME, user_id=USER_ID)
        expected = '門票類別未填喔\n日期未填喔\n價錢未填喔\n數量未填喔'
        result = ticket.validate()
        assert result['status'] is False
        assert result['info'] == expected

        validator = ItemValidator(ticket.to_dict())
        result = validator.check_ticket()
        assert result['status'] is False
        assert result['info'] == expected
