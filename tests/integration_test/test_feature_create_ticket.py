import pytest


from mayday.helpers.ticket_helper import TicketHelper
from mayday.objects.ticket import Ticket

USER_ID = 123456789
USERNAME = 'it_search_ticket'


@pytest.mark.usefixtures('database')
class Test:

    @pytest.fixture(autouse=True)
    def before_all(self, database: dict):
        self.db = database['ticket_table']

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
            username=USERNAME,
            user_id=USER_ID)
        ticket = Ticket(user_id=USER_ID, username=USERNAME).to_obj(dumpy_ticket)
        assert helper.save_ticket(ticket)
        db_in_ticket = self.db.get_tickets_by_user_id(USER_ID).__next__()
        assert db_in_ticket.section == ticket.section
