import logging

from mayday.db.tables.users import UsersModel
from mayday.objects.user import User

auth_logger: logging.Logger = logging.getLogger('auth')

class AuthHelper:

    def __init__(self, table: UsersModel):
        self.ticket_table = table

    def auth(self, user: User) -> bool:
        result = self.ticket_table.auth(user)
        result.update(dict(user_id=user.user_id))
        auth_logger.info(result)
        return result
