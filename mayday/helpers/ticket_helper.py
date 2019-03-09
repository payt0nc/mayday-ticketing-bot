import mayday
from mayday import Config
from mayday.controllers import MongoController
from mayday.objects import Ticket


class TicketHelper:

    DB_NAME = 'cache'
    COLLECTION_NAME = 'ticket'

    def __init__(self, mongo_controller: MongoController):
        self.logger = mayday.get_default_logger('ticket_helper')
        if mongo_controller:
            self.mongo = mongo_controller
        else:
            self.mongo = MongoController(mongo_config=Config.mongo_config)

    def update_ticket(self, ticket: Ticket) -> dict:
        pass
