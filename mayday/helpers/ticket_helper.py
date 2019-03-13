import mayday
from mayday import Config
from mayday.controllers import MongoController
from mayday.objects import Ticket


class TicketHelper:

    CACHE_DB_NAME = 'cache'
    TICKET_DB_NAME = 'ticket'
    COLLECTION_NAME = 'tickets'

    def __init__(self, mongo_controller: MongoController):
        self.logger = mayday.get_default_logger('ticket_helper')
        if mongo_controller:
            self.mongo = mongo_controller
        else:
            self.mongo = MongoController(mongo_config=Config.mongo_config)

    # Draft Ticket

    def create_blank_ticket(self, ticket: Ticket) -> Ticket:
        cached_ticket = self.mongo.save(
            db_name=self.CACHE_DB_NAME, collection_name=self.COLLECTION_NAME, content=ticket.to_dict())
        ticket = Ticket(user_id=ticket.user_id, username=ticket.username).to_obj(cached_ticket)
        self.logger.debug(ticket.to_dict())
        ticket_dict = self.mongo.save(
            db_name=self.CACHE_DB_NAME, collection_name=self.COLLECTION_NAME, content=ticket.to_dict())
        return Ticket(user_id=ticket.user_id, username=ticket.username).to_obj(ticket_dict)

    def update_cache_ticket(self, ticket: Ticket) -> Ticket:
        cached_ticket = self.mongo.save(
            db_name=self.CACHE_DB_NAME, collection_name=self.COLLECTION_NAME, content=ticket.to_dict())
        return Ticket(user_id=ticket.user_id, username=ticket.username).to_obj(cached_ticket)

    def reset_cache_ticket(self, ticket: Ticket) -> Ticket:
        self.logger.debug(ticket.to_dict())
        tickets = self.mongo.load(
            db_name=self.CACHE_DB_NAME, collection_name=self.COLLECTION_NAME,
            query=dict(ticket_id=ticket.ticket_id, user_id=ticket.user_id))
        if tickets:
            result = self.mongo.delete(
                db_name=self.CACHE_DB_NAME, collection_name=self.COLLECTION_NAME, object_id=tickets[0]['_id'])
            if result is False:
                self.logger.warning(dict(info='Cant delete ticket', ticket=ticket.to_dict()))
        return self.create_blank_ticket(Ticket(user_id=ticket.user_id, username=ticket.username))

    # Formal Ticket

    def save_ticket(self, ticket: Ticket) -> bool:
        saved_ticket = self.mongo.save(
            db_name=self.TICKET_DB_NAME, collection_name=self.COLLECTION_NAME, content=ticket.to_dict())
        self.logger.debug(saved_ticket)
        ticket_id = saved_ticket['_id']
        return self.mongo.upsert(
            db_name=self.TICKET_DB_NAME, collection_name=self.COLLECTION_NAME,
            content=Ticket(user_id=ticket.user_id, username=ticket.username).to_obj(saved_ticket).to_dict(),
            replace_condition=dict(_id=ticket_id))

    def update_ticket(self, ticket: Ticket) -> Ticket:
        saved_ticket = self.mongo.upsert(
            db_name=self.TICKET_DB_NAME, collection_name=self.COLLECTION_NAME, content=ticket.to_dict())
        return Ticket(user_id=ticket.user_id, username=ticket.username).to_obj(saved_ticket)
