import time

from sqlalchemy import BIGINT, INT, SMALLINT, Column, String, Table
from sqlalchemy.sql.expression import and_, desc, select, text

from mayday.db import sqls as SQL
from mayday.db.tables import BaseModel, MagicJSON
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
            Column('status', SMALLINT),
            Column('wish_dates', MagicJSON),
            Column('wish_price_ids', MagicJSON),
            Column('wish_quantities', MagicJSON),
            Column('user_id', BIGINT),
            Column('username', String),
            Column('remarks', String),
            Column('created_at', INT),
            Column('updated_at', INT)
        )
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
    def _trim_where_stmt(conditions: dict):
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

    def get_ticket_by_ticket_id(self, ticket_id: int):
        table = self.table
        stmt = select([
            table.c.id,
            table.c.category,
            table.c.date,
            table.c.price_id,
            table.c.quantity,
            table.c.section,
            table.c.row,
            table.c.status,
            table.c.wish_dates,
            table.c.wish_price_ids,
            table.c.wish_quantities,
            table.c.user_id,
            table.c.username,
            table.c.remarks,
            table.c.updated_at,
        ]) \
            .where(and_(table.c.id == ticket_id)) \
            .order_by(desc(table.c.updated_at))
        row = self.execute(stmt).fetchone()
        if row:
            return dict(
                id=row.id,
                category=row.category,
                date=row.date,
                price_id=row.price_id,
                quantity=row.quantity,
                section=row.section,
                row=row.row,
                status=row.status,
                wish_dates=row.wish_dates,
                wish_price_ids=row.wish_price_ids,
                wish_quantities=row.wish_quantities,
                user_id=row.user_id,
                username=row.username,
                remarks=row.remarks,
                updated_at=row.updated_at
            )
        return None

    def get_tickets_by_user_id(self, user_id: int):
        table = self.table
        stmt = select([
            table.c.id,
            table.c.category,
            table.c.date,
            table.c.price_id,
            table.c.quantity,
            table.c.section,
            table.c.row,
            table.c.status,
            table.c.wish_dates,
            table.c.wish_price_ids,
            table.c.wish_quantities,
            table.c.user_id,
            table.c.username,
            table.c.remarks,
            table.c.updated_at,
        ]) \
            .where(and_(table.c.user_id == user_id)) \
            .order_by(desc(table.c.updated_at))
        cursor = self.execute(stmt)
        row = cursor.fetchone()
        while row:
            yield dict(
                id=row.id,
                category=row.category,
                date=row.date,
                price_id=row.price_id,
                quantity=row.quantity,
                section=row.section,
                row=row.row,
                status=row.status,
                wish_dates=row.wish_dates,
                wish_price_ids=row.wish_price_ids,
                wish_quantities=row.wish_quantities,
                user_id=row.user_id,
                username=row.username,
                remarks=row.remarks,
                updated_at=row.updated_at
            )
            row = cursor.fetchone()

    def get_tickets_by_conditions(self, conditions: dict):
        stmt = text(SQL.SEARCH_BY_CONDITIONS.format(self._trim_where_stmt(conditions)))
        cursor = self.execute(stmt)
        row = cursor.fetchone()
        while row:
            yield dict(zip(SQL.SEARCH_BY_CONDITIONS_KEYS, row))
            row = cursor.fetchone()

    def get_ticket_stats(self):
        status_distribution = self.execute(text(SQL.STATUS_DISRIBUTION)).fetchall()
        ticket_distribution = self.execute(text(SQL.TICKET_DISTRIBUTION)).fetchall()
        return {
            'status_distribution': [dict(zip(SQL.STATUS_DISRIBUTION_KEYS, item)) for item in status_distribution],
            'ticket_distribution': [dict(zip(SQL.TICKET_DISTRIBUTION_KEYS, item)) for item in ticket_distribution],
            'updated_at': int(time.time())
        }

    def get_matched_wish_tickets(self, user_id: int):
        stmt = text(SQL.MATCHING_TICKETS.format_map({'user_id': user_id, 'year': THIS_YEAR}))
        cursor = self.execute(stmt)
        row = cursor.fetchone()
        while row:
            yield dict(zip(SQL.MATCHING_TICKETS_KEYS, row))
            row = cursor.fetchone()

    def create_ticket(self, ticket: dict):
        return self.raw_insert(ticket)

    def update_ticket(self, ticket_id: int, ticket: dict):
        stmt = text(SQL.UPDATE_TICKET.format(self._trim_ticket_tuple(ticket), ticket_id))
        self.execute(stmt)
