import logging

import mayday
from mayday.config import AUTH_LOGGER as auth_logger
from mayday.config import ROOT_LOGGER as logger
from mayday.db.tables.users import UsersModel
from mayday.objects.user import User


class AuthHelper:

    def __init__(self, table: UsersModel):
        self.ticket_table = table

    def auth(self, user: User) -> bool:
        return self.ticket_table.auth(user)
