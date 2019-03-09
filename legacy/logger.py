import json
import logging
import logging.config
from logging.handlers import TimedRotatingFileHandler


class LogConfig:

    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)

    json_format = {
        'ts': '%(asctime)s',
        'level': '%(levelname)s',
        'module': '%(module)s.%(funcName)s',
        'line_num': '%(lineno)s',
        'message': '%(message)s'
    }
    formatter = logging.Formatter(
        fmt=json.dumps(json_format, ensure_ascii=False, sort_keys=True),
        datefmt='%Y-%m-%d %H:%M:%S')

    # File
    file_handler = TimedRotatingFileHandler(
        '/data/log/bot/bot.log',
        when='h',
        interval=1,
        encoding='UTF-8',
        utc=True
    )
    file_handler.setFormatter(formatter)

    # Root Log File
    root_file_handler = TimedRotatingFileHandler(
        '/data/log/bot/root.log',
        when='h',
        interval=1,
        encoding='UTF-8',
        utc=True
    )
    root_file_handler.setFormatter(formatter)

    # Console
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    logger.addHandler(console_handler)
    logger.addHandler(root_file_handler)


class TicketValidatorConfig:
    category_values = range(1, 3)
    date_values = [504, 505, 506, 511, 512]
    date_values = range(1, 6)
    price_values = range(1, 6)
    status_values = range(1, 5)
    quantity_values = range(1, 5)
