import pytest
from mayday.objects.ticket import Ticket


TICKET_1 = dict(
    category=1,
    date=505,
    price_id=2,
    quantity=1,
    section='C1',
    row='',
    seat='',
    wish_dates=list(),
    wish_price_ids=list(),
    wish_quantities=list(),
    source_id=1,
    remarks='',
    status=1,
    username='test_account_1',
    user_id=8081)


@pytest.mark.usefixtures('database')
class Test:

    @pytest.fixture(autouse=True)
    def before_all(self, database: dict):
        self.db = database['ticket_table']
        self.db.raw_insert(TICKET_1)

    def test_update_ticket(self):
        # query = Query(category_id=1, user_id=USER_ID, username=USERNAME)
        # tickets = self.ticket_table.get_tickets_by_conditions(query.to_dict())

        tickets = self.db.get_tickets_by_user_id(8081)
        assert tickets

        ticket = tickets.__next__()
        ticket.update_field('status', 4)
        ticket_id = ticket.id
        assert isinstance(ticket, Ticket)
        assert self.db.update_ticket(ticket)

        new_ticket = self.db.get_ticket_by_ticket_id(ticket_id)

        assert new_ticket.id
        assert new_ticket.category == ticket.category
        assert new_ticket.date == ticket.date
        assert new_ticket.price_id == ticket.price_id
        assert new_ticket.quantity == ticket.quantity
        assert new_ticket.section == ticket.section
        assert new_ticket.row == ticket.row
        assert new_ticket.seat == ticket.seat
        assert new_ticket.wish_dates == ticket.wish_dates
        assert new_ticket.wish_price_ids == ticket.wish_price_ids
        assert new_ticket.wish_quantities == ticket.wish_quantities
        assert new_ticket.source_id == ticket.source_id
        assert new_ticket.remarks == ticket.remarks
        assert new_ticket.status == ticket.status
        assert new_ticket.username == ticket.username
        assert new_ticket.user_id == ticket.user_id
