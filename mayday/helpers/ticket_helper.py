import logging

import mayday
from mayday.db.tables.tickets import TicketsModel
from mayday.objects.ticket import Ticket

logger = logging.getLogger()
logger.setLevel(mayday.get_log_level())
logger.addHandler(mayday.console_handler())


class TicketHelper:

    def __init__(self, table: TicketsModel):
        self.ticket_table = table if table else mayday.TICKETS_TABLE

    def save_ticket(self, ticket: Ticket) -> bool:
        return self.ticket_table.create_ticket(ticket)

    def update_ticket(self, ticket: Ticket) -> Ticket:
        return self.ticket_table.update_ticket(ticket)
