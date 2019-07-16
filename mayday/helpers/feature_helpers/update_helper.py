from telegram import InlineKeyboardButton, InlineKeyboardMarkup

import mayday
from mayday.config import ROOT_LOGGER as logger
from mayday.helpers.feature_helpers import FeatureHelper
from mayday.objects.ticket import Ticket


class UpdateHelper(FeatureHelper):

    def update_cache(self, user_id: int, value: (str, int)) -> Ticket:
        ticket = self.load_drafting_ticket(user_id)
        last_choice = self.load_last_choice(user_id)
        logger.debug(last_choice)
        ticket.update_field(last_choice, value)
        self.save_drafting_ticket(user_id, ticket)
        return ticket

    @staticmethod
    def list_tickets_on_reply_keyboard(tickets: list):
        return InlineKeyboardMarkup([[InlineKeyboardButton(ticket.id, callback_data=ticket.id)] for ticket in tickets], one_time_keyboard=True)

    @staticmethod
    def extract_ticket_ids(tickets):
        return [ticket.get('id') for ticket in tickets]
