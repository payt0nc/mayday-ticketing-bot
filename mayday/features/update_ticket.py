import re

from telegram.ext.dispatcher import run_async

from mayday import MONGO_CONTROLLER
from mayday.constants import TICKET_MAPPING, conversations, stages
from mayday.constants.replykeyboards import KEYBOARDS
from mayday.helpers import AuthHelper, QueryHelper, TicketHelper, UpdateHelper
from mayday.objects import Ticket, User

auth_helper = AuthHelper(MONGO_CONTROLLER)
query_helper = QueryHelper(MONGO_CONTROLLER)
ticket_helper = TicketHelper(MONGO_CONTROLLER)
update_helper = UpdateHelper(feature='update')


@run_async
def start(bot, update, *args, **kwargs):
    user = User(telegram_user=update.effective_user)
    message = update.callback_query.message
    tickets = query_helper.search_by_user_id(user.user_id)
    if tickets:
        bot.edit_message_text(
            text=update_helper.tickets_tostr([ticket.to_human_readable() for ticket in tickets], conversations.TICKET),
            chat_id=user.user_id,
            message_id=message.message_id,
            reply_markup=update_helper.list_tickets_on_reply_keyboard(tickets))
        return stages.UPDATE_SELECT_TICKET
    bot.edit_message_text(
        chat_id=user.user_id,
        message_id=message.message_id,
        text=conversations.NONE_RECORD,
        reply_markup=KEYBOARDS.return_main_panal)
    return stages.MAIN_PANEL


@run_async
def select_ticket(bot, update, *args, **kwargs):
    user = User(telegram_user=update.effective_user)
    callback_data = update.callback_query.data
    if callback_data == 'mainpanel':
        bot.edit_message_text(
            chat_id=user.user_id,
            message_id=update.callback_query.message.message_id,
            text=conversations.MAIN_PANEL_START.format_map(user.to_dict()),
            reply_markup=KEYBOARDS.actions_keyboard_markup)
        return stages.MAIN_PANEL
    ticket = query_helper.search_by_ticket_id(ticket_id=callback_data)
    update_helper.save_drafting_ticket(user.user_id, ticket)
    bot.edit_message_text(
        text=conversations.UPDATE_YOURS.format_map(ticket.to_human_readable()),
        chat_id=user.user_id,
        message_id=update.callback_query.message.message_id,
        reply_markup=KEYBOARDS.update_ticket_keyboard_markup)
    return stages.UPDATE_SELECT_FIELD


@run_async
def select_field(bot, update, *arg, **kwargs):
    callback_data = update.callback_query.data
    message = update.callback_query.message
    user = User(telegram_user=update.effective_user)
    update_helper.save_last_choice(user_id=user.user_id, field=callback_data)
    if callback_data == 'mainpanel':
        bot.edit_message_text(
            chat_id=user.user_id,
            message_id=update.callback_query.message.message_id,
            text=conversations.MAIN_PANEL_START.format_map(user.to_dict()),
            reply_markup=KEYBOARDS.actions_keyboard_markup)
        return stages.MAIN_PANEL
    elif callback_data == 'check':
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
    message = update.callback_query.message
    user = User(telegram_user=update.effective_user)

    if callback_data == 'mainpanel':
        bot.edit_message_text(
            chat_id=user.user_id,
            message_id=update.callback_query.message.message_id,
            text=conversations.MAIN_PANEL_START.format(username=user.username),
            reply_markup=KEYBOARDS.actions_keyboard_markup)
        return stages.MAIN_PANEL

    if callback_data == 'submit':
        # Kick banned user out!
        if auth_helper.auth(user)['is_blacklist']:
            update.message.reply_text(conversations.MAIN_PANEL_YELLOWCOW)
            return stages.END

        ticket = update_helper.load_drafting_ticket(user_id=user.user_id)
        ticket_helper.update_ticket(ticket)
        bot.send_message(
            text=conversations.AND_THEN,
            chat_id=user.user_id,
            message_id=message.message_id,
            reply_markup=KEYBOARDS.after_submit_keyboard)
        return stages.UPDATE_SUBMIT


@run_async
def backward(bot, update, *args, **kwargs):
    callback_data = update.callback_query.data
    message = update.callback_query.message
    user = User(telegram_user=update.effective_user)

    if callback_data == 'mainpanel':
        bot.edit_message_text(
            chat_id=user.user_id,
            message_id=message.message_id,
            text=conversations.MAIN_PANEL_START.format(username=user.username),
            reply_markup=KEYBOARDS.actions_keyboard_markup)
        return stages.MAIN_PANEL
