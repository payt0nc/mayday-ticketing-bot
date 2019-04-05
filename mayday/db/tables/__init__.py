import json
import time
from datetime import datetime

import sqlalchemy
from sqlalchemy import types, create_engine
from sqlalchemy.ext.compiler import compiles
from sqlalchemy.schema import MetaData
from sqlalchemy.sql.expression import delete, insert, update


class BaseModel:
    def __init__(self, engine, metadata, table, role='reader'):
        self.engine = engine
        self.metadata = metadata
        self.table = table
        self.role = role

    def execute(self, stmt: str):
        return self.engine.execute(stmt)

    def raw_insert(self, row: dict):
        assert self.role == 'writer'
        row['updated_at'] = int(time.time())
        return self.execute(insert(self.table, row))

    def raw_update(self, where: dict, row: dict):
        assert self.role == 'writer'
        row['updated_at'] = int(time.time())
        return self.execute(update(self.table).where(where).values(row))

    def raw_upsert(self, row: dict):
        assert self.role == 'writer'
        row['updated_at'] = int(time.time())
        return self.execute(Upsert(self.table, row))


def create_engine_and_metadata(host, username, passwd, db_name, port=3306, db_settings=None):
    settings = {
        'max_overflow': -1,
        'pool_size': 8,
        'pool_recycle': 1024,
        'pool_timeout': 300,
        'encoding': 'utf8'
    }

    if db_settings is not None:
        settings.update(db_settings)

    db_connection_str = 'mysql://{username}:{passwd}@{host}:{port}/{db_name}?binary_prefix=True&charset=utf8mb4'.format(
        username=username,
        passwd=passwd,
        host=host,
        port=port,
        db_name=db_name)

    engine = create_engine(db_connection_str, **settings)
    metadata = MetaData(bind=engine)

    return engine, metadata


class Upsert(sqlalchemy.sql.expression.Insert):
    pass


@compiles(Upsert, "mysql")
def mysql_compile_upsert(insert_stmt, compiler, **kwargs):
    preparer = compiler.preparer
    if isinstance(insert_stmt.parameters, list):
        keys = insert_stmt.parameters[0].keys()
    else:
        keys = insert_stmt.parameters.keys()

    insert = compiler.visit_insert(insert_stmt, **kwargs)

    ondup = 'ON DUPLICATE KEY UPDATE'

    updates = ', '.join(
        '{} = VALUES({})'.format(preparer.format_column(c), preparer.format_column(c))
        for c in insert_stmt.table.columns
        if c.name in keys
    )
    upsert = ' '.join((insert, ondup, updates))
    return upsert


@compiles(Upsert, "sqlite")
def sqlite_compile_upsert(insert_stmt, compiler, **kwargs):
    insert = compiler.visit_insert(insert_stmt, **kwargs)
    return insert.replace("INSERT INTO", "INSERT OR REPLACE INTO", 1)


class StringfyJSON(types.TypeDecorator):
    # Stores and retrieves JSON as TEXT.

    @property
    def python_type(self):
        pass

    impl = types.TEXT

    def __init__(self):
        super().__init__()

    def process_literal_param(self, value, dialect):
        return super().process_literal_param(self, value, dialect)

    def process_bind_param(self, value, dialect):
        if value:
            value = json.dumps(value)
        return value

    def process_result_value(self, value, dialect):
        if value:
            value = json.loads(value)
        return value


# TypeEngine.with_variant says "use StringyJSON instead when connecting to 'sqlite'"
MagicJSON = types.JSON().with_variant(StringfyJSON, 'sqlite')
