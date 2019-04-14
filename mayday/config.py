import json
import logging
import os
from logging.handlers import RotatingFileHandler

from google.cloud import logging as stackdriver_logging
<<<<<<< HEAD
from google.cloud.logging.handlers import CloudLoggingHandler

=======
>>>>>>> 589487b7c59176c1e1cd4bd9d287bafb4b3f94b3

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
<<<<<<< HEAD
    return logging.INFO
    # return logging.INFO if os.environ.get('STAGE', 'TEST').upper() == 'PRODUCTION' else logging.DEBUG
=======
    return logging.INFO if os.environ.get('STAGE', 'TEST').upper() == 'PRODUCTION' else logging.DEBUG
>>>>>>> 589487b7c59176c1e1cd4bd9d287bafb4b3f94b3


def console_handler() -> logging.Handler:
    handler = logging.StreamHandler()
    formatter = logging.Formatter('%(asctime)s\t%(levelname)s\t%(module)s.%(funcName)s\t%(lineno)s\t%(message)s')
    handler.setFormatter(formatter)
    return handler


<<<<<<< HEAD
def file_rotate_handler(logger_name: str, log_home='log', log_filename=None) -> RotatingFileHandler:
    filepath = os.path.join(log_home, log_filename) if log_filename else os.path.join(log_home, logger_name)
    os.makedirs(os.path.dirname(filepath), exist_ok=True)

    handler = RotatingFileHandler(filepath, maxBytes=(64 * 1024 * 1024), backupCount=3)
    handler.setFormatter(json_formatter())
    return handler


def define_file_output_logger(logger_name: str, log_home='log', log_filename=None, level=logging.INFO):
    logger = logging.getLogger(logger_name)
    formatter = logging.Formatter('%(asctime)s\t%(levelname)s\t%(module)s.%(funcName)s\t%(lineno)s\t%(message)s')
    handler = file_rotate_handler(logger_name, log_home, log_filename)
=======
def define_file_output_logger(logger_name: str, log_home='log', log_filename=None, level=logging.INFO):
    logger = logging.getLogger(logger_name)
    filepath = os.path.join(log_home, log_filename) if log_filename else os.path.join(log_home, logger_name)
    os.makedirs(os.path.dirname(filepath), exist_ok=True)

    formatter = logging.Formatter('%(asctime)s\t%(levelname)s\t%(module)s.%(funcName)s\t%(lineno)s\t%(message)s')
    handler = RotatingFileHandler(filepath, maxBytes=(64 * 1024 * 1024), backupCount=3)
>>>>>>> 589487b7c59176c1e1cd4bd9d287bafb4b3f94b3
    handler.setFormatter(formatter)
    handler.setLevel(level)
    logger.addHandler(handler)
    return logger


<<<<<<< HEAD
def stackdriver_logger(logger_name: str, log_home='log', log_filename=None) -> logging.Logger:
    logger = logging.getLogger(logger_name)
    logger.setLevel(logging.INFO)
    logger.addHandler(CloudLoggingHandler(STACKDRIVER_CLIENT))
    logger.addHandler(file_rotate_handler(logger_name, log_home, log_filename))
    # logger.addHandler(console_handler())
    return logger
=======
def stackdriver_logger(logger_name: str) -> logging.Logger:
    handler = STACKDRIVER_CLIENT.get_default_handler()
    cloud_logger = logging.getLogger(logger_name)
    cloud_logger.setLevel(logging.INFO)
    cloud_logger.addHandler(handler)
    return cloud_logger
>>>>>>> 589487b7c59176c1e1cd4bd9d287bafb4b3f94b3


ROOT_LOGGER = logging.getLogger()
ROOT_LOGGER.setLevel(get_log_level())
ROOT_LOGGER.addHandler(console_handler())

AUTH_LOGGER = stackdriver_logger('auth_log')
# AUTH_LOGGER = define_file_output_logger('auth_log', 'auth.log')
EVENT_LOGGER = stackdriver_logger('event_log')
# EVENT_LOGGER = define_file_output_logger('event_log', 'event.log')
