import json
import logging
import os

import redis
from mayday.db.tables import create_engine_and_metadata
from mayday.db.tables.tickets import TicketsModel
from mayday.db.tables.users import UsersModel
from sqlalchemy import create_engine

# Application Setting
STAGE = os.environ.get('STAGE', 'TEST').upper()
TELEGRAM_API_CONFIG = dict(
    token=os.environ['TELEGRAM_TOKEN'],
    workers=int(os.environ.get('TELEGRAM_WORKERS', 4)),
    subscribe_channel_name='@{}'.format(os.environ['TELEGRAM_CHANNEL_NAME']),
    read_timeout=int(os.environ.get('TELEGRAM_READ_TIMEOUT', 30)),
    connection_timeout=int(os.environ.get('TELEGRAM_CONNECTION_TIMEOUT', 60)),
    polling_timeout=int(os.environ.get('TELEGRAM_POLLING_TIMEOUT', 20)),
    read_latency=int(os.environ.get('TELEGRAM_READ_LATENCY', 2)))

FEATURE_REDIS_CONNECTION_POOL = redis.ConnectionPool(
    host=os.environ.get('REDIS_HOST', 'localhost'),
    port=os.environ.get('REDIS_PORT', 6379),
    db=1)
CONSTANTS_REDIS_CONNECTION_POOL = redis.ConnectionPool(
    host=os.environ.get('REDIS_HOST', 'localhost'),
    port=os.environ.get('REDIS_PORT', 6379),
    db=2)

engine, metadata = create_engine_and_metadata(
    host=os.environ['DB_HOST'],
    username=os.environ['DB_USERNAME'],
    passwd=os.environ['DB_PASSWD'],
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
    # return logging.INFO
    return logging.INFO if STAGE == 'PRODUCTION' else logging.DEBUG
