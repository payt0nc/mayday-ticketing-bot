import pytest


from mayday.helpers.ticket_helper import TicketHelper
from mayday.objects.ticket import Ticket

USER_ID = 123456789


@pytest.mark.usefixtures('database')
class Test:

    @pytest.fixture(autouse=True)
    def before_all(self, database: dict):
        self.db = database['ticket_table']

        yield

    def test_create_ticket(self):
        helper = TicketHelper(self.db)
        dumpy_ticket = dict(
            category=1,
            date=504,
            price_id=1,
            quantity=1,
            section='A1',
            row='',
            seat='',
            wish_dates=list(),
            wish_price_ids=list(),
            wish_quantities=list(),
            source=1,
            remarks='',
            status=1,
            username=__name__,
            user_id=USER_ID)
        ticket = Ticket(user_id=USER_ID, username=__name__).to_obj(dumpy_ticket)
        assert helper.save_ticket(ticket)
        tickets_in_db = self.db.get_tickets_by_user_id(USER_ID)
        assert tickets_in_db
        ticket_in_db = tickets_in_db[0]
        assert ticket_in_db.section == ticket.section
