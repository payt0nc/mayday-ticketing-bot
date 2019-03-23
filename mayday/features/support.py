from mayday import MONGO_CONTROLLER
from mayday.constants import conversations, stages
from mayday.constants.replykeyboards import KEYBOARDS
from mayday.helpers import QueryHelper
from mayday.helpers.feature_helpers import sp_events_helper
from mayday.objects import User
from telegram.ext.dispatcher import run_async

query_helper = QueryHelper(MONGO_CONTROLLER)


@run_async
def list_events(bot, update, *args, **kwargs):
    user = User(telegram_user=update.effective_user)
    message = update.callback_query.message
    events = query_helper.list_all_events()
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
            reply_markup=sp_events_helper.generate_keyboard(events)
        )
    else:
        bot.edit_message_text(
            text=conversations.SUPPORT_NONE_EVENTS,
            chat_id=user.user_id,
            message_id=message.message_id,
            reply_markup=KEYBOARDS.return_main_panal
        )
    return stages.SUPPORT_EVENT_LIST
