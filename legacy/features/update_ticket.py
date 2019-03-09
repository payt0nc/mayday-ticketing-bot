import re
import traceback

import telegram
from telegram.ext.dispatcher import run_async

from mayday.constants import TICKET_MAPPING, conversations, stages
from mayday.constants.replykeyboards import ReplyKeyboards
from mayday.controllers.request import RequestHelper
from mayday.helpers.update_helper import UpdateHelper

KEYBOARDS = ReplyKeyboards()
request_helper = RequestHelper()
update_helper = UpdateHelper('update_ticket')


@run_async
def start(bot, update, user_data):
    telegram_info = update._effective_user
    message = update.callback_query.message
    callback_data = update.callback_query.data
    tickets = request_helper.send_search_my_ticket(userid=telegram_info.id)
    if tickets['status'] and tickets['info']:
        tickets = tickets['info']
        ticket_ids = update_helper.extract_ticket_ids(tickets)
        bot.edit_message_text(
            text=update_helper.tickets_tostr(tickets),
            chat_id=telegram_info.id,
            message_id=message.message_id,
            reply_markup=update_helper.list_tickets_on_reply_keyboard(ticket_ids)
        )
        return stages.UPDATE_SELECT_TICKET
    else:
        bot.edit_message_text(
            chat_id=telegram_info.id,
            message_id=message.message_id,
            text=conversations.NONE_RECORD,
            reply_markup=KEYBOARDS.return_main_panal
        )
        return stages.MAIN_PANEL


@run_async
def select_ticket(bot, update, user_data):
    telegram_info = update._effective_user
    callback_data = update.callback_query.data

    if callback_data == 'mainpanel':
        bot.edit_message_text(
            chat_id=telegram_info.id,
            message_id=update.callback_query.message.message_id,
            text=conversations.MAIN_PANEL_START.format_map({'username': telegram_info.username}),
            reply_markup=KEYBOARDS.actions_keyboard_markup
        )
        return stages.MAIN_PANEL

    if re.match(r'\d+', callback_data):
        ticket = request_helper.send_search_ticket_by_ticket_id(ticket_id=callback_data)
        update_helper.set_cache(user_id=telegram_info.id, content=ticket['info'])
        flatten_ticket = update_helper.flatten(ticket['info'])
        bot.edit_message_text(
            text=conversations.UPDATE_YOURS.format_map(flatten_ticket),
            chat_id=telegram_info.id,
            message_id=update.callback_query.message.message_id,
            reply_markup=KEYBOARDS.update_ticket_keyboard_markup
        )
        return stages.UPDATE_SELECT_FIELD


@run_async
def select_field(bot, update, user_data):
    callback_data = update.callback_query.data
    message = update.callback_query.message
    telegram_info = update._effective_user
    update_helper.set_last_choice(user_id=telegram_info.id, content=callback_data)
    if callback_data == 'mainpanel':
        bot.edit_message_text(
            chat_id=telegram_info.id,
            message_id=update.callback_query.message.message_id,
            text=conversations.MAIN_PANEL_START.format_map({'username': telegram_info.username}),
            reply_markup=KEYBOARDS.actions_keyboard_markup
        )
        return stages.MAIN_PANEL
    elif callback_data == 'check':
        ticket = update_helper.get_cache(user_id=telegram_info.id, username=telegram_info.username)
        flatten_ticket = update_helper.flatten(ticket)
        bot.edit_message_text(
            text=conversations.UPDATE_CHECK.format_map(flatten_ticket),
            chat_id=telegram_info.id,
            message_id=message.message_id,
            reply_markup=KEYBOARDS.before_submit_post_keyboard_markup
        )
        return stages.UPDATE_BEFORE_SUBMIT
    else:
        bot.edit_message_text(
            text=conversations.UPDATE_INFO.format_map(
                {'message': TICKET_MAPPING.get(callback_data)}
            ),
            chat_id=telegram_info.id,
            message_id=message.message_id,
            reply_markup=KEYBOARDS.conditions_keyboard_mapping.get(callback_data)
        )
        return stages.UPDATE_FILL_VALUE


@run_async
def fill_in_field(bot, update, user_data):
    callback_data = update.callback_query.data
    message = update.callback_query.message
    if message:
        telegram_info = update._effective_user
        ticket = update_helper.update_cache(user_id=telegram_info.id,
                                            username=telegram_info.username,
                                            content=callback_data)
        flatten_ticket = update_helper.flatten(ticket)
        bot.edit_message_text(
            text=conversations.UPDATE_YOURS.format_map(flatten_ticket),
            chat_id=telegram_info.id,
            message_id=message.message_id,
            reply_markup=KEYBOARDS.update_ticket_keyboard_markup
        )
        return stages.UPDATE_SELECT_FIELD
    else:
        return stages.UPDATE_FILL_VALUE


@run_async
def fill_type_in_field(bot, update, user_data):
    telegram_info = update._effective_user
    text = update.message.text
    ticket = update_helper.update_cache(
        user_id=telegram_info.id,
        username=telegram_info.username,
        content=text)
    flatten_ticket = update_helper.flatten(ticket)
    update.message.reply_text(
        text=conversations.UPDATE_YOURS.format_map(flatten_ticket),
        reply_markup=KEYBOARDS.update_ticket_keyboard_markup
    )
    return stages.UPDATE_SELECT_FIELD


@run_async
def submit(bot, update, user_data):
    callback_data = update.callback_query.data
    message = update.callback_query.message
    telegram_info = update._effective_user

    if callback_data == 'mainpanel':
        bot.edit_message_text(
            chat_id=telegram_info.id,
            message_id=update.callback_query.message.message_id,
            text=conversations.MAIN_PANEL_START.format_map({'username': telegram_info.username}),
            reply_markup=KEYBOARDS.actions_keyboard_markup
        )
        return stages.MAIN_PANEL

    if callback_data == 'submit':
        # Kick banned user out!
        if update_helper.get_lastest_auth(telegram_info) is False:
            update.message.reply_text(conversations.MAIN_PANEL_YELLOWCOW)
            return stages.END

        ticket = update_helper.get_cache(user_id=telegram_info.id, username=telegram_info.username)
        result = request_helper.send_ticket_update(ticket)
        if result.get('status'):
            bot.edit_message_text(
                text=conversations.UPDATE_INTO_DB,
                chat_id=telegram_info.id,
                message_id=message.message_id
            )
        else:
            bot.edit_message_text(
                text=conversations.UPDATE_ERROR,
                chat_id=telegram_info.id,
                message_id=message.message_id,
            )
        bot.send_message(
            text=conversations.AND_THEN,
            chat_id=telegram_info.id,
            message_id=message.message_id,
            reply_markup=KEYBOARDS.after_submit_keyboard
        )
        return stages.UPDATE_SUBMIT


@run_async
def backward(bot, update, user_data):
    callback_data = update.callback_query.data
    message = update.callback_query.message
    telegram_info = update._effective_user
    ticket = update_helper.get_cache(user_id=telegram_info.id, username=telegram_info.username)

    if callback_data == 'backward':
        bot.edit_message_text(
            text=conversations.UPDATE_YOURS.format_map(
                update_helper.flatten(ticket)),
            chat_id=telegram_info.id,
            message_id=message.message_id,
            reply_markup=KEYBOARDS.search_ticket_keyboard_markup
        )
        return stages.UPDATE_SELECT_TICKET

    if callback_data == 'mainpanel':
        bot.edit_message_text(
            chat_id=telegram_info.id,
            message_id=message.message_id,
            text=conversations.MAIN_PANEL_START.format_map({'username': telegram_info.username}),
            reply_markup=KEYBOARDS.actions_keyboard_markup
        )
        return stages.MAIN_PANEL
