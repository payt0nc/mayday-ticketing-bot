import re
import traceback

import telegram
from telegram.ext.dispatcher import run_async

from mayday.constants import TICKET_MAPPING, conversations, stages
from mayday.constants.replykeyboards import ReplyKeyboards
from mayday.helpers.request import RequestHelper
from mayday.helpers.feature_helpers.post_ticket_helper import PostTicketHelper


KEYBOARDS = ReplyKeyboards()
request_helper = RequestHelper()
post_helper = PostTicketHelper('post_ticket')


@run_async
def start(bot, update, user_data):
    callback_data = update.callback_query.data
    telegram_info = update._effective_user
    ticket = post_helper.init_cache(user_id=telegram_info.id,
                                    username=telegram_info.username)
    category_id = post_helper.get_category_id_from_cache(user_id=telegram_info.id,
                                                         username=telegram_info.username)
    bot.edit_message_text(
        text=conversations.POST_TICKET_START.format_map(
            post_helper.flatten(ticket)),
        chat_id=telegram_info.id,
        message_id=update.callback_query.message.message_id,
        reply_markup=KEYBOARDS.post_ticket_keyboard_markup.get(category_id))
    return stages.POST_SELECT_FIELD


@run_async
def select_field(bot, update, user_data):

    callback_data = update.callback_query.data
    message = update.callback_query.message
    telegram_info = update._effective_user
    post_helper.set_last_choice(user_id=telegram_info.id, content=callback_data)
    category_id = post_helper.get_category_id_from_cache(user_id=telegram_info.id, username=telegram_info.username)
    if callback_data == 'reset':
        ticket = post_helper.reset_cache(user_id=telegram_info.id, username=telegram_info.username)
        bot.edit_message_text(
            text=conversations.POST_TICKET_START.format_map(
                post_helper.flatten(ticket)),
            chat_id=telegram_info.id,
            message_id=message.message_id,
            reply_markup=KEYBOARDS.post_ticket_keyboard_markup.get(category_id),
            parse_mode=telegram.ParseMode.MARKDOWN)
        return stages.POST_SELECT_FIELD
    elif callback_data == 'check':
        ticket = post_helper.get_cache(user_id=telegram_info.id, username=telegram_info.username)
        check_result = TicketValidator(ticket).check_ticket()
        check_wishlist_result = WishlistValidator(ticket).check_wishlist()
        category_id = post_helper.get_category_id_from_cache(
            user_id=telegram_info.id,
            username=telegram_info.username)
        if check_result.status:
            if check_wishlist_result.status is False:
                ticket = post_helper.fill_in_wishlist(ticket, check_wishlist_result.info)
            flatten_ticket = post_helper.flatten(ticket)
            bot.edit_message_text(
                text=conversations.POST_TICKET_CHECK.format_map(flatten_ticket),
                chat_id=telegram_info.id,
                message_id=message.message_id,
                reply_markup=KEYBOARDS.before_submit_post_keyboard_markup)
            return stages.POST_BEFORE_SUBMIT
        else:
            bot.send_message(
                text=conversations.TYPE_IN_WARNING.format_map({'error_message': check_result['info']}),
                chat_id=telegram_info.id,
                message_id=message.message_id)
            bot.send_message(
                text=conversations.POST_TICKET_START.format_map(
                    post_helper.flatten(ticket)),
                chat_id=telegram_info.id,
                message_id=message.message_id,
                reply_markup=KEYBOARDS.post_ticket_keyboard_markup.get(category_id))
            return stages.POST_SELECT_FIELD
    elif callback_data == 'section':
        ticket = post_helper.get_cache(user_id=telegram_info.id, username=telegram_info.username)
        category_id = post_helper.get_category_id_from_cache(
            user_id=telegram_info.id, username=telegram_info.username)
        if ticket.get('price_id'):
            bot.edit_message_text(
                text=conversations.POST_TICKET_INFO.format_map(
                    {'message': TICKET_MAPPING.get(callback_data)}),
                chat_id=telegram_info.id,
                message_id=message.message_id,
                reply_markup=KEYBOARDS.conditions_keyboard_mapping.get(callback_data).get(ticket.get('price_id')))
            return stages.POST_FILL_VALUE
        else:
            bot.edit_message_text(
                text=conversations.POST_TICKET_SECTION,
                chat_id=telegram_info.id,
                message_id=message.message_id,
                reply_markup=KEYBOARDS.post_ticket_keyboard_markup.get(category_id))
            return stages.POST_SELECT_FIELD
    elif callback_data == 'mainpanel':
        bot.edit_message_text(
            chat_id=telegram_info.id,
            message_id=message.message_id,
            text=conversations.MAIN_PANEL_START.format_map({'username': telegram_info.username}),
            reply_markup=KEYBOARDS.actions_keyboard_markup)
        return stages.MAIN_PANEL
    else:
        bot.edit_message_text(
            text=conversations.POST_TICKET_INFO.format_map(
                {'message': TICKET_MAPPING.get(callback_data)}),
            chat_id=telegram_info.id,
            message_id=message.message_id,
            reply_markup=KEYBOARDS.conditions_keyboard_mapping.get(callback_data))
        return stages.POST_FILL_VALUE


@run_async
def fill_in_field(bot, update, user_data):

    callback_data = update.callback_query.data
    message = update.callback_query.message
    telegram_info = update._effective_user
    category_id = post_helper.get_category_id_from_cache(user_id=telegram_info.id, username=telegram_info.username)
    if re.match(r'\d+||^([A-Z0-9]){2}$', callback_data):
        ticket = post_helper.update_cache(user_id=telegram_info.id,
                                          username=telegram_info.username,
                                          content=callback_data)
        flatten_ticket = post_helper.flatten(ticket)
        bot.edit_message_text(
            text=conversations.POST_TICKET_START.format_map(flatten_ticket),
            chat_id=telegram_info.id,
            message_id=message.message_id,
            reply_markup=KEYBOARDS.post_ticket_keyboard_markup.get(category_id))
        return stages.POST_SELECT_FIELD
    else:
        ticket = post_helper.get_cache(user_id=telegram_info.id, username=telegram_info.username)
        choice = post_helper.get_last_choice(user_id=telegram_info.id)
        keyboard = KEYBOARDS.conditions_keyboard_mapping.get(choice)
        flatten_ticket = post_helper.flatten(ticket)
        text = '\n\n'.join([
            conversations.TYPE_IN_ERROR,
            conversations.POST_TICKET_INFO.format_map(
                {'message': TICKET_MAPPING.get(choice)})])
        bot.edit_message_text(
            text=text,
            chat_id=telegram_info.id,
            message_id=message.message_id,
            reply_markup=keyboard)
        # FIXME: No Return?


@run_async
def fill_type_in_field(bot, update, user_data):
    telegram_info = update._effective_user
    text = update.message.text
    ticket = post_helper.update_cache(user_id=telegram_info.id,
                                      username=telegram_info.username,
                                      content=text)
    flatten_ticket = post_helper.flatten(ticket)
    category_id = post_helper.get_category_id_from_cache(user_id=telegram_info.id, username=telegram_info.username)
    update.message.reply_text(
        text=conversations.POST_TICKET_START.format_map(flatten_ticket),
        reply_markup=KEYBOARDS.post_ticket_keyboard_markup.get(category_id))
    return stages.POST_SELECT_FIELD


@run_async
def submit(bot, update, user_data):
    callback_data = update.callback_query.data
    message = update.callback_query.message
    telegram_info = update._effective_user
    category_id = post_helper.get_category_id_from_cache(user_id=telegram_info.id, username=telegram_info.username)

    if callback_data == 'reset':
        ticket = post_helper.reset_cache(user_id=telegram_info.id, username=telegram_info.username)
        bot.edit_message_text(
            text=conversations.POST_TICKET_START.format_map(
                post_helper.flatten(ticket)),
            chat_id=telegram_info.id,
            message_id=message.message_id,
            reply_markup=KEYBOARDS.post_ticket_keyboard_markup.get(category_id))
        return stages.POST_SELECT_FIELD

    if callback_data == 'submit':
        # Kick banned user out!
        if post_helper.get_lastest_auth(telegram_info) is False:
            update.message.reply_text(conversations.MAIN_PANEL_YELLOWCOW)
            return stages.END
        ticket = post_helper.get_cache(user_id=telegram_info.id, username=telegram_info.username)
        result = request_helper.send_ticket_insert(ticket)
        if result.get('status'):
            bot.edit_message_text(
                text=conversations.POST_TICKET_INTO_DB,
                chat_id=telegram_info.id,
                message_id=message.message_id)
        else:
            bot.edit_message_text(
                text=conversations.POST_TICKET_ERROR,
                chat_id=telegram_info.id,
                message_id=message.message_id)
        bot.send_message(
            text=conversations.AND_THEN,
            chat_id=telegram_info.id,
            message_id=message.message_id,
            reply_markup=KEYBOARDS.after_submit_keyboard)
        return stages.POST_SUBMIT


@run_async
def backward(bot, update, user_data):
    callback_data = update.callback_query.data
    message = update.callback_query.message
    telegram_info = update._effective_user
    ticket = post_helper.get_cache(user_id=telegram_info.id, username=telegram_info.username)
    if callback_data == 'backward':
        bot.send_message(
            text=conversations.POST_TICKET_START.format_map(
                post_helper.flatten(ticket)),
            chat_id=telegram_info.id,
            message_id=message.message_id,
            reply_markup=KEYBOARDS.search_ticket_keyboard_markup)
        return stages.POST_SELECT_FIELD
    if callback_data == 'mainpanel':
        bot.sendMessage(
            chat_id=telegram_info.id,
            message_id=message.message_id,
            text=conversations.MAIN_PANEL_START.format_map({'username': telegram_info.username}),
            reply_markup=KEYBOARDS.actions_keyboard_markup)
        return stages.MAIN_PANEL
