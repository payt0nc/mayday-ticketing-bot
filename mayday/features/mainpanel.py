import time

import mayday
from mayday.constants import conversations, stages
from mayday.constants.replykeyboards import ReplyKeyboards
# from mayday.features import (platform_stats, post_ticket, quick_search, search, support, update_ticket)
from mayday.helpers import ActionHelper, AuthHelper
from mayday.objects import User
from telegram.ext.dispatcher import run_async

KEYBOARDS = ReplyKeyboards()
AUTH_HELPER = AuthHelper(mayday.MONGO_CONTROLLER)
ACTION_HELPER = ActionHelper(mayday.ACTION_REDIS_CONTROLLER)

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
            reply_markup=KEYBOARDS.actions_keyboard_markup
        )
    return stages.MAIN_PANEL


@run_async
def route(bot, update, user_data, chat_data):
    user = User(telegram_user=update.effective_user)
    callback_data = update.callback_query.data
    if callback_data == 'info':
        bot.edit_message_text(
            text=conversations.INFO,
            chat_id=user.user_id,
            message_id=update.callback_query.message.message_id,
            reply_markup=KEYBOARDS.actions_keyboard_markup)
        return stages.MAIN_PANEL

    '''
    if callback_data == 'post':
        post_ticket.start(bot, update, user_data)
        return stages.POST_SELECT_FIELD

    if callback_data == 'search':
        search.start(bot, update, user_data)
        return stages.SEARCH_SELECT_FIELD

    if callback_data == 'stats':
        platform_stats.stats(bot, update, user_data)
        return stages.TICKET_STAT_LIST

    if callback_data == 'my_ticket':
        update_ticket.start(bot, update, user_data)
        return stages.UPDATE_SELECT_TICKET

    if callback_data == 'events':
        support.start(bot, update, user_data)
        return stages.SUPPORT_EVENT_LIST

    if callback_data == 'quick_search':
        quick_search.start(bot, update, user_data)
        return stages.QUICK_SEARCH_MODE_SELECTION
    '''
    if callback_data == 'bye':
        done(bot, update, user_data, chat_data)
        return stages.END


@run_async
def done(bot, update, user_data, chat_data):
    user = User(telegram_user=update.effective_user)
    try:
        chat_id = update.callback_query.message.chat.id
    except Exception:
        chat_id = update.message.chat.id

    bot.sendMessage(chat_id=update.message.chat.id, text=conversations.MAIN_PANEL_DONE)
    '''
    bot.sendPhoto(
        chat_id=chat_id,
        photo=REDIS.direct_read('MAYDAY-BOT-CONFIG-GOODBYE_PHOTO_ID'),
        caption=conversations.MAIN_PANEL_DONE)
    '''
    return stages.END


@run_async
def error(bot, update, error):
    # TODO: Amend the log format
    pass


@run_async
def help(bot, update):
    bot.edit_message_text(
        chat_id=update.callback_query.message.chat.id,
        message_id=update.callback_query.message.message_id,
        text=conversations.MAIN_PANEL_TIMEOUT)
    return stages.END


@run_async
def timeout(bot, update, chat_data):
    try:
        chat_id = update.callback_query.message.chat.id
    except Exception:
        chat_id = update.message.chat.id
    bot.edit_message_text(
        chat_id=chat_id,
        message_id=update.callback_query.message.message_id,
        text=conversations.MAIN_PANEL_TIMEOUT)
    return stages.END
