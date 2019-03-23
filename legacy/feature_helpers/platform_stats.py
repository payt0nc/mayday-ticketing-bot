import traceback

import telegram
from telegram.ext.dispatcher import run_async

import mayday
from mayday.constants import conversations, stages
from mayday.constants.replykeyboards import ReplyKeyboards
from mayday.objects import User


KEYBOARDS = ReplyKeyboards()
logger = mayday.get_default_logger('platform_stats')


@run_async
def stats(bot, update, user_data):
    user = User(update._effective_user)
    message = update.callback_query.message
    # stmt = pf_helper.get_stat()

    if callback_data == 'mainpanel':
        bot.edit_message_text(
            chat_id=user.user_id,
            message_id=message.message_id,
            text=conversations.MAIN_PANEL_START.format_map({'username': telegram_info.username}),
            reply_markup=KEYBOARDS.actions_keyboard_markup
        )
        return stages.MAIN_PANEL

    bot.edit_message_text(
        text='',
        chat_id=user.user_id,
        message_id=message.message_id,
        reply_markup=KEYBOARDS.return_main_panal,
        parse_mode=telegram.ParseMode.MARKDOWN
    )
    return stages.TICKET_STAT_LIST
