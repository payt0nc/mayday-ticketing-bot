import mayday
from mayday import Config
from mayday.controllers import MongoController
from mayday.objects import Ticket


class TicketHelper:

    config = Config().schema_config

    CACHE_DB_NAME = config['cache_db_name']
    TICKET_DB_NAME = config['ticket_db_name']
    TICKET_COLLECTION_NAME = config['ticket_collection_name']

    def __init__(self, mongo_controller: MongoController):
        self.logger = mayday.get_default_logger('ticket_helper')
        if mongo_controller:
            self.mongo = mongo_controller
        else:
            self.mongo = MongoController(mongo_config=Config.mongo_config)

    # Draft Ticket

    def create_blank_ticket(self, user_id: int, username: str) -> Ticket:
        ticket = Ticket(user_id, username)
        new_ticket = self.mongo.save(
            db_name=self.CACHE_DB_NAME, collection_name=self.TICKET_COLLECTION_NAME, content=ticket.to_dict())
        self.mongo.update(db_name=self.CACHE_DB_NAME, collection_name=self.TICKET_COLLECTION_NAME,
                          conditions=ticket.to_dict(), update_part=dict(ticket_id=str(new_ticket['_id'])[-6:]))
        new_ticket = self.mongo.load(db_name=self.CACHE_DB_NAME, collection_name=self.TICKET_COLLECTION_NAME,
                                     query={'_id': new_ticket['_id']})[0]
        return Ticket(user_id, username).to_obj(new_ticket)

    def load_cache_ticket(self, user_id: int, username: str) -> Ticket:
        ticket = self.mongo.load(
            db_name=self.CACHE_DB_NAME, collection_name=self.TICKET_COLLECTION_NAME,
            query=dict(user_id=user_id, username=username))[0]
        return Ticket(user_id=user_id, username=username).to_obj(ticket)

    def update_cache_ticket(self, ticket: Ticket) -> Ticket:
        self.mongo.update(
            db_name=self.CACHE_DB_NAME, collection_name=self.TICKET_COLLECTION_NAME,
            conditions=dict(user_id=ticket.user_id, username=ticket.username), update_part=ticket.to_dict())
        cached_ticket = self.mongo.load(
            db_name=self.CACHE_DB_NAME, collection_name=self.TICKET_COLLECTION_NAME, query=dict(user_id=ticket.user_id, username=ticket.username))
        self.logger.debug(cached_ticket)
        return Ticket(user_id=ticket.user_id, username=ticket.username).to_obj(cached_ticket[0])

    def reset_cache_ticket(self, ticket: Ticket) -> Ticket:
        self.logger.debug(ticket.to_dict())
        tickets_count = self.mongo.count(
            db_name=self.CACHE_DB_NAME, collection_name=self.TICKET_COLLECTION_NAME,
            query=dict(ticket_id=ticket.ticket_id))
        if tickets_count:
            result = self.mongo.delete_all(
                db_name=self.CACHE_DB_NAME, collection_name=self.TICKET_COLLECTION_NAME, query=dict(user_id=ticket.user_id))
            if result is False:
                self.logger.warning(dict(info='Cant delete ticket', ticket=ticket.to_dict()))
        self.create_blank_ticket(ticket.user_id, ticket.username)
        return self.load_cache_ticket(ticket.user_id, ticket.username)

    # Formal Ticket

    def save_ticket(self, ticket: Ticket) -> bool:
        saved_ticket = self.mongo.save(
            db_name=self.TICKET_DB_NAME, collection_name=self.TICKET_COLLECTION_NAME, content=ticket.to_dict())
        return bool(self.mongo.update(db_name=self.TICKET_DB_NAME, collection_name=self.TICKET_COLLECTION_NAME,
                                      conditions=ticket.to_dict(), update_part=dict(ticket_id=str(saved_ticket['_id'])[-6:])))

    def update_ticket(self, ticket: Ticket) -> Ticket:
        self.mongo.update(
            db_name=self.TICKET_DB_NAME, collection_name=self.TICKET_COLLECTION_NAME,
            conditions=dict(ticket_id=ticket.ticket_id), update_part=ticket.to_dict())
        new_ticket = self.mongo.load(
            db_name=self.TICKET_DB_NAME, collection_name=self.TICKET_COLLECTION_NAME, query=dict(ticket_id=ticket.ticket_id))
        return Ticket(user_id=ticket.user_id, username=ticket.username).to_obj(new_ticket[0])
