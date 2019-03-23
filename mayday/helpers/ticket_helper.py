import mayday
from mayday import Config
from mayday.controllers import MongoController
from mayday.objects import Ticket


class TicketHelper:

    config = Config().schema_config

    TICKET_DB_NAME = config['ticket_db_name']
    TICKET_COLLECTION_NAME = config['ticket_collection_name']

    def __init__(self, mongo_controller: MongoController):
        self.logger = mayday.get_default_logger('ticket_helper')
        if mongo_controller:
            self.mongo = mongo_controller
        else:
            self.mongo = MongoController(mongo_config=Config.mongo_config)

    # Formal Ticket
    def save_ticket(self, ticket: Ticket) -> bool:
        saved_ticket = self.mongo.save(
            db_name=self.TICKET_DB_NAME, collection_name=self.TICKET_COLLECTION_NAME, content=ticket.to_dict())
        return bool(self.mongo.update(db_name=self.TICKET_DB_NAME, collection_name=self.TICKET_COLLECTION_NAME,
                                      conditions=ticket.to_dict(), update_part=dict(ticket_id=str(saved_ticket['_id'])[-6:])))
    '''
    def update_ticket(self, ticket: Ticket) -> Ticket:
        self.mongo.update(
            db_name=self.TICKET_DB_NAME, collection_name=self.TICKET_COLLECTION_NAME,
            conditions=dict(ticket_id=ticket.ticket_id), update_part=ticket.to_dict())
        new_ticket = self.mongo.load(
            db_name=self.TICKET_DB_NAME, collection_name=self.TICKET_COLLECTION_NAME, query=dict(ticket_id=ticket.ticket_id))
        return Ticket(user_id=ticket.user_id, username=ticket.username).to_obj(new_ticket[0])
    '''
