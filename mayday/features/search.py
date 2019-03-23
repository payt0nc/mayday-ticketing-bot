import re
import traceback

import telegram
from telegram import ReplyKeyboardRemove, bot, chataction
from telegram.ext.dispatcher import run_async

from mayday.constants import TICKET_MAPPING, conversations, stages
from mayday.constants.replykeyboards import ReplyKeyboards
from mayday.controllers.request import RequestHelper
from mayday.helpers.search_helper import SearchHelper
from mayday.utils import log_util
from mayday.validators.ticket_validator import TicketValidator

KEYBOARDS = ReplyKeyboards()
request_helper = RequestHelper()

search_helper = SearchHelper('search_ticket')


@run_async
def quick_search_start(bot, update, user_data):
    telegram_info = update._effective_user
    message = update.callback_query.message
    query = search_helper.get_quick_search(user_id=telegram_info.id)
    search_helper.set_cache(user_id=telegram_info.id, content=query)
    if query:
        flatten_query = search_helper.flatten(query)
        bot.edit_message_text(
            text=conversations.QUICK_SEARCH_LIST_QUERY.format_map(flatten_query),
            chat_id=telegram_info.id,
            message_id=message.message_id,
            reply_markup=KEYBOARDS.quick_search_keyboard_markup)
        return stages.SEARCH_BEFORE_SUBMIT
    else:
        bot.edit_message_text(
            text=conversations.QUICK_SEARCH_NULL,
            chat_id=telegram_info.id,
            message_id=message.message_id,
            reply_markup=KEYBOARDS.quick_search_backward_keyboard)
        return stages.SEARCH_SUBMIT


@run_async
def start(bot, update, user_data):
    telegram_info = update._effective_user
    message = update.callback_query.message
    query = search_helper.init_cache(
        user_id=telegram_info.id,
        username=telegram_info.username)
    flatten_query = search_helper.flatten(query)
    bot.edit_message_text(
        text=conversations.SEARCH_TICKET_START.format_map(flatten_query),
        chat_id=telegram_info.id,
        message_id=message.message_id,
        reply_markup=KEYBOARDS.search_ticket_keyboard_markup)
    return stages.SEARCH_SELECT_FIELD


@run_async
def select_field(bot, update, user_data):
    callback_data = update.callback_query.data
    message = update.callback_query.message
    telegram_info = update._effective_user
    search_helper.set_last_choice(
        user_id=telegram_info.id,
        content=callback_data)
    if callback_data == 'check':
        query = search_helper.get_cache(user_id=telegram_info.id, username=telegram_info.username)
        check_result = TicketValidator(query).check_query()
        if check_result['status']:
            flatten_query = search_helper.flatten(query)
            bot.edit_message_text(
                text=conversations.SEARCH_CHECK.format_map(flatten_query),
                chat_id=telegram_info.id,
                message_id=message.message_id,
                reply_markup=KEYBOARDS.before_submit_search_keyboard_markup,
                parse_mode=telegram.ParseMode.MARKDOWN)
            return stages.SEARCH_BEFORE_SUBMIT
        else:
            bot.send_message(
                text=conversations.TYPE_IN_WARNING.format_map({'error_message': check_result['info']}),
                chat_id=telegram_info.id,
                message_id=message.message_id)
            flatten_query = search_helper.flatten(query)
            bot.send_message(
                text=conversations.SEARCH_TICKET_START.format_map(flatten_query),
                chat_id=telegram_info.id,
                message_id=message.message_id,
                reply_markup=KEYBOARDS.search_ticket_keyboard_markup,
                parse_mode=telegram.ParseMode.MARKDOWN)
            return stages.SEARCH_SELECT_FIELD
    elif callback_data == 'reset':
        query = search_helper.reset_cache(
            user_id=telegram_info.id,
            username=telegram_info.username)
        flatten_query = search_helper.flatten(query)
        bot.edit_message_text(
            text=conversations.SEARCH_TICKET_START.format_map(flatten_query),
            chat_id=telegram_info.id,
            message_id=message.message_id,
            reply_markup=KEYBOARDS.search_ticket_keyboard_markup,
            parse_mode=telegram.ParseMode.MARKDOWN)
        return stages.SEARCH_SELECT_FIELD
    elif callback_data == 'mainpanel':
        bot.edit_message_text(
            chat_id=telegram_info.id,
            message_id=message.message_id,
            text=conversations.MAIN_PANEL_START.format_map({'username': telegram_info.username}),
            reply_markup=KEYBOARDS.actions_keyboard_markup)
        return stages.MAIN_PANEL
    else:
        bot.edit_message_text(
            text=conversations.SEARCH_TICKET_INFO.format_map(
                {'message': TICKET_MAPPING.get(callback_data)}),
            chat_id=telegram_info.id,
            message_id=message.message_id,
            reply_markup=KEYBOARDS.conditions_keyboard_mapping.get(callback_data))
    return stages.SEARCH_FILL_VALUE


@run_async
def fill_in_field(bot, update, user_data):
    callback_data = update.callback_query.data
    message = update.callback_query.message
    telegram_info = update._effective_user
    if re.match(r'\d+', callback_data):
        query = search_helper.update_cache(
            user_id=telegram_info.id,
            username=telegram_info.username,
            content=callback_data)
        flatten_query = search_helper.flatten(query)
        bot.edit_message_text(
            chat_id=telegram_info.id,
            message_id=message.message_id,
            text=conversations.SEARCH_TICKET_START.format_map(flatten_query),
            reply_markup=KEYBOARDS.search_ticket_keyboard_markup,
            parse_mode=telegram.ParseMode.MARKDOWN)
        return stages.SEARCH_SELECT_FIELD
    else:
        query = search_helper.get_cache(user_id=telegram_info.id, username=telegram_info.username)
        choice = search_helper.get_last_choice(user_id=telegram_info.id)
        flatten_query = search_helper.flatten(query)
        bot.sendMessage(
            chat_id=telegram_info.id,
            text=conversations.TYPE_IN_ERROR)
        bot.sendMessage(
            chat_id=telegram_info.id,
            message_id=message.message_id,
            text=conversations.SEARCH_TICKET_START.format_map(flatten_query),
            reply_markup=KEYBOARDS.conditions_keyboard_mapping.get(choice),
            parse_mode=telegram.ParseMode.MARKDOWN)


@run_async
def submit(bot, update, user_data):
    callback_data = update.callback_query.data
    message = update.callback_query.message
    telegram_info = update._effective_user
    if callback_data == 'mainpanel':
        bot.sendMessage(
            chat_id=telegram_info.id,
            message_id=message.message_id,
            text=conversations.MAIN_PANEL_START.format_map({'username': telegram_info.username}),
            reply_markup=KEYBOARDS.actions_keyboard_markup)
        return stages.MAIN_PANEL

    if callback_data == 'reset':
        search_helper.reset_cache(
            user_id=telegram_info.id,
            username=telegram_info.username)
        query = search_helper.reset_cache(
            user_id=telegram_info.id,
            username=telegram_info.username)
        bot.edit_message_text(
            text=conversations.SEARCH_TICKET_START.format_map(
                search_helper.flatten(query)),
            chat_id=telegram_info.id,
            message_id=message.message_id,
            reply_markup=KEYBOARDS.search_ticket_keyboard_markup,
            parse_mode=telegram.ParseMode.MARKDOWN)
        return stages.SEARCH_SELECT_FIELD

    if callback_data == 'back':
        query = search_helper.get_cache(user_id=telegram_info.id, username=telegram_info.username)
        bot.edit_message_reply_markup(
            text=conversations.SEARCH_TICKET_START.format_map(
                search_helper.flatten(query)),
            chat_id=telegram_info.id,
            message_id=message.message_id,
            reply_markup=KEYBOARDS.search_ticket_keyboard_markup,
            parse_mode=telegram.ParseMode.MARKDOWN)
        return stages.SEARCH_SELECT_FIELD

    if callback_data == 'quick_search':
        query = search_helper.get_cache(user_id=telegram_info.id, username=telegram_info.username)
        flatten_query = search_helper.flatten(query)
        result = search_helper.set_quick_search(
            user_id=telegram_info.id,
            query=query)
        bot.edit_message_text(
            text=conversations.QUICK_SEARCH_INSERT_SUCESS.format_map(flatten_query),
            chat_id=telegram_info.id,
            message_id=message.message_id,
            reply_markup=KEYBOARDS.before_submit_post_keyboard_markup)
        return stages.SEARCH_BEFORE_SUBMIT

    if callback_data == 'submit':
        # Kick banned user out!
        if search_helper.get_lastest_auth(telegram_info) is False:
            update.message.reply_text(conversations.MAIN_PANEL_YELLOWCOW)
            return stages.END

        query = search_helper.get_cache(user_id=telegram_info.id, username=telegram_info.username)
        bot.send_chat_action(
            chat_id=telegram_info.id,
            action=chataction.ChatAction.TYPING)
        result = request_helper.send_ticket_query(query)

        if result.get('status'):
            tickets = result.get('info')
            if (tickets and len(tickets) <= 25):
                bot.edit_message_text(
                    text=conversations.SEARCH_WITH_RESULTS,
                    chat_id=telegram_info.id,
                    message_id=message.message_id)
                traits = search_helper.generate_tickets_traits(tickets)
                for trait in traits:
                    bot.send_message(
                        text=search_helper.tickets_tostr(trait),
                        chat_id=telegram_info.id,
                        message_id=message.message_id)
                bot.send_message(
                    text=conversations.AND_THEN,
                    chat_id=telegram_info.id,
                    message_id=message.message_id,
                    reply_markup=KEYBOARDS.after_submit_keyboard)
            elif len(tickets) > 25:
                bot.edit_message_text(
                    text=conversations.SEARCH_TOO_MUCH_TICKETS,
                    chat_id=telegram_info.id,
                    message_id=message.message_id)
                bot.send_message(
                    text=conversations.AND_THEN,
                    chat_id=telegram_info.id,
                    message_id=message.message_id,
                    reply_markup=KEYBOARDS.after_submit_keyboard)
            else:
                bot.edit_message_text(
                    text=conversations.SEARCH_WITHOUT_TICKETS,
                    chat_id=telegram_info.id,
                    message_id=message.message_id,
                    reply_markup=KEYBOARDS.after_submit_keyboard)
            return stages.SEARCH_SUBMIT
        else:
            bot.send_message(
                text=conversations.SEARCH_TICKET_ERROR,
                chat_id=telegram_info.id,
                message_id=message.message_id)
            query = search_helper.get_cache(user_id=telegram_info.id, username=telegram_info.username)
            bot.send_message(
                text=conversations.SEARCH_TICKET_START.format_map(
                    search_helper.flatten(query)),
                chat_id=telegram_info.id,
                message_id=message.message_id,
                reply_markup=KEYBOARDS.search_ticket_keyboard_markup,
                parse_mode=telegram.ParseMode.MARKDOWN)
        return stages.SEARCH_SELECT_FIELD


@run_async
def backward(bot, update, user_data):
    callback_data = update.callback_query.data
    message = update.callback_query.message
    telegram_info = update._effective_user
    query = search_helper.get_cache(user_id=telegram_info.id, username=telegram_info.username)

    if callback_data == 'backward':
        bot.send_message(
            text=conversations.SEARCH_TICKET_START.format_map(
                search_helper.flatten(query)),
            chat_id=telegram_info.id,
            message_id=message.message_id,
            reply_markup=KEYBOARDS.search_ticket_keyboard_markup
        )
        return stages.SEARCH_SELECT_FIELD

    if callback_data == 'mainpanel':
        bot.sendMessage(
            chat_id=telegram_info.id,
            message_id=message.message_id,
            text=conversations.MAIN_PANEL_START.format_map({'username': telegram_info.username}),
            reply_markup=KEYBOARDS.actions_keyboard_markup
        )
        return stages.MAIN_PANEL
