<<<<<<< HEAD
from mayday.config import AUTH_LOGGER as auth_logger
=======
import logging

import mayday
from mayday.config import AUTH_LOGGER as auth_logger
from mayday.config import ROOT_LOGGER as logger
>>>>>>> 589487b7c59176c1e1cd4bd9d287bafb4b3f94b3
from mayday.db.tables.users import UsersModel
from mayday.objects.user import User


class AuthHelper:

    def __init__(self, table: UsersModel):
        self.ticket_table = table

    def auth(self, user: User) -> bool:
        result = self.ticket_table.auth(user)
        result.update(dict(user_id=user.user_id))
        auth_logger.info(result)
        return result
