import logging

import mayday
from mayday.db.tables.users import UsersModel
from mayday.objects.user import User

logger = logging.getLogger()
logger.setLevel(mayday.get_log_level())
logger.addHandler(mayday.console_handler())


class AuthHelper:

    def __init__(self, table: UsersModel):
        self.ticket_table = table

    def auth(self, user: User) -> bool:
        return self.ticket_table.auth(user)
