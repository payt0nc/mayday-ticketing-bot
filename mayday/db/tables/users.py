import time

from sqlalchemy import BIGINT, BOOLEAN, INT, Column, String, Table
from sqlalchemy.sql.expression import select, text

from mayday.db.tables import BaseModel


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
            Column('is_banned', BOOLEAN, default=False),
            Column('is_admin', BOOLEAN, default=False),
            Column('created_at', BIGINT),
            Column('updated_at', BIGINT)
        )
        super().__init__(engine, metadata, table, role)

    def _update_user(self, user_profile):
        user_profile['updated_at'] = int(time.time())
        stmt = text(
            'UPDATE users SET username=\'{username}\', first_name=\'{first_name}\', last_name=\'{last_name}\', updated_at={updated_at} WHERE user_id = {user_id}'
            .format_map(user_profile))
        return self.execute(stmt)

    def _set_new_user(self, user_profile):
        user_profile['created_at'] = int(time.time())
        return self.raw_insert(user_profile)

    def _get_user(self, user_profile):
        stmt = select([self.table.c.is_banned, self.table.c.is_admin]).where(
            self.table.c.user_id == user_profile['user_id'])
        row = self.execute(stmt).fetchone()
        if row:
            return dict(zip(['is_banned', 'is_admin'], row))
        return None

    def get_user_profile(self, user_profile):
        stmt = select(['*']).where(self.table.c.user_id == user_profile['user_id'])
        row = self.execute(stmt).fetchone()
        if row:
            return dict(zip([col.key for col in self.table.columns], row))
        return None

    def get_auth(self, user_profile):
        # check isExisted and blacklist
        auth_result = self._get_user(user_profile)
        if auth_result is None:
            self._set_new_user(user_profile)
            auth_result = self._get_user(user_profile)
        # update lastest login time
        self._update_user(user_profile)
        return auth_result

    def ban_user(self, user_profile):
        stmt = text('UPDATE users SET is_banned = 1 WHERE user_id = {user_id};'.format_map(user_profile))
        self.execute(stmt)
        return self._get_user(user_profile)
