import time

import mayday
import telegram
from mayday.config import AUTH_LOGGER as auth_logger
from mayday.config import EVENT_LOGGER as event_logger
from mayday.config import ROOT_LOGGER as logger
from mayday.constants import conversations, stages
from mayday.constants.replykeyboards import KEYBOARDS
from mayday.controllers.redis import RedisController
from mayday.db.tables.users import UsersModel
from mayday.features import search
from mayday.helpers.auth_helper import AuthHelper
from mayday.helpers.feature_helpers.quick_search_helper import QuickSearchHelper
from mayday.objects.user import User
from telegram import chataction
from telegram.ext.dispatcher import run_async

auth_helper = AuthHelper(UsersModel(mayday.engine, mayday.metadata, role='writer'))
quick_search_helper = QuickSearchHelper('quick_search')
redis = RedisController(redis_conection_pool=mayday.FEATURE_REDIS_CONNECTION_POOL)


@run_async
def start(bot, update, *args, **kwargs):
    user = User(telegram_user=update.effective_user)
    redis.clean_all(user.user_id, 'start')

    if user.is_username_blank():
        update.message.reply_text(conversations.MAIN_PANEL_USERNAME_MISSING)
        return stages.END

    access_pass = auth_helper.auth(user)
    if access_pass['is_admin']:
        pass

    elif access_pass['is_blacklist']:
        update.message.reply_text(conversations.MAIN_PANEL_YELLOWCOW)
        return stages.END

    update.message.reply_text(conversations.MAIN_PANEL_REMINDER)
    time.sleep(0.3)

    bot.send_message(
        text=conversations.QUICK_SEARCH_START,
        chat_id=user.user_id,
        reply_markup=KEYBOARDS.quick_search_start_keyboard_markup,
        parse_mode=telegram.ParseMode.MARKDOWN)
    return stages.QUICK_SEARCH_MODE_SELECTION


@run_async
def select_mode(bot, update, *args, **kwargs):
    user = User(telegram_user=update.effective_user)
    callback_data = update.callback_query.data
    message = update.callback_query.message

    if callback_data == 'cached_condition':
        return search.quick_search_start(bot, update, *args, **kwargs)

    if callback_data == 'matching_my_ticket':
        if auth_helper.auth(user)['is_blacklist']:
            update.message.reply_text(conversations.MAIN_PANEL_YELLOWCOW)
            return stages.END

        bot.send_chat_action(chat_id=user.user_id, action=chataction.ChatAction.TYPING)

        tickets = quick_search_helper.match_my_tickets(user.user_id)
        if tickets and len(tickets) <= 25:
            bot.send_message(
                text=conversations.SEARCH_WITH_RESULTS,
                chat_id=user.user_id,
                message_id=message.message_id)
            for trait in quick_search_helper.split_tickets_traits(tickets):
                bot.send_message(
                    text=quick_search_helper.tickets_tostr(trait, conversations.TICKET),
                    chat_id=user.user_id,
                    message_id=message.message_id)
                time.sleep(0.2)
        elif len(tickets) > 25:
            bot.edit_message_text(
                text=conversations.SEARCH_TOO_MUCH_TICKETS,
                chat_id=user.user_id,
                message_id=message.message_id)
            time.sleep(0.2)
        else:
            bot.edit_message_text(
                text=conversations.SEARCH_WITHOUT_TICKETS,
                chat_id=user.user_id,
                message_id=message.message_id)
            time.sleep(0.2)
        bot.send_message(
            text=conversations.QUICK_SEARCH_START,
            chat_id=user.user_id,
            message_id=update.callback_query.message.message_id,
            reply_markup=KEYBOARDS.quick_search_start_keyboard_markup,
            parse_mode=telegram.ParseMode.MARKDOWN)
        return stages.QUICK_SEARCH_MODE_SELECTION
