import json
import logging
import time
from itertools import groupby

from sqlalchemy import (BIGINT, INT, JSON, SMALLINT, Boolean, Column, String,
                        Table)
from sqlalchemy.sql.expression import and_, desc, select, text

# from mayday import console_handler, get_log_level
from mayday.db import sqls as SQL
from mayday.db.tables import BaseModel
from mayday.objects.ticket import Ticket

logger = logging.getLogger()
# logger.setLevel(get_log_level())
# logger.addHandler(console_handler())


class TicketsModel(BaseModel):

    def __init__(self, engine, metadata, role='reader'):
        table = Table(
            'tickets',
            metadata,
            Column('id', INT, primary_key=True, autoincrement=True),
            Column('category', SMALLINT),
            Column('date', INT),
            Column('price_id', SMALLINT),
            Column('quantity', SMALLINT),
            Column('section', String(64)),
            Column('row', String(8)),
            Column('seat', String(16)),
            Column('status', SMALLINT),
            Column('source_id', SMALLINT),
            Column('wish_dates', JSON),
            Column('wish_price_ids', JSON),
            Column('wish_quantities', JSON),
            Column('remarks', String(255)),
            Column('is_banned', Boolean, default=False),
            Column('user_id', BIGINT),
            Column('username', String(255)),
            Column('created_at', INT),
            Column('updated_at', INT),
            extend_existing=True)
        super().__init__(engine, metadata, table, role)

    @staticmethod
    def _trim_where_stmt(conditions: dict) -> str:
        conds = []
        for key, value in conditions.items():
            if value:
                if key == 'status':
                    conds.append('status = {}'.format(value))
                if key == 'category':
                    conds.append('category = {}'.format(value))
                if key in ['prices', 'dates', 'quantities']:
                    if isinstance(value, list):
                        conds.append('{} in ({})'.format(
                            dict(prices='price_id', dates='date', quantities='quantity').get(key),
                            ','.join(map(str, value))))
                    else:
                        conds.append('{} = {}'.format(key, value))
        return ' AND '.join(conds)

    def get_tickets_by_date(self, date: int):
        stmt = select(['*']).where(and_(self.table.c.date == date)).order_by(desc(self.table.c.updated_at))
        cursor = self.execute(stmt)
        tickets = list()
        for row in cursor.fetchall():
            ticket = dict()
            for key, value in dict(zip([col.key for col in self.table.columns], row)).items():
                if 'wish' in key and isinstance(value, str):
                    value = json.loads(value)
                ticket[key] = value
            tickets.append(Ticket().to_obj(ticket))
        return tickets

    def get_ticket_by_ticket_id(self, ticket_id: int) -> Ticket:
        stmt = select(['*']).where(and_(self.table.c.id == ticket_id))
        row = self.execute(stmt).fetchone()
        if row:
            ticket = dict()
            for key, value in dict(zip([col.key for col in self.table.columns], row)).items():
                if 'wish' in key and isinstance(value, str):
                    value = json.loads(value)
                ticket[key] = value
            return Ticket().to_obj(ticket)
        return None

    def get_tickets_by_user_id(self, user_id: int) -> list:
        stmt = select(['*']).where(and_(self.table.c.user_id == user_id)).order_by(desc(self.table.c.updated_at))
        cursor = self.execute(stmt)
        tickets = list()
        for row in cursor.fetchall():
            ticket = dict()
            for key, value in dict(zip([col.key for col in self.table.columns], row)).items():
                if 'wish' in key and isinstance(value, str):
                    value = json.loads(value)
                ticket[key] = value
            print(ticket)
            tickets.append(Ticket().to_obj(ticket))
        return tickets

    def get_ticket_by_section(self, section: str) -> list:
        stmt = select(['*']).where(and_(self.table.c.section == section)).order_by(desc(self.table.c.updated_at))
        cursor = self.execute(stmt)
        tickets = list()
        for row in cursor.fetchall():
            ticket = dict()
            for key, value in dict(zip([col.key for col in self.table.columns], row)).items():
                if 'wish' in key and isinstance(value, str):
                    value = json.loads(value)
                ticket[key] = value
            tickets.append(Ticket().to_obj(ticket))
        return tickets

    def get_tickets_by_conditions(self, conditions: dict) -> list:
        stmt = text(SQL.SEARCH_BY_CONDITIONS.format(self._trim_where_stmt(conditions)))
        cursor = self.execute(stmt)
        tickets = list()
        for row in cursor.fetchall():
            ticket = dict()
            for key, value in dict(zip(SQL.SEARCH_BY_CONDITIONS_KEYS, row)).items():
                if 'wish' in key and isinstance(value, str):
                    value = json.loads(value)
                ticket[key] = value
            tickets.append(Ticket().to_obj(ticket))
        return tickets

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
        ticket = ticket.to_dict()
        del ticket['id']
        return bool(self.raw_insert(ticket).rowcount)

    def update_ticket(self, ticket: Ticket) -> bool:
        return bool(self.raw_update(self.table.c.id == ticket.id, ticket.to_dict()).rowcount)

    @staticmethod
    def transform_tickets_stats(ticket_stats: dict) -> dict:
        status_distribution = dict()
        for distribution in ticket_stats['status_distribution']:
            status_distribution[distribution['status']] = distribution['amount']

        ticket_result = dict()
        for category, stats in groupby(ticket_stats['ticket_distribution'], key=lambda x: x['category']):
            ticket_result[category] = dict()
            for price_id, date_amount in groupby(stats, key=lambda x: x['price_id']):
                for item in date_amount:
                    if price_id not in ticket_result[category].keys():
                        ticket_result[category][price_id] = dict()
                    ticket_result[category][price_id].update({item['date']: item['amount']})

        return dict(
            ticket_distribution=ticket_result,
            status_distribution=status_distribution,
            updated_at=ticket_stats['updated_at']
        )
