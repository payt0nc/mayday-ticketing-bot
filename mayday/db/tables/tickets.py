import time

from sqlalchemy import BIGINT, BOOLEAN, INT, SMALLINT, Column, String, Table
from sqlalchemy.sql.expression import and_, desc, select, text

from mayday.db import sqls as SQL
from mayday.db.tables import BaseModel, MagicJSON

THIS_YEAR = 2019


class Tickets(BaseModel):

    def __init__(self, engine, metadata, role='reader'):
        table = Table(
            'tickets',
            metadata,
            Column('id', INT, primary_key=True, autoincrement=True),
            Column('category_id', SMALLINT),
            Column('date', INT),
            Column('price_id', INT),
            Column('quantity', SMALLINT),
            Column('section', String),
            Column('row', String),
            Column('status_id', SMALLINT),
            Column('wish_date', MagicJSON),
            Column('wish_price_id', MagicJSON),
            Column('wish_quantity', MagicJSON),
            Column('user_id', BIGINT),
            Column('username', String),
            Column('remarks', String),
            Column('updated_at', INT),
            Column('year', INT, default=THIS_YEAR)
        )
        super().__init__(engine, metadata, table, role)

    @staticmethod
    def _trim_ticket_tuple(ticket: dict):
        values = ['year={}'.format(THIS_YEAR)]
        for key, value in ticket.items():
            if value:
                if key == 'status':
                    values.append('status_id = {}'.format(value))
                elif key == 'category_id':
                    values.append('category_id = {}'.format(value))
                elif key in ['section', 'row', 'remarks', 'wish_date', 'wish_price_id', 'wish_quantity']:
                    values.append('{} = \'{}\''.format(key, value))
                elif key not in ['updated_at', 'user_id', 'username']:
                    values.append('{} = {}'.format(key, value))
        return ','.join(values)

    @staticmethod
    def _trim_where_stmt(conditions: dict):
        conds = ['year = {}'.format(THIS_YEAR)]
        for key, value in conditions.items():
            if value:
                if key == 'status':
                    conds.append('status_id = {}'.format(value))

                if key == 'category_id':
                    conds.append('category_id = {}'.format(value))

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
            table.c.category_id,
            table.c.date,
            table.c.price_id,
            table.c.quantity,
            table.c.section,
            table.c.row,
            table.c.status_id,
            table.c.wish_date,
            table.c.wish_price_id,
            table.c.wish_quantity,
            table.c.user_id,
            table.c.username,
            table.c.remarks,
            table.c.updated_at,
        ]) \
            .where(and_(table.c.id == ticket_id, table.c.year == THIS_YEAR)) \
            .order_by(desc(table.c.updated_at))
        row = self.execute(stmt).fetchone()
        if row:
            return dict(
                id=row.id,
                category_id=row.category_id,
                date=row.date,
                price_id=row.price_id,
                quantity=row.quantity,
                section=row.section,
                row=row.row,
                status_id=row.status_id,
                wish_date=row.wish_date,
                wish_price_id=row.wish_price_id,
                wish_quantity=row.wish_quantity,
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
            table.c.category_id,
            table.c.date,
            table.c.price_id,
            table.c.quantity,
            table.c.section,
            table.c.row,
            table.c.status_id,
            table.c.wish_date,
            table.c.wish_price_id,
            table.c.wish_quantity,
            table.c.user_id,
            table.c.username,
            table.c.remarks,
            table.c.updated_at,
        ]) \
            .where(and_(table.c.user_id == user_id, table.c.year == THIS_YEAR)) \
            .order_by(desc(table.c.updated_at))
        cursor = self.execute(stmt)
        row = cursor.fetchone()
        while row:
            yield dict(
                id=row.id,
                category_id=row.category_id,
                date=row.date,
                price_id=row.price_id,
                quantity=row.quantity,
                section=row.section,
                row=row.row,
                status_id=row.status_id,
                wish_date=row.wish_date,
                wish_price_id=row.wish_price_id,
                wish_quantity=row.wish_quantity,
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
