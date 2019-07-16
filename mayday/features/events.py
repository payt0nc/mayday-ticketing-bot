from datetime import datetime
import time

import pytz
from telegram import chataction
from telegram.ext.dispatcher import run_async
from telegram.parsemode import ParseMode

import mayday
from mayday.config import EVENT_LOGGER as event_logger
from mayday.config import ROOT_LOGGER as logger
from mayday.constants import STATUS_MAPPING, conversations, stages
from mayday.helpers.feature_helpers.events_helper import EventHelper
from mayday.objects.user import User

event_helper = EventHelper('events')
TIMEZONE = pytz.timezone('Asia/Taipei')


@run_async
def list_events(bot, update, *args, **kwargs):
    user = User(telegram_user=update.effective_user)
    events = event_helper.list_all_events()
    if events:
        bot.send_message(
            text=conversations.SUPPORT_LIST_EVENTS,
            chat_id=user.user_id,
            reply_markup=event_helper.generate_keyboard(events))
    else:
        bot.send_message(chat_id=user.user_id, text=conversations.SUPPORT_NONE_EVENTS)
    return stages.END


@run_async
def info(bot, update, *args, **kwargs):
    user = User(telegram_user=update.effective_user)
    bot.send_photo(
        chat_id=user.user_id,
        photo=conversations.OFFICIAL_POSTER,
        caption=conversations.INFO,
        parse_mode=ParseMode.MARKDOWN)
    time.sleep(0.5)
    bot.send_photo(
        chat_id=user.user_id,
        photo=conversations.SEATING_PLAN,
        parse_mode=ParseMode.MARKDOWN)
    return stages.END


@run_async
def send_chart(bot, update, *args, **kwargs):
    user = User(telegram_user=update.effective_user)
    bot.send_chat_action(chat_id=user.user_id, action=chataction.ChatAction.TYPING)
    bot.send_message(
        chat_id=user.user_id,
        text=conversations.STATS.format(
            updated_at=datetime.fromtimestamp(int(time.time())).astimezone(TIMEZONE).strftime('%Y-%m-%d %H:%M:%S')))
    return stages.END
