import time
import traceback

import telegram
from telegram.ext.dispatcher import run_async

from mayday import LogConfig
from mayday.constants import conversations, stages
from mayday.constants.replykeyboards import ReplyKeyboards
from mayday.controllers.redis import RedisHelper
from mayday.features import (platform_stats, post_ticket, quick_search, search,
                             support, update_ticket)
from mayday.utils import log_util
from mayday.validators import authenticator

flogger = LogConfig.flogger
KEYBOARDS = ReplyKeyboards()
REDIS = RedisHelper()


@run_async
def start(bot, update, user_data, chat_data):
    try:
        telegram_info = update._effective_user
        auth = authenticator.auth(telegram_info)
        flogger.info('user: {}, username:{}, auth:{}'.format(telegram_info.id, telegram_info.username, auth))

        if auth.is_username_valid is False:
            msg = log_util.get_ub_log(
                user_id=telegram_info.id,
                username=telegram_info.username,
                funcname=__name__,
                callback_data='auth',
                error='username is missing'
            )
            flogger.warning(msg)
            update.message.reply_text(conversations.MAIN_PANEL_USERNAME_MISSING)
            return stages.END

        if auth.is_admin:
            # TODO: Add Admin Panel
            pass

        if auth.is_banned:
            msg = log_util.get_ub_log(
                user_id=telegram_info.id,
                username=telegram_info.username,
                funcname=__name__,
                callback_data='auth',
                error='banned'
            )
            flogger.warning(msg)
            update.message.reply_text(conversations.MAIN_PANEL_YELLOWCOW)
            return stages.END

        if auth.status:
            msg = log_util.get_ub_log(
                user_id=telegram_info.id,
                username=telegram_info.username,
                funcname=__name__,
                callback_data='auth',
            )
            flogger.info(msg)
            update.message.reply_text(conversations.MAIN_PANEL_REMINDER)
            time.sleep(0.5)
            bot.sendMessage(
                chat_id=update.message.chat.id,
                text=conversations.MAIN_PANEL_START.format_map({'username': telegram_info.username}),
                reply_markup=KEYBOARDS.actions_keyboard_markup
            )
            return stages.MAIN_PANEL
    except Exception:
        msg = log_util.get_ub_log(
            user_id=telegram_info.id,
            username=telegram_info.username,
            funcname=__name__,
            callback_data='start',
            extra=str(update),
            trace_back=str(traceback.format_exc())
        )
        flogger.error(msg)


@run_async
def route(bot, update, user_data, chat_data):
    try:
        telegram_info = update._effective_user
        callback_data = update.callback_query.data
        flogger.info("user_data: {}, update: {}".format(user_data, update))

        msg = log_util.get_ub_log(
            user_id=telegram_info.id,
            username=telegram_info.username,
            funcname=__name__,
            callback_data=callback_data,
        )
        flogger.info(msg)

        if callback_data == 'info':
            telegram_info = update._effective_user
            bot.edit_message_text(
                text=conversations.INFO,
                chat_id=telegram_info.id,
                message_id=update.callback_query.message.message_id,
                reply_markup=KEYBOARDS.actions_keyboard_markup
            )
            return stages.MAIN_PANEL

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

        if callback_data == 'bye':
            done(bot, update, user_data, chat_data)
            return stages.END
    except Exception:
        msg = log_util.get_ub_log(
            user_id=telegram_info.id,
            username=telegram_info.username,
            funcname=__name__,
            callback_data='done',
            extra=str(update),
            trace_back=str(traceback.format_exc())
        )
        flogger.error(msg)


@run_async
def done(bot, update, user_data, chat_data):
    telegram_info = update._effective_user
    try:
        chat_id = update.callback_query.message.chat.id
    except Exception:
        chat_id = update.message.chat.id

    try:
        flogger.info(log_util.get_ub_log(
            user_id=telegram_info.id,
            username=telegram_info.username,
            funcname=__name__,
            callback_data='done'))
        bot.sendPhoto(
            chat_id=chat_id,
            photo=REDIS.direct_read('MAYDAY-BOT-CONFIG-GOODBYE_PHOTO_ID'),
            caption=conversations.MAIN_PANEL_DONE)
        return stages.END
    except Exception:
        bot.sendPhoto(
            chat_id=chat_id,
            photo=REDIS.direct_read('MAYDAY-BOT-CONFIG-GOODBYE_PHOTO_URL'),
            caption=conversations.MAIN_PANEL_DONE)
        msg = log_util.get_ub_log(
            user_id=telegram_info.id,
            username=telegram_info.username,
            funcname=__name__,
            callback_data='done_catch_miss',
            extra=str(update),
            trace_back=str(traceback.format_exc()))
        flogger.warning(msg)
        return stages.END


@run_async
def error(bot, update, error):
    # TODO: Amend the log format
    flogger.error('Update "%s" caused error "%s"' % (update, error))


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

    try:
        telegram_info = update._effective_user
        msg = log_util.get_ub_log(
            user_id=telegram_info.id,
            username=telegram_info.username,
            funcname=__name__,
            callback_data='timeout'
        )
        flogger.info(msg)
        bot.edit_message_text(
            chat_id=chat_id,
            message_id=update.callback_query.message.message_id,
            text=conversations.MAIN_PANEL_TIMEOUT)
        return stages.END

    except Exception:
        msg = log_util.get_ub_log(
            user_id=telegram_info.id,
            username=telegram_info.username,
            funcname=__name__,
            callback_data='timeout',
            extra=str(update)
        )
        flogger.warning(msg)
        bot.sendMessage(
            chat_id=chat_id,
            text=conversations.MAIN_PANEL_TIMEOUT
        )
        return stages.END
