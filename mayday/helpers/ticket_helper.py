import mayday
from mayday.config import ROOT_LOGGER as logger
from mayday.db.tables.tickets import TicketsModel
from mayday.objects.ticket import Ticket


class TicketHelper:

    def __init__(self, table: TicketsModel):
        self.ticket_table = table

    def save_ticket(self, ticket: Ticket) -> bool:
        return self.ticket_table.create_ticket(ticket)

    def update_ticket(self, ticket: Ticket) -> Ticket:
        return self.ticket_table.update_ticket(ticket)

    def load_ticket_by_user_id(self, user_id: int) -> list:
        return self.ticket_table.get_tickets_by_user_id(user_id)
