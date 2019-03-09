import traceback

import telegram
from telegram.ext.dispatcher import run_async

from mayday.constants import conversations, stages
from mayday.constants.replykeyboards import ReplyKeyboards
from mayday.helpers.feature_helpers.stat_helper import StatHelper

KEYBOARDS = ReplyKeyboards()
pf_helper = StatHelper('stat_help')


@run_async
def stats(bot, update, user_data):
    telegram_info = update._effective_user
    message = update.callback_query.message
    stmt = pf_helper.get_stat()
    bot.edit_message_text(
        text=stmt,
        chat_id=telegram_info.id,
        message_id=message.message_id,
        reply_markup=KEYBOARDS.return_main_panal,
        parse_mode=telegram.ParseMode.MARKDOWN
    )
    return stages.TICKET_STAT_LIST


@run_async
def backward(bot, update, user_data):
    callback_data = update.callback_query.data
    message = update.callback_query.message
    telegram_info = update._effective_user

    if callback_data == 'mainpanel':
        bot.edit_message_text(
            chat_id=telegram_info.id,
            message_id=message.message_id,
            text=conversations.MAIN_PANEL_START.format_map({'username': telegram_info.username}),
            reply_markup=KEYBOARDS.actions_keyboard_markup
        )
        return stages.MAIN_PANEL
