import json
import logging
import os

from sqlalchemy import create_engine
from mayday.db.tables import create_engine_and_metadata
from mayday.db.tables.tickets import Tickets as TicketsTable
from mayday.db.tables.users import Users as UsersTable


# Application Setting
STAGE = os.environ.get('stage', 'test').upper()
TELEGRAM_TOKEN = os.environ['TELEGRAM_TOKEN']
SUBSCRIBE_CHANNEL_NAME = '@testHKmayday'

# init mysql db connection
engine, metadata = create_engine_and_metadata(
    host=os.environ.get('DB_HOST', 'localhost'),
    username=os.environ.get('DB_USERNAME', 'root'),
    passwd=os.environ.get('DB_PASSWD', 'test123456'),
    db_name=os.environ.get('DB_NAME', 'mayday'))
if STAGE == 'TEST':
    engine = create_engine('sqlite:///:memory:')
TICKETS_TABLE = TicketsTable(engine, metadata, role='writer')
USERS_TABLE = UsersTable(engine, metadata, role='writer')


# Log Configurate

def json_formatter() -> logging.Formatter:
    log_json_format = dict(
        ts='%(asctime)s',
        level='%(levelname)s',
        module='%(module)s.%(funcName)s',
        line_num='%(lineno)s',
        message='%(message)s')
    return logging.Formatter(
        fmt=json.dumps(log_json_format, ensure_ascii=False, sort_keys=True),
        datefmt='%Y-%m-%d %H:%M:%S')


def console_handler() -> logging.Handler:
    handler = logging.StreamHandler()
    handler.setFormatter(json_formatter())
    return handler


def get_log_level():
    return logging.INFO if STAGE == 'PRODUCTION' else logging.DEBUG
