import logging
import re

import telegram
from telegram.ext.dispatcher import run_async

import mayday
from mayday import SUBSCRIBE_CHANNEL_NAME
from mayday.constants import TICKET_MAPPING, conversations, stages
from mayday.constants.replykeyboards import KEYBOARDS
from mayday.db.tables.tickets import TicketsModel
from mayday.db.tables.users import UsersModel
from mayday.helpers.auth_helper import AuthHelper
from mayday.helpers.feature_helpers.post_ticket_helper import PostTicketHelper
from mayday.helpers.ticket_helper import TicketHelper
from mayday.objects.user import User

post_helper = PostTicketHelper('post')
auth_helper = AuthHelper(UsersModel(mayday.engine, mayday.metadata, role='writer'))
ticket_helper = TicketHelper(TicketsModel(mayday.engine, mayday.metadata, role='writer'))


logger = logging.getLogger()
logger.setLevel(mayday.get_log_level())
logger.addHandler(mayday.console_handler())


@run_async
def start(bot, update, *args, **kwargs):
    user = User(telegram_user=update.effective_user)
    ticket = post_helper.reset_cache(user.user_id, user.username)
    category = post_helper.get_category_id_from_cache(user.user_id)
    bot.edit_message_text(
        text=conversations.POST_TICKET_START.format_map(ticket.to_human_readable()),
        chat_id=user.user_id,
        message_id=update.callback_query.message.message_id,
        reply_markup=KEYBOARDS.post_ticket_keyboard_markup.get(category))
    return stages.POST_SELECT_FIELD


@run_async
def select_field(bot, update, *args, **kwargs):
    callback_data = update.callback_query.data
    logger.debug(callback_data)
    message = update.callback_query.message
    user = User(telegram_user=update.effective_user)
    post_helper.save_last_choice(user_id=user.user_id, field=callback_data)
    category = post_helper.get_category_id_from_cache(user_id=user.user_id)
    logger.debug(category)

    if callback_data == 'reset':
        ticket = post_helper.reset_cache(user_id=user.user_id, username=user.username)
        bot.edit_message_text(
            text=conversations.POST_TICKET_START.format_map(ticket.to_human_readable()),
            chat_id=user.user_id,
            message_id=message.message_id,
            reply_markup=KEYBOARDS.post_ticket_keyboard_markup.get(category),
            parse_mode=telegram.ParseMode.MARKDOWN)
        return stages.POST_SELECT_FIELD

    if callback_data == 'check':
        ticket = post_helper.load_drafting_ticket(user.user_id)
        check_result = ticket.validate()
        check_wishlist = ticket.validate_wishlist()
        category = post_helper.get_category_id_from_cache(user.user_id)
        if check_result['status']:
            if check_wishlist['status'] is False:
                ticket = ticket.fill_full_wishlist()
                post_helper.save_drafting_ticket(user.user_id, ticket)
            bot.edit_message_text(
                text=conversations.POST_TICKET_CHECK.format_map(ticket.to_human_readable()),
                chat_id=user.user_id,
                message_id=message.message_id,
                reply_markup=KEYBOARDS.before_submit_post_keyboard_markup)
            return stages.POST_BEFORE_SUBMIT

        bot.send_message(
            text=conversations.TYPE_IN_WARNING.format(error_message=check_result['info']),
            chat_id=user.user_id,
            message_id=message.message_id)
        bot.send_message(
            text=conversations.POST_TICKET_START.format_map(ticket.to_human_readable()),
            chat_id=user.user_id,
            message_id=message.message_id,
            reply_markup=KEYBOARDS.post_ticket_keyboard_markup.get(category))
        return stages.POST_SELECT_FIELD

    if callback_data == 'section':
        ticket = post_helper.load_drafting_ticket(user.user_id)
        category = post_helper.get_category_id_from_cache(user_id=user.user_id)
        if ticket.price:
            bot.edit_message_text(
                text=conversations.POST_TICKET_INFO.format(message=TICKET_MAPPING.get(callback_data)),
                chat_id=user.user_id,
                message_id=message.message_id,
                reply_markup=KEYBOARDS.conditions_keyboard_mapping.get(callback_data)['price'])
            return stages.POST_FILL_VALUE
        bot.edit_message_text(
            text=conversations.POST_TICKET_SECTION,
            chat_id=user.user_id,
            message_id=message.message_id,
            reply_markup=KEYBOARDS.post_ticket_keyboard_markup.get(category))
        return stages.POST_SELECT_FIELD

    if callback_data == 'mainpanel':
        bot.edit_message_text(
            chat_id=user.user_id,
            message_id=message.message_id,
            text=conversations.MAIN_PANEL_START.format(username=user.username),
            reply_markup=KEYBOARDS.actions_keyboard_markup)
        return stages.MAIN_PANEL

    bot.edit_message_text(
        text=conversations.POST_TICKET_INFO.format(message=TICKET_MAPPING.get(callback_data)),
        chat_id=user.user_id,
        message_id=message.message_id,
        reply_markup=KEYBOARDS.conditions_keyboard_mapping.get(callback_data))
    return stages.POST_FILL_VALUE


@run_async
def fill_in_field(bot, update, *args, **kwargs):

    callback_data = update.callback_query.data
    message = update.callback_query.message
    user = User(telegram_user=update.effective_user)
    category = post_helper.get_category_id_from_cache(user_id=user.user_id)
    if re.match(r'\d+||^([A-Z0-9]){2}$', callback_data):
        ticket = post_helper.update_cache(user.user_id, callback_data)
        bot.edit_message_text(
            text=conversations.POST_TICKET_START.format_map(ticket.to_human_readable()),
            chat_id=user.user_id,
            message_id=message.message_id,
            reply_markup=KEYBOARDS.post_ticket_keyboard_markup.get(category))
        return stages.POST_SELECT_FIELD

    ticket = post_helper.load_drafting_ticket(user.user_id)
    choice = post_helper.load_last_choice(user.user_id)
    keyboard = KEYBOARDS.conditions_keyboard_mapping.get(choice)
    text = '\n\n'.join([conversations.TYPE_IN_ERROR,
                        conversations.POST_TICKET_INFO.format(message=TICKET_MAPPING.get(choice))])
    bot.edit_message_text(text=text, chat_id=user.user_id, message_id=message.message_id, reply_markup=keyboard)
    # FIXME: No Return?


@run_async
def fill_type_in_field(bot, update, *args, **kwargs):
    user = User(telegram_user=update.effective_user)
    text = update.message.text
    ticket = post_helper.update_cache(user.user_id, text)
    category = post_helper.get_category_id_from_cache(user_id=user.user_id)
    update.message.reply_text(
        text=conversations.POST_TICKET_START.format_map(ticket.to_human_readable()),
        reply_markup=KEYBOARDS.post_ticket_keyboard_markup.get(category))
    return stages.POST_SELECT_FIELD


@run_async
def submit(bot, update, *args, **kwargs):
    callback_data = update.callback_query.data
    message = update.callback_query.message
    user = User(telegram_user=update.effective_user)
    category = post_helper.get_category_id_from_cache(user_id=user.user_id)

    if callback_data == 'reset':
        ticket = post_helper.reset_cache(user_id=user.user_id, username=user.username)
        bot.edit_message_text(
            text=conversations.POST_TICKET_START.format_map(ticket.to_human_readable()),
            chat_id=user.user_id,
            message_id=message.message_id,
            reply_markup=KEYBOARDS.post_ticket_keyboard_markup.get(category))
        return stages.POST_SELECT_FIELD

    if callback_data == 'submit':
        # Kick banned user out!
        if auth_helper.auth(user)['is_blacklist']:
            update.message.reply_text(conversations.MAIN_PANEL_YELLOWCOW)
            return stages.END
        ticket = post_helper.load_drafting_ticket(user.user_id)
        if ticket_helper.save_ticket(ticket):
            bot.edit_message_text(
                text=conversations.POST_TICKET_INTO_DB,
                chat_id=user.user_id,
                message_id=message.message_id)
        else:
            bot.edit_message_text(
                text=conversations.POST_TICKET_ERROR,
                chat_id=user.user_id,
                message_id=message.message_id)

        # Send Ticket to Channel
        bot.send_message(
            text=conversations.NEW_TICKET.format_map(ticket.to_human_readable()),
            chat_id=SUBSCRIBE_CHANNEL_NAME,
            parse_mode=telegram.ParseMode.MARKDOWN)

        bot.send_message(
            text=conversations.AND_THEN,
            chat_id=user.user_id,
            message_id=message.message_id,
            reply_markup=KEYBOARDS.after_submit_keyboard)
        return stages.POST_SUBMIT


@run_async
def backward(bot, update, *args, **kwargs):
    callback_data = update.callback_query.data
    message = update.callback_query.message
    user = User(telegram_user=update.effective_user)
    ticket = post_helper.load_drafting_ticket(user.user_id)
    if callback_data == 'backward':
        bot.send_message(
            text=conversations.POST_TICKET_START.format_map(ticket.to_human_readable()),
            chat_id=user.user_id,
            message_id=message.message_id,
            reply_markup=KEYBOARDS.search_ticket_keyboard_markup)
        return stages.POST_SELECT_FIELD
    if callback_data == 'mainpanel':
        bot.sendMessage(
            chat_id=user.user_id,
            message_id=message.message_id,
            text=conversations.MAIN_PANEL_START.format(username=user.username),
            reply_markup=KEYBOARDS.actions_keyboard_markup)
        return stages.MAIN_PANEL
