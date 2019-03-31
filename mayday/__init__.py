import json
import logging
import os

from sqlalchemy import create_engine

from mayday.db.tables import create_engine_and_metadata
from mayday.db.tables.tickets import TicketsModel
from mayday.db.tables.users import UsersModel

# Application Setting
STAGE = os.environ.get('stage', 'TEST').upper()
TELEGRAM_TOKEN = os.environ['TELEGRAM_TOKEN']
SUBSCRIBE_CHANNEL_NAME = '@testHKmayday'

engine, metadata = create_engine_and_metadata(
    host=os.environ.get('DB_HOST', '10.0.1.6'),
    username=os.environ.get('DB_USERNAME', 'root'),
    passwd=os.environ.get('DB_PASSWD', 'test123456'),
    db_name=os.environ.get('DB_NAME', 'mayday'))
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
