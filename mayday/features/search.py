import logging
import re
import time

import mayday
import telegram
from mayday.config import EVENT_LOGGER as event_logger
from mayday.config import ROOT_LOGGER as logger
from mayday.constants import TICKET_MAPPING, conversations, stages
from mayday.constants.replykeyboards import KEYBOARDS
from mayday.controllers.redis import RedisController
from mayday.db.tables.tickets import TicketsModel
from mayday.db.tables.users import UsersModel
from mayday.helpers.auth_helper import AuthHelper
from mayday.helpers.feature_helpers.search_helper import SearchHelper
from mayday.helpers.query_helper import QueryHelper
from mayday.objects.user import User
from telegram import chataction
from telegram.error import BadRequest
from telegram.ext.dispatcher import run_async

auth_helper = AuthHelper(UsersModel(mayday.engine, mayday.metadata, role='writer'))
query_helper = QueryHelper(TicketsModel(mayday.engine, mayday.metadata, role='writer'))
search_helper = SearchHelper('search')
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

    query = search_helper.reset_cache(user.user_id)
    bot.send_message(
        text=conversations.SEARCH_TICKET_START.format_map(query.to_human_readable()),
        chat_id=user.user_id,
        reply_markup=KEYBOARDS.search_ticket_keyboard_markup)
    return stages.SEARCH_SELECT_FIELD


@run_async
def select_field(bot, update, *args, **kwargs):
    callback_data = update.callback_query.data
    message = update.callback_query.message
    user = User(telegram_user=update.effective_user)
    if not search_helper.save_last_choice(user.user_id, field=callback_data):
        try:
            query = search_helper.load_drafting_query(user.user_id)
        except Exception:
            logger.warning("cache miss")
            query = search_helper.reset_cache(user.user_id)
        bot.send_message(
            text=conversations.SEARCH_TICKET_START.format_map(query.to_human_readable()),
            chat_id=user.user_id,
            reply_markup=KEYBOARDS.search_ticket_keyboard_markup)
        return stages.SEARCH_SELECT_FIELD

    if callback_data == 'check':
        query = search_helper.load_drafting_query(user.user_id)
        check_result = query.validate()
        if check_result['status']:
            bot.edit_message_text(
                text=conversations.SEARCH_CHECK.format_map(query.to_human_readable()),
                chat_id=user.user_id,
                message_id=message.message_id,
                reply_markup=KEYBOARDS.before_submit_search_keyboard_markup,
                parse_mode=telegram.ParseMode.MARKDOWN)
            return stages.SEARCH_BEFORE_SUBMIT
        bot.send_message(
            text=conversations.TYPE_IN_WARNING.format(error_message=check_result['info']),
            chat_id=user.user_id,
            message_id=message.message_id)
        bot.send_message(
            text=conversations.SEARCH_TICKET_START.format_map(query.to_human_readable()),
            chat_id=user.user_id,
            message_id=message.message_id,
            reply_markup=KEYBOARDS.search_ticket_keyboard_markup,
            parse_mode=telegram.ParseMode.MARKDOWN)
        return stages.SEARCH_SELECT_FIELD

    if callback_data == 'reset':
        query = search_helper.reset_cache(user.user_id)
        try:
            bot.edit_message_text(
                text=conversations.SEARCH_TICKET_START.format_map(query.to_human_readable()),
                chat_id=user.user_id,
                message_id=message.message_id,
                reply_markup=KEYBOARDS.search_ticket_keyboard_markup,
                parse_mode=telegram.ParseMode.MARKDOWN)
        except BadRequest:
            bot.send_message(
                text=conversations.SEARCH_TICKET_START.format_map(query.to_human_readable()),
                chat_id=user.user_id,
                message_id=message.message_id,
                reply_markup=KEYBOARDS.search_ticket_keyboard_markup,
                parse_mode=telegram.ParseMode.MARKDOWN)
        return stages.SEARCH_SELECT_FIELD

    bot.edit_message_text(
        text=conversations.SEARCH_TICKET_INFO.format(message=TICKET_MAPPING.get(callback_data)),
        chat_id=user.user_id,
        message_id=message.message_id,
        reply_markup=KEYBOARDS.conditions_keyboard_mapping.get(callback_data))
    return stages.SEARCH_FILL_VALUE


@run_async
def fill_in_field(bot, update, *args, **kwargs):
    callback_data = update.callback_query.data
    message = update.callback_query.message
    user = User(telegram_user=update.effective_user)
    if re.match(r'\d+', callback_data):
        query = search_helper.update_cache(user.user_id, callback_data)
        bot.edit_message_text(
            chat_id=user.user_id,
            message_id=message.message_id,
            text=conversations.SEARCH_TICKET_START.format_map(query.to_human_readable()),
            reply_markup=KEYBOARDS.search_ticket_keyboard_markup,
            parse_mode=telegram.ParseMode.MARKDOWN)
        return stages.SEARCH_SELECT_FIELD

    query = search_helper.load_drafting_query(user.user_id)
    choice = search_helper.load_last_choice(user.user_id)
    bot.sendMessage(chat_id=user.user_id, text=conversations.TYPE_IN_ERROR)
    bot.sendMessage(
        chat_id=user.user_id,
        message_id=message.message_id,
        text=conversations.SEARCH_TICKET_START.format_map(query.to_human_readable()),
        reply_markup=KEYBOARDS.conditions_keyboard_mapping.get(choice),
        parse_mode=telegram.ParseMode.MARKDOWN)
    # FIXME: No Return??


@run_async
def submit(bot, update, *args, **kwargs):
    callback_data = update.callback_query.data
    message = update.callback_query.message
    user = User(telegram_user=update.effective_user)

    if callback_data == 'reset':
        query = search_helper.reset_cache(user.user_id)
        bot.edit_message_text(
            text=conversations.SEARCH_TICKET_START.format_map(query.to_human_readable()),
            chat_id=user.user_id,
            message_id=message.message_id,
            reply_markup=KEYBOARDS.search_ticket_keyboard_markup,
            parse_mode=telegram.ParseMode.MARKDOWN)
        return stages.SEARCH_SELECT_FIELD

    if callback_data == 'back':
        query = search_helper.load_drafting_query(user.user_id)
        bot.edit_message_reply_markup(
            text=conversations.SEARCH_TICKET_START.format_map(query.to_human_readable()),
            chat_id=user.user_id,
            message_id=message.message_id,
            reply_markup=KEYBOARDS.search_ticket_keyboard_markup,
            parse_mode=telegram.ParseMode.MARKDOWN)
        return stages.SEARCH_SELECT_FIELD

    if callback_data == 'quick_search':
        query = search_helper.load_drafting_query(user.user_id)
        query_helper.save_quick_search(query)
        bot.edit_message_text(
            text=conversations.QUICK_SEARCH_INSERT_SUCESS.format_map(query.to_human_readable()),
            chat_id=user.user_id,
            message_id=message.message_id,
            reply_markup=KEYBOARDS.before_submit_post_keyboard_markup)
        return stages.SEARCH_BEFORE_SUBMIT

    if callback_data == 'submit':
        # Kick banned user out!
        if auth_helper.auth(user)['is_blacklist']:
            update.message.reply_text(conversations.MAIN_PANEL_YELLOWCOW)
            return stages.END

        query = search_helper.load_drafting_query(user.user_id)
        bot.send_chat_action(chat_id=user.user_id, action=chataction.ChatAction.TYPING)
        tickets = query_helper.search_by_query(query)

        if (tickets and len(tickets) <= 25):
            bot.edit_message_text(
                text=conversations.SEARCH_WITH_RESULTS,
                chat_id=user.user_id,
                message_id=message.message_id)
            time.sleep(0.2)
            for trait in query_helper.split_tickets_traits(tickets):
                bot.send_message(
                    text=search_helper.tickets_tostr(trait, conversations.TICKET),
                    chat_id=user.user_id,
                    message_id=message.message_id)
                time.sleep(0.2)
            return stages.END
        elif len(tickets) > 25:
            bot.edit_message_text(
                text=conversations.SEARCH_TOO_MUCH_TICKETS,
                chat_id=user.user_id,
                message_id=message.message_id)
            return stages.END
        else:
            bot.edit_message_text(
                text=conversations.SEARCH_WITHOUT_TICKETS,
                chat_id=user.user_id,
                message_id=message.message_id)
            time.sleep(0.2)
            query = search_helper.load_drafting_query(user.user_id)
            bot.send_message(
                text=conversations.SEARCH_TICKET_START.format_map(query.to_human_readable()),
                chat_id=user.user_id,
                message_id=message.message_id,
                reply_markup=KEYBOARDS.search_ticket_keyboard_markup,
                parse_mode=telegram.ParseMode.MARKDOWN)
        return stages.SEARCH_SELECT_FIELD


@run_async
def backward(bot, update, *args, **kwargs):
    callback_data = update.callback_query.data
    message = update.callback_query.message
    user = User(telegram_user=update.effective_user)
    query = search_helper.load_drafting_query(user.user_id)

    if callback_data == 'backward':
        bot.send_message(
            text=conversations.SEARCH_TICKET_START.format_map(query.to_human_readable()),
            chat_id=user.user_id,
            message_id=message.message_id,
            reply_markup=KEYBOARDS.search_ticket_keyboard_markup)
        return stages.SEARCH_SELECT_FIELD
