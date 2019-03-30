import logging
import mayday
from mayday.controllers.mongo import MongoController
from mayday.objects.ticket import Ticket

logger = logging.getLogger()
logger.setLevel(mayday.get_log_level())
logger.addHandler(mayday.console_handler())


class TicketHelper:

    TICKET_DB_NAME = 'ticket'
    TICKET_COLLECTION_NAME = 'tickets'

    def __init__(self, mongo_controller: MongoController):
        if mongo_controller:
            self.mongo = mongo_controller
        else:
            self.mongo = MongoController()

    # Formal Ticket
    def save_ticket(self, ticket: Ticket) -> bool:
        return self.mongo.save(
            db_name=self.TICKET_DB_NAME, collection_name=self.TICKET_COLLECTION_NAME, content=ticket.to_dict())

    def update_ticket(self, ticket: Ticket) -> Ticket:
        self.mongo.update(
            db_name=self.TICKET_DB_NAME, collection_name=self.TICKET_COLLECTION_NAME,
            conditions=dict(user_id=ticket.user_id, ticket_id=ticket.ticket_id), update_part=ticket.to_dict())
        new_ticket = self.mongo.load(
            db_name=self.TICKET_DB_NAME, collection_name=self.TICKET_COLLECTION_NAME, query=dict(ticket_id=ticket.ticket_id))
        return Ticket(user_id=ticket.user_id, username=ticket.username).to_obj(new_ticket[0])
