import unittest

from mayday.objects import Ticket


class Test(unittest.TestCase):

    def test_ticket_init(self):
        user_id = 123456789
        username = 'testcase'

        ticket = Ticket(user_id, username)
        self.assertDictEqual(
            ticket.to_dict(),
            dict(
                category='',
                date='',
                price=int(),
                quantity=int(),
                section='',
                row='',
                seat='',
                wish_dates=set(),
                wish_prices=set(),
                wish_quantities=set(),
                remarks='',
                status=1,
                username='testcase',
                user_id=123456789
            )
        )

    def test_ticket_dict_to_obj(self):
        user_id = 123456789
        username = 'testcase'
        ticket = dict(
            category=1,
            date=503,
            price=1,
            quantity=1,
            section='Yellow',
            row='32',
            seat='59',
            wish_dates=set(),
            wish_prices=set(),
            wish_quantities=set(),
            remarks='',
            status=1,
            username='testcase',
            user_id=123456789
        )
        obj = Ticket(user_id, username).to_obj(ticket)
        assert obj.date == ticket['date']
        assert obj.price == ticket['price']
        assert obj.quantity == ticket['quantity']
        assert obj.status == ticket['status']
        assert obj.category == ticket['category']
        assert obj.to_dict() == ticket

    def test_ticket_update_field(self):
        user_id = 123456789
        username = 'testcase'

        ticket = Ticket(user_id, username)

        ticket.update_field('category', 1)
        assert isinstance(ticket.category, int)
        assert ticket.category == 1

        ticket.update_field('category', 0)
        assert isinstance(ticket.category, int)
        assert ticket.category == 0

        ticket.update_field('date', 1)
        assert isinstance(ticket.date, int)
        assert ticket.date == 1

        ticket.update_field('price', 1)
        assert isinstance(ticket.price, int)
        assert ticket.price == 1

        ticket.update_field('quantity', 1)
        assert isinstance(ticket.quantity, int)
        assert ticket.quantity == 1

        ticket.update_field('status', 1)
        assert isinstance(ticket.status, int)
        assert ticket.status == 1

        ticket.update_field('wish_dates', 503)
        assert isinstance(ticket.wish_dates, set)
        assert ticket.wish_dates == {503}

        ticket.update_field('wish_dates', 504)
        assert isinstance(ticket.wish_dates, set)
        assert ticket.wish_dates == {503, 504}

        ticket.update_field('wish_dates', 505)
        assert isinstance(ticket.wish_dates, set)
        assert ticket.wish_dates == {503, 504, 505}

        ticket.update_field('wish_dates', 510)
        assert isinstance(ticket.wish_dates, set)
        assert ticket.wish_dates == {503, 504, 505, 510}

        ticket.update_field('wish_dates', 511)
        assert isinstance(ticket.wish_dates, set)
        assert ticket.wish_dates == {503, 504, 505, 510, 511}

        ticket.update_field('wish_prices', 1)
        assert isinstance(ticket.wish_prices, set)
        assert ticket.wish_prices == {1}

        ticket.update_field('wish_prices', 2)
        assert isinstance(ticket.wish_prices, set)
        assert ticket.wish_prices == {1, 2}

        ticket.update_field('wish_prices', 3)
        assert isinstance(ticket.wish_prices, set)
        assert ticket.wish_prices == {1, 2, 3}

        ticket.update_field('wish_prices', 4)
        assert isinstance(ticket.wish_prices, set)
        assert ticket.wish_prices == {1, 2, 3, 4}

        ticket.update_field('wish_quantities', 1)
        assert isinstance(ticket.wish_quantities, set)
        assert ticket.wish_quantities == {1}

        ticket.update_field('wish_quantities', 2)
        assert isinstance(ticket.wish_quantities, set)
        assert ticket.wish_quantities == {1, 2}

        ticket.update_field('wish_quantities', 3)
        assert isinstance(ticket.wish_quantities, set)
        assert ticket.wish_quantities == {1, 2, 3}

        ticket.update_field('wish_quantities', 4)
        assert isinstance(ticket.wish_quantities, set)
        assert ticket.wish_quantities == {1, 2, 3, 4}

        ticket.update_field('status', 0)
        assert isinstance(ticket.status, int)
        assert ticket.status == 0

        ticket.update_field('status', 1)
        assert isinstance(ticket.status, int)
        assert ticket.status == 1

        # Remove
        ticket.update_field('wish_quantities', 4, remove=True)
        assert isinstance(ticket.wish_quantities, set)
        assert ticket.wish_quantities == {1, 2, 3}

        ticket.update_field('wish_quantities', 3, remove=True)
        assert isinstance(ticket.wish_quantities, set)
        assert ticket.wish_quantities == {1, 2}

        ticket.update_field('wish_quantities', 2, remove=True)
        assert isinstance(ticket.wish_quantities, set)
        assert ticket.wish_quantities == {1}

        ticket.update_field('wish_dates', 511, remove=True)
        assert isinstance(ticket.wish_dates, set)
        assert ticket.wish_dates == {503, 504, 505, 510}

        ticket.update_field('wish_dates', 510, remove=True)
        assert isinstance(ticket.wish_dates, set)
        assert ticket.wish_dates == {503, 504, 505}

        ticket.update_field('wish_dates', 505, remove=True)
        assert isinstance(ticket.wish_dates, set)
        assert ticket.wish_dates == {503, 504}

        ticket.update_field('wish_dates', 504, remove=True)
        assert isinstance(ticket.wish_dates, set)
        assert ticket.wish_dates == {503}

        ticket.update_field('wish_dates', 503, remove=True)
        assert isinstance(ticket.wish_dates, set)
        assert ticket.wish_dates == set()

        ticket.update_field('wish_prices', 4, remove=True)
        assert isinstance(ticket.wish_prices, set)
        assert ticket.wish_prices == {1, 2, 3}

        ticket.update_field('wish_prices', 3, remove=True)
        assert isinstance(ticket.wish_prices, set)
        assert ticket.wish_prices == {1, 2}

        ticket.update_field('wish_prices', 2, remove=True)
        assert isinstance(ticket.wish_prices, set)
        assert ticket.wish_prices == {1}

        ticket.update_field('wish_prices', 1, remove=True)
        assert isinstance(ticket.wish_prices, set)
        assert ticket.wish_prices == set()
