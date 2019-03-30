import time

from sqlalchemy import BIGINT, BOOLEAN, INT, Column, String, Table
from sqlalchemy.sql.expression import select

from mayday.db.tables import BaseModel
from mayday.objects.user import User


class Users(BaseModel):

    def __init__(self, engine, metadata, role='reader'):
        table = Table(
            'users',
            metadata,
            Column('id', INT, primary_key=True, autoincrement=True),
            Column('user_id', BIGINT, unique=True),
            Column('username', String),
            Column('first_name', String),
            Column('last_name', String),
            Column('language_code', String),
            Column('is_admin', BOOLEAN, default=False),
            Column('is_blacklist', BOOLEAN, default=False),
            Column('is_bot', BOOLEAN, default=False),
            Column('created_at', BIGINT),
            Column('updated_at', BIGINT)
        )
        super().__init__(engine, metadata, table, role)

    def _auth(self, user: User):
        stmt = select([self.table.c.is_blacklist, self.table.c.is_admin]).where(self.table.c.user_id == user.user_id)
        row = self.execute(stmt).fetchone()
        if row:
            return dict(zip(['is_blacklist', 'is_admin'], row))
        return None

    def get_user_profile(self, user_id: int) -> User:
        stmt = select(['*']).where(self.table.c.user_id == user_id)
        row = self.execute(stmt).fetchone()
        if row:
            user_profile = dict(zip([col.key for col in self.table.columns], row))
            return User(user_profile=user_profile)
        return None

    def get_auth(self, user: User) -> dict:
        # check isExisted and blacklist
        auth_result = self._auth(user)
        if auth_result:
            self.raw_update(self.table.c.user_id == user.user_id, dict(updated_at=int(time.time())))
            return auth_result
        self.raw_upsert(user.to_dict())
        return self._auth(user)

    def ban_user(self, user: User):
        return self.raw_update(self.table.c.user_id == user.user_id, dict(is_blacklist=True)).rowcount
