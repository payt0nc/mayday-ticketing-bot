import unittest

from mayday.objects.ticket import Ticket

USER_ID = 123456789
USERNAME = 'testcase'


class Test(unittest.TestCase):

    def test_ticket_init(self):
        ticket = Ticket(USER_ID, USERNAME)
        self.assertDictEqual(
            ticket.to_dict(),
            dict(
                id=0,
                category=int(),
                date=int(),
                price_id=int(),
                quantity=int(),
                section='',
                row='',
                seat='',
                wish_dates=list(),
                wish_price_ids=list(),
                wish_quantities=list(),
                source_id=0,
                remarks='',
                status=1,
                username=USERNAME,
                user_id=USER_ID,
                created_at=ticket.created_at,
                updated_at=ticket.updated_at
            )
        )

    def test_ticket_dict_to_obj(self):
        ticket = {
            'id': 0,
            'category': 1,
            'date': 503,
            'price_id': 1,
            'quantity': 1,
            'section': 'Yellow',
            'row': '32',
            'seat': '59',
            'wish_dates': list(),
            'wish_price_ids': list(),
            'wish_quantities': list(),
            'source_id': 0,
            'remarks': '',
            'status': 1,
            'username': USERNAME,
            'user_id': USER_ID
        }
        obj = Ticket(USER_ID, USERNAME).to_obj(ticket)
        assert obj.date == ticket['date']
        assert obj.price_id == ticket['price_id']
        assert obj.quantity == ticket['quantity']
        assert obj.status == ticket['status']
        assert obj.category == ticket['category']
        assert obj.id == 0

    def test_ticket_update_field(self):
        ticket = Ticket(USER_ID, USERNAME)

        ticket.update_field('category', 1)
        assert isinstance(ticket.category, int)
        assert ticket.category == 1

        ticket.update_field('category', 0)
        assert isinstance(ticket.category, int)
        assert ticket.category == 0

        ticket.update_field('id', 1)
        assert isinstance(ticket.id, int)
        assert ticket.id == 1

        ticket.update_field('date', 1)
        assert isinstance(ticket.date, int)
        assert ticket.date == 1

        ticket.update_field('price_id', 1)
        assert isinstance(ticket.price_id, int)
        assert ticket.price_id == 1

        ticket.update_field('quantity', 1)
        assert isinstance(ticket.quantity, int)
        assert ticket.quantity == 1

        ticket.update_field('status', 1)
        assert isinstance(ticket.status, int)
        assert ticket.status == 1

        ticket.update_field('wish_dates', 503)
        assert isinstance(ticket.wish_dates, list)
        assert ticket.wish_dates == [503]

        ticket.update_field('wish_dates', 504)
        assert isinstance(ticket.wish_dates, list)
        assert ticket.wish_dates == [503, 504]

        ticket.update_field('wish_dates', 505)
        assert isinstance(ticket.wish_dates, list)
        assert ticket.wish_dates == [503, 504, 505]

        ticket.update_field('wish_dates', 510)
        assert isinstance(ticket.wish_dates, list)
        assert ticket.wish_dates == [503, 504, 505, 510]

        ticket.update_field('wish_dates', 511)
        assert isinstance(ticket.wish_dates, list)
        assert ticket.wish_dates == [503, 504, 505, 510, 511]

        ticket.update_field('wish_price_ids', 1)
        assert isinstance(ticket.wish_price_ids, list)
        assert ticket.wish_price_ids == [1]

        ticket.update_field('wish_price_ids', 2)
        assert isinstance(ticket.wish_price_ids, list)
        assert ticket.wish_price_ids == [1, 2]

        ticket.update_field('wish_price_ids', 3)
        assert isinstance(ticket.wish_price_ids, list)
        assert ticket.wish_price_ids == [1, 2, 3]

        ticket.update_field('wish_price_ids', 4)
        assert isinstance(ticket.wish_price_ids, list)
        assert ticket.wish_price_ids == [1, 2, 3, 4]

        ticket.update_field('wish_quantities', 1)
        assert isinstance(ticket.wish_quantities, list)
        assert ticket.wish_quantities == [1]

        ticket.update_field('wish_quantities', 2)
        assert isinstance(ticket.wish_quantities, list)
        assert ticket.wish_quantities == [1, 2]

        ticket.update_field('wish_quantities', 3)
        assert isinstance(ticket.wish_quantities, list)
        assert ticket.wish_quantities == [1, 2, 3]

        ticket.update_field('wish_quantities', 4)
        assert isinstance(ticket.wish_quantities, list)
        assert ticket.wish_quantities == [1, 2, 3, 4]

        ticket.update_field('status', 0)
        assert isinstance(ticket.status, int)
        assert ticket.status == 0

        ticket.update_field('status', 1)
        assert isinstance(ticket.status, int)
        assert ticket.status == 1

        ticket.update_field('source_id', 1)
        assert isinstance(ticket.status, int)
        assert ticket.status == 1

        # Remove
        ticket.update_field('wish_quantities', 4, remove=True)
        assert isinstance(ticket.wish_quantities, list)
        assert ticket.wish_quantities == [1, 2, 3]

        ticket.update_field('wish_quantities', 3, remove=True)
        assert isinstance(ticket.wish_quantities, list)
        assert ticket.wish_quantities == [1, 2]

        ticket.update_field('wish_quantities', 2, remove=True)
        assert isinstance(ticket.wish_quantities, list)
        assert ticket.wish_quantities == [1]

        ticket.update_field('wish_dates', 511, remove=True)
        assert isinstance(ticket.wish_dates, list)
        assert ticket.wish_dates == [503, 504, 505, 510]

        ticket.update_field('wish_dates', 510, remove=True)
        assert isinstance(ticket.wish_dates, list)
        assert ticket.wish_dates == [503, 504, 505]

        ticket.update_field('wish_dates', 505, remove=True)
        assert isinstance(ticket.wish_dates, list)
        assert ticket.wish_dates == [503, 504]

        ticket.update_field('wish_dates', 504, remove=True)
        assert isinstance(ticket.wish_dates, list)
        assert ticket.wish_dates == [503]

        ticket.update_field('wish_dates', 503, remove=True)
        assert isinstance(ticket.wish_dates, list)
        assert ticket.wish_dates == list()

        ticket.update_field('wish_price_ids', 4, remove=True)
        assert isinstance(ticket.wish_price_ids, list)
        assert ticket.wish_price_ids == [1, 2, 3]

        ticket.update_field('wish_price_ids', 3, remove=True)
        assert isinstance(ticket.wish_price_ids, list)
        assert ticket.wish_price_ids == [1, 2]

        ticket.update_field('wish_price_ids', 2, remove=True)
        assert isinstance(ticket.wish_price_ids, list)
        assert ticket.wish_price_ids == [1]

        ticket.update_field('wish_price_ids', 1, remove=True)
        assert isinstance(ticket.wish_price_ids, list)
        assert ticket.wish_price_ids == list()

    def test_ticket_to_human_readable(self):
        sample_ticket = dict(
            category=1,
            date=503,
            price_id=1,
            quantity=2,
            section='Yellow',
            row='32',
            seat='59',
            wish_dates=[504, 505],
            wish_price_ids=[1],
            wish_quantities=[1, 2],
            source_id=1,
            remarks='',
            status=1,
            username=USERNAME,
            user_id=USER_ID
        )
        ticket = Ticket(USER_ID, USERNAME).to_obj(sample_ticket)
        ticket_string = ticket.to_human_readable()
        assert ticket_string['category'] == '原價轉讓'
        assert ticket_string['date'] == '5.3(Fri)'
        assert ticket_string['price_id'] == '$1180座位'
        assert ticket_string['quantity'] == 2
        assert ticket_string['section'] == 'Yellow'
        assert ticket_string['row'] == '32'
        assert ticket_string['seat'] == '59'
        assert ticket_string['wish_dates'] == '5.4(Sat), 5.5(Sun)'
        assert ticket_string['wish_price_ids'] == '$1180座位'
        assert ticket_string['wish_quantities'] == '1, 2'
        assert ticket_string['status'] == '待交易'
        assert ticket_string['remarks'] == ''

    def test_ticket_check_wishlist(self):
        sample_ticket = dict(
            category=2,
            date=503,
            price_id=1,
            quantity=2,
            section='Yellow',
            row='32',
            seat='59',
            wish_dates=[],
            wish_price_ids=[],
            wish_quantities=[],
            source_id=1,
            remarks='',
            status=1,
            username=USERNAME,
            user_id=USER_ID
        )
        ticket = Ticket(USER_ID, USERNAME).to_obj(sample_ticket)
        assert ticket.validate_wishlist()['status'] is False
        assert ticket.validate_wishlist()['info'] == '希望交換的日期未填喔\n希望交換的價格種類未填喔\n希望交換的數量未填喔'

    def test_ticket_fill_full_wishlist(self):
        sample_ticket = dict(
            category=2,
            date=503,
            price_id=1,
            quantity=2,
            section='Yellow',
            row='32',
            seat='59',
            wish_dates=[],
            wish_price_ids=[],
            wish_quantities=[],
            source_id=1,
            remarks='',
            status=1,
            username=USERNAME,
            user_id=USER_ID
        )
        ticket = Ticket(USER_ID, USERNAME).to_obj(sample_ticket)
        ticket.fill_full_wishlist()

        assert ticket.wish_dates == [503, 504, 505, 510, 511, 512]
        assert ticket.wish_price_ids == [1, 2, 3, 4, 5, 6, 7]
        assert ticket.wish_quantities == [1, 2, 3, 4]
