from sqlalchemy import BOOLEAN, INT, Column, String, Table
from sqlalchemy.sql.expression import desc, select

from mayday.db.tables import BaseModel


class EventsModel(BaseModel):

    def __init__(self, engine, metadata, role='reader'):
        table = Table(
            'events',
            metadata,
            Column('id', INT, primary_key=True, autoincrement=True),
            Column('name', String(255)),
            Column('type_id', INT),
            Column('description', String(255)),
            Column('markdown_path', String(255)),
            Column('attachment_hex', String(255)),
            Column('attachment_type', INT),
            Column('is_deleted', BOOLEAN),
            Column('updated_at', INT),
            extend_existing=True)
        super().__init__(engine, metadata, table, role)

    def insert(self, row):
        self.raw_insert(row)

    def list_all_events(self) -> list:
        stmt = select(['*']).where(self.table.c.is_deleted == False).order_by(desc(self.table.c.id))
        cursor = self.execute(stmt)
        events = list()
        row = cursor.fetchone()
        while row:
            events.append(dict(zip([col.key for col in self.table.columns], row)))
            row = cursor.fetchone()
        return events
