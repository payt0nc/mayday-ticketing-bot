import json
import logging
import os

from google.cloud import logging as stackdriver_logging
from google.oauth2 import service_account

# credentials = service_account.Credentials.from_service_account_file(os.environ['GOOGLE_APPLICATION_CREDENTIALS'])
# scoped_credentials = credentials.with_scopes(['https://www.googleapis.com/auth/cloud-platform'])
STACKDRIVER_CLIENT = stackdriver_logging.Client()


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


def get_log_level():
    return logging.INFO if os.environ.get('STAGE', 'TEST').upper() == 'PRODUCTION' else logging.DEBUG


def console_handler() -> logging.Handler:
    handler = logging.StreamHandler()
    handler.setFormatter(json_formatter())
    return handler


def stackdriver_logger(logger_name: str) -> logging.Logger:
    handler = STACKDRIVER_CLIENT.get_default_handler()
    cloud_logger = logging.getLogger(logger_name)
    cloud_logger.setLevel(logging.INFO)
    cloud_logger.addHandler(handler)
    return cloud_logger


ROOT_LOGGER = logging.getLogger()
ROOT_LOGGER.setLevel(get_log_level())
ROOT_LOGGER.addHandler(console_handler())

AUTH_LOGGER = stackdriver_logger('auth_log')
EVENT_LOGGER = stackdriver_logger('event_log')
