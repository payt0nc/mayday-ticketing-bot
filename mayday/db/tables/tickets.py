import json
import time

from sqlalchemy import BIGINT, Boolean, INT, SMALLINT, Column, String, Table, JSON
from sqlalchemy.sql.expression import and_, desc, select, text

from mayday.db import sqls as SQL
from mayday.db.tables import BaseModel
from mayday.objects.ticket import Ticket


class Tickets(BaseModel):

    def __init__(self, engine, metadata, role='reader'):
        table = Table(
            'tickets',
            metadata,
            Column('id', INT, primary_key=True, autoincrement=True),
            Column('category', SMALLINT),
            Column('date', INT),
            Column('price_id', SMALLINT),
            Column('quantity', SMALLINT),
            Column('section', String),
            Column('row', String),
            Column('seat', String),
            Column('status', SMALLINT),
            Column('source', String),
            Column('wish_dates', JSON),
            Column('wish_price_ids', JSON),
            Column('wish_quantities', JSON),
            Column('remarks', String),
            Column('is_banned', Boolean, default=False),
            Column('user_id', BIGINT),
            Column('username', String),
            Column('created_at', INT),
            Column('updated_at', INT))
        super().__init__(engine, metadata, table, role)

    @staticmethod
    def _trim_ticket_tuple(ticket: dict):
        values = []
        for key, value in ticket.items():
            if value:
                if key == 'status':
                    values.append('status = {}'.format(value))
                elif key == 'category':
                    values.append('category = {}'.format(value))
                elif key in ['section', 'row', 'remarks', 'wish_dates', 'wish_price_ids', 'wish_quantities']:
                    values.append('{} = \'{}\''.format(key, value))
                elif key not in ['updated_at', 'user_id', 'username']:
                    values.append('{} = {}'.format(key, value))
        return ','.join(values)

    @staticmethod
    def _trim_where_stmt(conditions: dict) -> str:
        conds = []
        for key, value in conditions.items():
            if value:
                if key == 'status':
                    conds.append('status = {}'.format(value))
                if key == 'category':
                    conds.append('category = {}'.format(value))
                if key in ['price_id', 'date', 'quantity']:
                    if isinstance(value, list):
                        conds.append('{} in ({})'.format(key, ','.join(map(str, value))))
                    else:
                        conds.append('{} = {}'.format(key, value))
        return ' AND '.join(conds)

    def get_ticket_by_ticket_id(self, ticket_id: int) -> dict:
        stmt = select(['*']).where(and_(self.table.c.id == ticket_id))
        row = self.execute(stmt).fetchone()
        if row:
            ticket = dict()
            for key, value in dict(zip([col.key for col in self.table.columns], row)).items():
                if 'wish' in key and isinstance(value, str):
                    value = json.loads(value)
                ticket[key] = value
        return Ticket().to_obj(ticket)

    def get_tickets_by_user_id(self, user_id: int):
        table = self.table
        stmt = select(['*']).where(and_(table.c.user_id == user_id)).order_by(desc(table.c.updated_at))
        cursor = self.execute(stmt)
        row = cursor.fetchone()
        while row:
            ticket = dict()
            for key, value in dict(zip([col.key for col in self.table.columns], row)).items():
                if 'wish' in key and isinstance(value, str):
                    value = json.loads(value)
                ticket[key] = value
            yield Ticket().to_obj(ticket)
            row = cursor.fetchone()

    def get_tickets_by_conditions(self, conditions: dict):
        stmt = text(SQL.SEARCH_BY_CONDITIONS.format(self._trim_where_stmt(conditions)))
        cursor = self.execute(stmt)
        row = cursor.fetchone()
        while row:
            yield dict(zip(SQL.SEARCH_BY_CONDITIONS_KEYS, row))
            row = cursor.fetchone()

    def get_ticket_stats(self) -> dict:
        status_distribution = self.execute(text(SQL.STATUS_DISRIBUTION)).fetchall()
        ticket_distribution = self.execute(text(SQL.TICKET_DISTRIBUTION)).fetchall()
        return dict(
            status_distribution=[dict(zip(SQL.STATUS_DISRIBUTION_KEYS, item)) for item in status_distribution],
            ticket_distribution=[dict(zip(SQL.TICKET_DISTRIBUTION_KEYS, item)) for item in ticket_distribution],
            updated_at=int(time.time()))

    def get_matched_wish_tickets(self, user_id: int):
        stmt = text(SQL.MATCHING_TICKETS.format(user_id=user_id))
        cursor = self.execute(stmt)
        row = cursor.fetchone()
        while row:
            yield dict(zip(SQL.MATCHING_TICKETS_KEYS, row))
            row = cursor.fetchone()

    def create_ticket(self, ticket: Ticket):
        return self.raw_insert(ticket.to_dict())

    def update_ticket(self, ticket: Ticket) -> bool:
        return bool(self.raw_update(self.table.c.id == ticket.ticket_id, ticket.to_dict()).rowcount)
