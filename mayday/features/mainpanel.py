import time

from telegram.ext.dispatcher import run_async
from telegram.parsemode import ParseMode

import mayday
from mayday.constants import conversations, stages
from mayday.constants.replykeyboards import KEYBOARDS
# from mayday.features import (platform_stats, post_ticket, quick_search, search, support, update_ticket)
from mayday.features import (post_ticket, quick_search, search, support,
                             update_ticket)
from mayday.helpers.auth_helper import AuthHelper
from mayday.objects.user import User

AUTH_HELPER = AuthHelper(mayday.MONGO_CONTROLLER)
logger = mayday.get_default_logger('main_panel')


@run_async
def start(bot, update, user_data, chat_data):
    user = User(telegram_user=update.effective_user)
    if user.is_username_blank():
        update.message.reply_text(conversations.MAIN_PANEL_USERNAME_MISSING)
        return stages.END

    access_pass = AUTH_HELPER.auth(user)
    if access_pass['is_admin']:
        pass

    elif access_pass['is_blacklist']:
        update.message.reply_text(conversations.MAIN_PANEL_YELLOWCOW)
        return stages.END

    else:
        update.message.reply_text(conversations.MAIN_PANEL_REMINDER)
        time.sleep(0.5)
        bot.sendMessage(
            chat_id=update.message.chat.id,
            text=conversations.MAIN_PANEL_START.format_map(user.to_dict()),
            reply_markup=KEYBOARDS.actions_keyboard_markup)
    return stages.MAIN_PANEL


@run_async
def route(bot, update, user_data, chat_data):
    callback_data = update.callback_query.data
    if callback_data == 'info':
        return info(bot, update, user_data, chat_data)

    if callback_data == 'events':
        return support.list_events(bot, update, user_data)

    if callback_data == 'my_ticket':
        return update_ticket.start(bot, update, user_data)

    if callback_data == 'post':
        return post_ticket.start(bot, update, user_data)

    if callback_data == 'search':
        return search.start(bot, update, user_data)

    if callback_data == 'quick_search':
        return quick_search.start(bot, update, user_data)

    if callback_data == 'bye':
        return done(bot, update, user_data, chat_data)


@run_async
def info(bot, update, *args, **kwargs):
    user = User(telegram_user=update.effective_user)
    bot.send_photo(
        chat_id=user.user_id,
        photo=conversations.OFFICIAL_POSTER,
        caption=conversations.INFO,
        parse_mode=ParseMode.MARKDOWN)
    time.sleep(0.5)
    bot.send_photo(
        chat_id=user.user_id,
        photo=conversations.SEATING_PLAN,
        parse_mode=ParseMode.MARKDOWN)
    time.sleep(0.5)
    bot.sendMessage(
        chat_id=user.user_id,
        text=conversations.MAIN_PANEL_START.format_map(user.to_dict()),
        reply_markup=KEYBOARDS.actions_keyboard_markup)
    return stages.MAIN_PANEL


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
    bot.edit_message_text(
        chat_id=update.callback_query.message.chat.id,
        message_id=update.callback_query.message.message_id,
        text=conversations.MAIN_PANEL_TIMEOUT)
    return stages.END


@run_async
def timeout(bot, update, *args, **kwargs):
    try:
        chat_id = update.callback_query.message.chat.id
    except Exception:
        chat_id = update.message.chat.id
    bot.edit_message_text(
        chat_id=chat_id,
        message_id=update.callback_query.message.message_id,
        text=conversations.MAIN_PANEL_TIMEOUT)
    return stages.END
