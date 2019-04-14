import time

import mayday
<<<<<<< HEAD
=======
from mayday.config import AUTH_LOGGER as auth_logger
>>>>>>> 589487b7c59176c1e1cd4bd9d287bafb4b3f94b3
from mayday.config import EVENT_LOGGER as event_logger
from mayday.config import ROOT_LOGGER as logger
from mayday.constants import TICKET_MAPPING, conversations, stages
from mayday.constants.replykeyboards import KEYBOARDS
from mayday.controllers.redis import RedisController
from mayday.db.tables.tickets import TicketsModel
from mayday.db.tables.users import UsersModel
from mayday.helpers.auth_helper import AuthHelper
from mayday.helpers.feature_helpers.search_helper import SearchHelper
from mayday.helpers.feature_helpers.update_helper import UpdateHelper
from mayday.helpers.query_helper import QueryHelper
from mayday.helpers.ticket_helper import TicketHelper
from mayday.objects.user import User
from telegram.error import BadRequest
from telegram.ext.dispatcher import run_async

auth_helper = AuthHelper(UsersModel(mayday.engine, mayday.metadata, role='writer'))
query_helper = QueryHelper(TicketsModel(mayday.engine, mayday.metadata, role='writer'))
ticket_helper = TicketHelper(TicketsModel(mayday.engine, mayday.metadata, role='writer'))
search_helper = SearchHelper('search')
update_helper = UpdateHelper(feature='update')
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

    tickets = query_helper.search_by_user_id(user.user_id)
    if tickets:
        bot.send_message(
            text=update_helper.tickets_tostr([ticket.to_human_readable() for ticket in tickets], conversations.TICKET),
            chat_id=user.user_id,
            reply_markup=update_helper.list_tickets_on_reply_keyboard(tickets))
        return stages.UPDATE_SELECT_TICKET
    bot.send_message(chat_id=user.user_id, text=conversations.NONE_RECORD)
    return stages.SEARCH_SELECT_FIELD


@run_async
def select_ticket(bot, update, *args, **kwargs):
    user = User(telegram_user=update.effective_user)
    message = update.callback_query.message
    callback_data = update.callback_query.data

    ticket = query_helper.search_by_ticket_id(ticket_id=callback_data)
    update_helper.save_drafting_ticket(user.user_id, ticket)
    bot.edit_message_text(
        text=conversations.UPDATE_YOURS.format_map(ticket.to_human_readable()),
        chat_id=user.user_id,
        message_id=message.message_id,
        reply_markup=KEYBOARDS.update_ticket_keyboard_markup)
    return stages.UPDATE_SELECT_FIELD


@run_async
def select_field(bot, update, *arg, **kwargs):
    callback_data = update.callback_query.data
    message = update.callback_query.message
    user = User(telegram_user=update.effective_user)
    if not update_helper.save_last_choice(user_id=user.user_id, field=callback_data):
        ticket = update_helper.load_drafting_ticket(ticket_id=callback_data)
        bot.send_message(
            text=conversations.UPDATE_YOURS.format_map(ticket.to_human_readable()),
            chat_id=user.user_id,
            message_id=message.message_id,
            reply_markup=KEYBOARDS.update_ticket_keyboard_markup)
        return stages.UPDATE_SELECT_FIELD

    if callback_data == 'check':
        ticket_in_cache = update_helper.load_drafting_ticket(user_id=user.user_id)
        bot.edit_message_text(
            text=conversations.UPDATE_CHECK.format_map(ticket_in_cache.to_human_readable()),
            chat_id=user.user_id,
            message_id=message.message_id,
            reply_markup=KEYBOARDS.before_submit_post_keyboard_markup)
        return stages.UPDATE_BEFORE_SUBMIT
    else:
        bot.edit_message_text(
            text=conversations.UPDATE_INFO.format_map(dict(message=TICKET_MAPPING.get(callback_data))),
            chat_id=user.user_id,
            message_id=message.message_id,
            reply_markup=KEYBOARDS.conditions_keyboard_mapping.get(callback_data))
        return stages.UPDATE_FILL_VALUE


@run_async
def fill_in_field(bot, update, *args, **kwargs):
    callback_data = update.callback_query.data
    message = update.callback_query.message
    if message:
        user = User(telegram_user=update.effective_user)
        ticket = update_helper.update_cache(user_id=user.user_id, value=callback_data)
        bot.edit_message_text(
            text=conversations.UPDATE_YOURS.format_map(ticket.to_human_readable()),
            chat_id=user.user_id,
            message_id=message.message_id,
            reply_markup=KEYBOARDS.update_ticket_keyboard_markup)
        return stages.UPDATE_SELECT_FIELD
    # FIXME: Why return stage.UPDATE_FILL_VALUE
    return stages.UPDATE_FILL_VALUE


@run_async
def fill_type_in_field(bot, update, *args, **kwargs):
    user = User(telegram_user=update.effective_user)
    ticket = update_helper.update_cache(user_id=user.user_id, value=update.message.text)
    update.message.reply_text(
        text=conversations.UPDATE_YOURS.format_map(ticket.to_human_readable()),
        reply_markup=KEYBOARDS.update_ticket_keyboard_markup)
    return stages.UPDATE_SELECT_FIELD


@run_async
def submit(bot, update, *args, **kwargs):
    callback_data = update.callback_query.data
    user = User(telegram_user=update.effective_user)
    message = update.callback_query.message
    # Kick banned user out!
    if auth_helper.auth(user)['is_blacklist']:
        ticket = update_helper.load_drafting_ticket(user_id=user.user_id)
        ticket_helper.update_ticket(ticket)
        try:
            bot.edit_message_text(
                text=conversations.MAIN_PANEL_YELLOWCOW,
                chat_id=user.user_id,
                message_id=message.message_id)
        except BadRequest:
            bot.send_message(
                text=conversations.MAIN_PANEL_YELLOWCOW,
                chat_id=user.user_id,
                message_id=message.message_id)
        return stages.END

    if callback_data == 'submit':
        try:
            bot.edit_message_text(
                text=conversations.UPDATE_INTO_DB,
                chat_id=user.user_id,
                message_id=message.message_id)
        except BadRequest:
            bot.send_message(
                text=conversations.UPDATE_INTO_DB,
                chat_id=user.user_id,
                message_id=message.message_id)
    return stages.END
