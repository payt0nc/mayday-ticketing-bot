import logging

import mayday
from mayday.constants import conversations, stages
from telegram.ext.dispatcher import run_async

logger = logging.getLogger()
logger.setLevel(mayday.get_log_level())
logger.addHandler(mayday.console_handler())


@run_async
def done(bot, update, *args, **kwargs):
    try:
        chat_id = update.callback_query.message.chat.id
    except Exception:
        chat_id = update.message.chat.id
    bot.sendMessage(chat_id=chat_id, text=conversations.MAIN_PANEL_DONE)
    return stages.END


@run_async
def error(bot, update, error):
    # TODO: Amend the log format
    pass


@run_async
def ask_help(bot, update, *args, **kwargs):
    update.message.reply_text(conversations.MAIN_PANEL_TIMEOUT)
    return stages.END


@run_async
def timeout(bot, update, *args, **kwargs):
    try:
        chat_id = update.callback_query.message.chat.id
    except Exception:
        chat_id = update.message.chat.id
    update.message.reply_text(conversations.MAIN_PANEL_TIMEOUT)
    return stages.END
