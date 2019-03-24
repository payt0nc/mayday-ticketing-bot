from mayday.constants import conversations, stages
from mayday.constants.replykeyboards import KEYBOARDS
from mayday.features import search
from mayday.helpers import QuickSearchHelper
import telegram
from telegram import chataction
from telegram.ext.dispatcher import run_async

quick_search_helper = QuickSearchHelper('quick_search')


@run_async
def start(bot, update, user_data):
    telegram_info = update._effective_user
    callback_data = update.callback_query.data
    ticket = quick_search_helper.init_cache(user_id=telegram_info.id,
                                            username=telegram_info.username)

    bot.edit_message_text(
        text=conversations.QUICK_SEARCH_START,
        chat_id=telegram_info.id,
        message_id=update.callback_query.message.message_id,
        reply_markup=KEYBOARDS.quick_search_start_keyboard_markup,
        parse_mode=telegram.ParseMode.MARKDOWN
    )
    return stages.QUICK_SEARCH_MODE_SELECTION


@run_async
def select_mode(bot, update, user_data):
    telegram_info = update._effective_user
    callback_data = update.callback_query.data
    message = update.callback_query.message

    if callback_data == 'mainpanel':
        bot.edit_message_text(
            chat_id=telegram_info.id,
            message_id=message.message_id,
            text=conversations.MAIN_PANEL_START.format_map({'username': telegram_info.username}),
            reply_markup=KEYBOARDS.actions_keyboard_markup,
            parse_mode=telegram.ParseMode.MARKDOWN
        )
        return stages.MAIN_PANEL

    if callback_data == 'cached_condition':
        search.quick_search_start(bot, update, user_data)
        return stages.QUICK_SEARCH_LIST

    if callback_data == 'matching_my_ticket':
        if quick_search_helper.get_lastest_auth(telegram_info) is False:
            update.message.reply_text(conversations.MAIN_PANEL_YELLOWCOW)
            return stages.END

        bot.send_chat_action(
            chat_id=telegram_info.id,
            action=chataction.ChatAction.TYPING
        )
        result = quick_search_helper.get_my_ticket_matching(user_id=telegram_info.id)

        if result.get('status'):
            tickets = result.get('info')
            if (tickets and len(tickets) <= 25):
                bot.send_message(
                    text=conversations.SEARCH_WITH_RESULTS,
                    chat_id=telegram_info.id,
                    message_id=message.message_id

                )
                traits = quick_search_helper.generate_tickets_traits(tickets)
                for trait in traits:
                    bot.send_message(
                        text=quick_search_helper.tickets_tostr(trait),
                        chat_id=telegram_info.id,
                        message_id=message.message_id
                    )
            elif len(tickets) > 25:
                bot.edit_message_text(
                    text=conversations.SEARCH_TOO_MUCH_TICKETS,
                    chat_id=telegram_info.id,
                    message_id=message.message_id

                )
            else:
                bot.edit_message_text(
                    text=conversations.SEARCH_WITHOUT_TICKETS,
                    chat_id=telegram_info.id,
                    message_id=message.message_id

                )
            bot.send_message(
                text=conversations.AND_THEN,
                chat_id=telegram_info.id,
                message_id=message.message_id,
                reply_markup=KEYBOARDS.quick_search_start_keyboard_markup,

            )
        else:
            bot.send_message(
                text=conversations.SEARCH_TICKET_ERROR,
                chat_id=telegram_info.id,
                message_id=message.message_id
            )
            query = quick_search_helper.get_cache(user_id=telegram_info.id, username=telegram_info.username)
            bot.send_message(
                text=conversations.QUICK_SEARCH_START,
                chat_id=telegram_info.id,
                message_id=update.callback_query.message.message_id,
                reply_markup=KEYBOARDS.quick_search_start_keyboard_markup,
                parse_mode=telegram.ParseMode.MARKDOWN
            )
        return stages.QUICK_SEARCH_MODE_SELECTION
