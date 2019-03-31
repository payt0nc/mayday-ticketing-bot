import logging

from telegram.ext.dispatcher import run_async

import mayday
from mayday.constants import conversations, stages
from mayday.constants.replykeyboards import KEYBOARDS
from mayday.helpers.feature_helpers.sp_events_helper import EventHelper
from mayday.objects.user import User

logger = logging.getLogger()
logger.setLevel(mayday.get_log_level())
logger.addHandler(mayday.console_handler())

event_helper = EventHelper('events')


@run_async
def list_events(bot, update, *args, **kwargs):
    user = User(telegram_user=update.effective_user)
    message = update.callback_query.message
    events = event_helper.list_all_events()
    callback_data = update.callback_query.data
    if callback_data == 'mainpanel':
        bot.edit_message_text(
            text=conversations.MAIN_PANEL_START.format_map(dict(username=user.username)),
            chat_id=user.user_id,
            message_id=message.message_id,
            reply_markup=KEYBOARDS.actions_keyboard_markup
        )
        return stages.MAIN_PANEL

    if events:
        bot.edit_message_text(
            text=conversations.SUPPORT_LIST_EVENTS,
            chat_id=user.user_id,
            message_id=message.message_id,
            reply_markup=event_helper.generate_keyboard(events)
        )
    else:
        bot.edit_message_text(
            text=conversations.SUPPORT_NONE_EVENTS,
            chat_id=user.user_id,
            message_id=message.message_id,
            reply_markup=KEYBOARDS.return_main_panal
        )
    return stages.SUPPORT_EVENT_LIST
