import logging
import re
import time
import traceback

import mayday
import telegram
from mayday import SUBSCRIBE_CHANNEL_NAME
from mayday.constants import TICKET_MAPPING, conversations, stages
from mayday.constants.replykeyboards import KEYBOARDS
from mayday.controllers.redis import RedisController
from mayday.db.tables.tickets import TicketsModel
from mayday.db.tables.users import UsersModel
from mayday.helpers.auth_helper import AuthHelper
from mayday.helpers.feature_helpers.post_ticket_helper import PostTicketHelper
from mayday.helpers.ticket_helper import TicketHelper
from mayday.objects.user import User
from telegram.error import BadRequest
from telegram.ext.dispatcher import run_async

post_helper = PostTicketHelper('post')
auth_helper = AuthHelper(UsersModel(mayday.engine, mayday.metadata, role='writer'))
ticket_helper = TicketHelper(TicketsModel(mayday.engine, mayday.metadata, role='writer'))
redis = RedisController(redis_conection_pool=mayday.FEATURE_REDIS_CONNECTION_POOL)

logger = logging.getLogger()
logger.setLevel(mayday.get_log_level())
logger.addHandler(mayday.console_handler())


@run_async
def start(bot, update, *args, **kwargs):
    user = User(telegram_user=update.effective_user)

    category = post_helper.get_category_id_from_cache(user.user_id)
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

    ticket = post_helper.reset_cache(user.user_id, user.username)
    logger.info(ticket.to_dict())
    update.message.reply_text(conversations.MAIN_PANEL_REMINDER)
    time.sleep(0.3)
    bot.send_message(
        text=conversations.POST_TICKET_START.format_map(ticket.to_human_readable()),
        chat_id=user.user_id,
        reply_markup=KEYBOARDS.post_ticket_keyboard_markup.get(category))
    return stages.POST_SELECT_FIELD


@run_async
def select_field(bot, update, *args, **kwargs):
    callback_data = update.callback_query.data
    logger.debug(callback_data)
    message = update.callback_query.message
    user = User(telegram_user=update.effective_user)
    if not post_helper.save_last_choice(user_id=user.user_id, field=callback_data):
        try:
            ticket = post_helper.load_drafting_ticket(user.user_id)
        except Exception:
            logger.warning("cache miss")
            ticket = post_helper.reset_cache(user.user_id, user.username)
        category = post_helper.get_category_id_from_cache(user.user_id)

        bot.send_message(
            text=conversations.POST_TICKET_START.format_map(ticket.to_human_readable()),
            chat_id=user.user_id,
            reply_markup=KEYBOARDS.post_ticket_keyboard_markup.get(category))
        return stages.POST_SELECT_FIELD

    category = post_helper.get_category_id_from_cache(user_id=user.user_id)
    logger.debug(category)

    if callback_data == 'reset':
        ticket = post_helper.reset_cache(user_id=user.user_id, username=user.username)
        try:
            bot.edit_message_text(
                text=conversations.POST_TICKET_START.format_map(ticket.to_human_readable()),
                chat_id=user.user_id,
                message_id=message.message_id,
                reply_markup=KEYBOARDS.post_ticket_keyboard_markup.get(category),
                parse_mode=telegram.ParseMode.MARKDOWN)
        except BadRequest:
            bot.send_message(
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
            try:
                bot.edit_message_text(
                    text=conversations.POST_TICKET_CHECK.format_map(ticket.to_human_readable()),
                    chat_id=user.user_id,
                    message_id=message.message_id,
                    reply_markup=KEYBOARDS.before_submit_post_keyboard_markup)
            except BadRequest:
                bot.send_message(
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
        if ticket.price_id:
            try:
                bot.edit_message_text(
                    text=conversations.POST_TICKET_INFO.format(message=TICKET_MAPPING.get(callback_data)),
                    chat_id=user.user_id,
                    message_id=message.message_id,
                    reply_markup=KEYBOARDS.conditions_keyboard_mapping.get(callback_data)[ticket.price_id])
            except BadRequest:
                bot.send_message(
                    text=conversations.POST_TICKET_INFO.format(message=TICKET_MAPPING.get(callback_data)),
                    chat_id=user.user_id,
                    message_id=message.message_id,
                    reply_markup=KEYBOARDS.conditions_keyboard_mapping.get(callback_data)[ticket.price_id])
            return stages.POST_FILL_VALUE
        try:
            bot.edit_message_text(
                text=conversations.POST_TICKET_SECTION,
                chat_id=user.user_id,
                message_id=message.message_id,
                reply_markup=KEYBOARDS.post_ticket_keyboard_markup.get(category))
        except BadRequest:
            bot.send_message(
                text=conversations.POST_TICKET_SECTION,
                chat_id=user.user_id,
                message_id=message.message_id,
                reply_markup=KEYBOARDS.post_ticket_keyboard_markup.get(category))
        return stages.POST_SELECT_FIELD

    try:
        bot.edit_message_text(
            text=conversations.POST_TICKET_INFO.format(message=TICKET_MAPPING.get(callback_data)),
            chat_id=user.user_id,
            message_id=message.message_id,
            reply_markup=KEYBOARDS.conditions_keyboard_mapping.get(callback_data))
    except BadRequest:
        bot.send_message(
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
        logger.info(ticket.to_dict())
        try:
            bot.edit_message_text(
                text=conversations.POST_TICKET_START.format_map(ticket.to_human_readable()),
                chat_id=user.user_id,
                message_id=message.message_id,
                reply_markup=KEYBOARDS.post_ticket_keyboard_markup.get(category))
        except BadRequest:
            bot.send_message(
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
    try:
        bot.edit_message_text(text=text, chat_id=user.user_id, message_id=message.message_id, reply_markup=keyboard)
    except BadRequest:
        bot.send_message(text=text, chat_id=user.user_id, message_id=message.message_id, reply_markup=keyboard)


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
        try:
            bot.edit_message_text(
                text=conversations.POST_TICKET_START.format_map(ticket.to_human_readable()),
                chat_id=user.user_id,
                message_id=message.message_id,
                reply_markup=KEYBOARDS.post_ticket_keyboard_markup.get(category))
        except BadRequest:
            bot.send_message(
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
            try:
                bot.edit_message_text(
                    text=conversations.POST_TICKET_INTO_DB,
                    chat_id=user.user_id,
                    message_id=message.message_id)
            except BadRequest:
                bot.send_message(
                    text=conversations.POST_TICKET_INTO_DB,
                    chat_id=user.user_id,
                    message_id=message.message_id)
        else:
            try:
                bot.edit_message_text(
                    text=conversations.POST_TICKET_ERROR,
                    chat_id=user.user_id,
                    message_id=message.message_id)
            except BadRequest:
                bot.send_message(
                    text=conversations.POST_TICKET_ERROR,
                    chat_id=user.user_id,
                    message_id=message.message_id)

        # Send Ticket to Channel
        bot.send_message(
            text=conversations.NEW_TICKET.format_map(ticket.to_human_readable()),
            chat_id=SUBSCRIBE_CHANNEL_NAME,
            parse_mode=telegram.ParseMode.MARKDOWN)
        return stages.END
