import re

import telegram
from telegram.ext.dispatcher import run_async

from mayday.constants import conversations, stages
from mayday.constants.replykeyboards import ReplyKeyboards
from mayday.controllers.request import RequestHelper
from mayday.helpers.sp_events_helper import SPEventHelper

sp_helper = SPEventHelper('sp_helper')
request_helper = RequestHelper()
KEYBOARDS = ReplyKeyboards()


@run_async
def start(bot, update, user_data):
    telegram_info = update._effective_user
    message = update.callback_query.message
    callback_data = update.callback_query.data
    events = request_helper.get_sp_events().get('info')
    keyboard = sp_helper.generate_keyboard(events)
    if events:
        bot.edit_message_text(
            text=conversations.SUPPORT_LIST_EVENTS,
            chat_id=telegram_info.id,
            message_id=message.message_id,
            reply_markup=keyboard
        )
    else:
        bot.edit_message_text(
            text=conversations.SUPPORT_NONE_EVENTS,
            chat_id=telegram_info.id,
            message_id=message.message_id,
            reply_markup=KEYBOARDS.return_main_panal
        )
    return stages.SUPPORT_EVENT_LIST


@run_async
def list_events(bot, update, user_data):
    telegram_info = update._effective_user
    message = update.callback_query.message
    callback_data = update.callback_query.data
    events = request_helper.get_sp_events().get('info')
    keyboard = sp_helper.generate_keyboard(events)
    event_mapping = sp_helper.generate_event_mapping(events)

    if callback_data == 'mainpanel':
        bot.edit_message_text(
            text=conversations.MAIN_PANEL_START.format_map(
                {'username': telegram_info.username}),
            chat_id=telegram_info.id,
            message_id=message.message_id,
            reply_markup=KEYBOARDS.actions_keyboard_markup
        )
        return stages.MAIN_PANEL

    elif re.match(r'\d+', callback_data):
        event = event_mapping.get(int(callback_data))
        if event:
            if event.get('type') == 'photo':
                bot.send_photo(
                    chat_id=telegram_info.id,
                    photo=event.get('attachment_id'),
                    caption=event.get('description'),
                    reply_markup=keyboard,
                    parse_mode=telegram.ParseMode.MARKDOWN
                )
            elif event.get('type') == 'document':
                bot.send_document(
                    chat_id=telegram_info.id,
                    document=event.get('attachment_id'),
                    caption=event.get('description'),
                    reply_markup=keyboard,
                    parse_mode=telegram.ParseMode.MARKDOWN
                )
            else:
                bot.edit_message_text(
                    text=event.get('description'),
                    chat_id=telegram_info.id,
                    message_id=message.message_id,
                    reply_markup=keyboard
                )
            return stages.SUPPORT_EVENT_LIST
