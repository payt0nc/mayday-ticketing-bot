from telegram.ext import (CallbackQueryHandler, CommandHandler, ConversationHandler, Filters,
                          MessageHandler, RegexHandler, Updater)


import mayday
from mayday import Config
from mayday.constants import stages
from mayday.constants.replykeyboards import ReplyKeyboards
from mayday.features import (mainpanel, post_ticket, search, support,
                             update_ticket, quick_search, platform_stats)

keyboards = ReplyKeyboards()
config = Config()


def main():
    updater = Updater(config.telegram_token, workers=64, request_kwargs={'read_timeout': 30, 'connect_timeout': 60})
    dp = updater.dispatcher

    # Main Panel Handler
    main_panel_handler = ConversationHandler(
        entry_points=[CommandHandler('start', mainpanel.start, pass_user_data=True, pass_chat_data=True)],
        states={
            stages.MAIN_PANEL: [
                CallbackQueryHandler(mainpanel.route, pass_user_data=True, pass_chat_data=True)
            ],
            # Post Stage
            stages.POST_SELECT_FIELD: [
                CallbackQueryHandler(post_ticket.select_field, pass_user_data=True)
            ],
            stages.POST_FILL_VALUE: [
                CallbackQueryHandler(post_ticket.fill_in_field, pass_user_data=True),
                MessageHandler(Filters.text, post_ticket.fill_type_in_field, pass_user_data=True)
            ],
            stages.POST_BEFORE_SUBMIT: [
                CallbackQueryHandler(post_ticket.submit, pass_user_data=True)
            ],
            stages.POST_SUBMIT: [
                CallbackQueryHandler(post_ticket.backward, pass_user_data=True)
            ],
            # Search Stage
            stages.SEARCH_SELECT_FIELD: [
                CallbackQueryHandler(search.select_field, pass_user_data=True)
            ],
            stages.SEARCH_FILL_VALUE: [
                CallbackQueryHandler(search.fill_in_field, pass_user_data=True)
            ],
            stages.SEARCH_BEFORE_SUBMIT: [
                CallbackQueryHandler(search.submit, pass_user_data=True)
            ],
            stages.SEARCH_SUBMIT: [
                CallbackQueryHandler(search.backward, pass_user_data=True)
            ],
            # Update Stage
            stages.UPDATE_SELECT_TICKET: [
                CallbackQueryHandler(update_ticket.select_ticket, pass_user_data=True)
            ],
            stages.UPDATE_SELECT_FIELD: [
                CallbackQueryHandler(update_ticket.select_field, pass_user_data=True)
            ],
            stages.UPDATE_FILL_VALUE: [
                CallbackQueryHandler(update_ticket.fill_in_field, pass_user_data=True),
                MessageHandler(Filters.text, update_ticket.fill_type_in_field, pass_user_data=True)
            ],
            stages.UPDATE_BEFORE_SUBMIT: [
                CallbackQueryHandler(update_ticket.submit, pass_user_data=True)
            ],
            stages.UPDATE_SUBMIT: [
                CallbackQueryHandler(update_ticket.backward, pass_user_data=True)
            ],
            # Quick Search Stage
            stages.QUICK_SEARCH_MODE_SELECTION: [
                CallbackQueryHandler(quick_search.select_mode, pass_user_data=True)
            ],
            stages.QUICK_SEARCH_LIST: [
                CallbackQueryHandler(search.submit, pass_user_data=True)
            ],
            # Event Stage
            stages.SUPPORT_EVENT_LIST: [
                CallbackQueryHandler(support.list_events, pass_user_data=True)
            ],
            # Ticket Stat
            stages.TICKET_STAT_LIST: [
                CallbackQueryHandler(platform_stats.backward, pass_user_data=True)
            ]
        },
        fallbacks=[
            CommandHandler('home', mainpanel.start, pass_user_data=True, pass_chat_data=True),
            RegexHandler('^(Done|done|完)$', mainpanel.done, pass_user_data=True, pass_chat_data=True)
        ],
        per_user=True,
        per_chat=True
    )
    dp.add_handler(main_panel_handler)

    # Force Escape
    dp.add_handler(CommandHandler('help', mainpanel.help))
    dp.add_handler(RegexHandler('^(Done|done|完)$', mainpanel.done, pass_user_data=True, pass_chat_data=True))
    dp.add_handler(CommandHandler('done', mainpanel.done, pass_user_data=True, pass_chat_data=True))

    # log all errors
    dp.add_error_handler(mainpanel.error)

    # Start the Bot
    updater.start_polling(timeout=20, read_latency=5)

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
