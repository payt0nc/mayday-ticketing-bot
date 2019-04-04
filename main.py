from telegram.ext import (CallbackQueryHandler, CommandHandler,
                          ConversationHandler, Filters, MessageHandler,
                          RegexHandler, Updater)

import mayday
from mayday.constants import stages
from mayday.features import (mainpanel, post_ticket, quick_search, search, events, update_ticket)


def main():
    updater = Updater(mayday.TELEGRAM_TOKEN, workers=4, request_kwargs={'read_timeout': 30, 'connect_timeout': 60})
    dp = updater.dispatcher

    # Post Ticket Handler
    post_ticket_handler = ConversationHandler(
        entry_points=[CommandHandler('post_ticket', post_ticket.start, pass_user_data=True)],
        states={
            stages.POST_SELECT_FIELD: [CallbackQueryHandler(post_ticket.select_field, pass_user_data=True)],
            stages.POST_FILL_VALUE: [CallbackQueryHandler(post_ticket.fill_in_field, pass_user_data=True),
                                     MessageHandler(Filters.text, post_ticket.fill_type_in_field, pass_user_data=True)],
            stages.POST_BEFORE_SUBMIT: [CallbackQueryHandler(post_ticket.submit, pass_user_data=True)],
            # stages.POST_SUBMIT: [CallbackQueryHandler(post_ticket.backward, pass_user_data=True)]
        },
        fallbacks=[
            CommandHandler('done', mainpanel.done, pass_user_data=True, pass_chat_data=True),
            RegexHandler('^(Done|done|完)$', mainpanel.done, pass_user_data=True, pass_chat_data=True)],
        per_user=True,
        per_chat=True)
    dp.add_handler(post_ticket_handler)

    # Search Ticket Handler
    search_ticket_handler = ConversationHandler(
        entry_points=[CommandHandler('search_tickets', search.start, pass_user_data=True)],
        states={
            stages.SEARCH_SELECT_FIELD: [CallbackQueryHandler(search.select_field, pass_user_data=True)],
            stages.SEARCH_FILL_VALUE: [CallbackQueryHandler(search.fill_in_field, pass_user_data=True)],
            stages.SEARCH_BEFORE_SUBMIT: [CallbackQueryHandler(search.submit, pass_user_data=True)],
            stages.SEARCH_SUBMIT: [CallbackQueryHandler(search.backward, pass_user_data=True)]
        },
        fallbacks=[
            CommandHandler('done', mainpanel.done, pass_user_data=True, pass_chat_data=True),
            RegexHandler('^(Done|done|完)$', mainpanel.done, pass_user_data=True, pass_chat_data=True)],
        per_user=True,
        per_chat=True)
    dp.add_handler(search_ticket_handler)

    # Update Ticket Handler
    update_ticket_handler = ConversationHandler(
        entry_points=[CommandHandler('my_tickets', update_ticket.start, pass_user_data=True)],
        states={
            stages.UPDATE_SELECT_TICKET: [CallbackQueryHandler(update_ticket.select_ticket, pass_user_data=True)],
            stages.UPDATE_SELECT_FIELD: [CallbackQueryHandler(update_ticket.select_field, pass_user_data=True)],
            stages.UPDATE_FILL_VALUE: [CallbackQueryHandler(update_ticket.fill_in_field, pass_user_data=True), MessageHandler(Filters.text, update_ticket.fill_type_in_field, pass_user_data=True)],
            stages.UPDATE_BEFORE_SUBMIT: [CallbackQueryHandler(update_ticket.submit, pass_user_data=True)],
            # stages.UPDATE_SUBMIT: [CallbackQueryHandler(update_ticket.backward, pass_user_data=True)]
        },
        fallbacks=[
            CommandHandler('done', mainpanel.done, pass_user_data=True, pass_chat_data=True),
            RegexHandler('^(Done|done|完)$', mainpanel.done, pass_user_data=True, pass_chat_data=True)],
        per_user=True,
        per_chat=True)
    dp.add_handler(update_ticket_handler)

    # Quick Search Ticket Handler
    quick_search_handler = ConversationHandler(
        entry_points=[CommandHandler('quick_search', quick_search.start, pass_user_data=True)],
        states={
            stages.QUICK_SEARCH_MODE_SELECTION: [CallbackQueryHandler(quick_search.select_mode, pass_user_data=True)],
            stages.QUICK_SEARCH_LIST: [CallbackQueryHandler(search.submit, pass_user_data=True)]},
        fallbacks=[
            CommandHandler('done', mainpanel.done, pass_user_data=True, pass_chat_data=True),
            RegexHandler('^(Done|done|完)$', mainpanel.done, pass_user_data=True, pass_chat_data=True)],
        per_user=True,
        per_chat=True)
    dp.add_handler(quick_search_handler)

    dp.add_handler(CommandHandler('start', mainpanel.menu))
    dp.add_handler(CommandHandler('info', events.info))
    dp.add_handler(CommandHandler('events', events.list_events))
    dp.add_handler(CommandHandler('help', mainpanel.ask_help))
    dp.add_handler(CommandHandler('done', mainpanel.done, pass_user_data=True, pass_chat_data=True))
    dp.add_handler(RegexHandler('^(Done|done|完)$', mainpanel.done, pass_user_data=True, pass_chat_data=True))

    # log all errors
    dp.add_error_handler(mainpanel.error)

    # Start the Bot
    updater.start_polling(timeout=10, read_latency=1)

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
