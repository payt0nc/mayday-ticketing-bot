from mayday.helpers import FeatureHelper
from mayday.objects import Ticket
from telegram import InlineKeyboardButton, InlineKeyboardMarkup


class UpdateHelper(FeatureHelper):

    def update_cache(self, user_id: int, value: (str, int)) -> Ticket:
        ticket = self.load_drafting_ticket(user_id)
        last_choice = self.load_last_choice(user_id)
        self.logger.debug(last_choice)
        ticket.update_field(last_choice, value)
        self.save_drafting_ticket(user_id, ticket)
        return ticket

    def reset_cache(self, user_id: int) -> Ticket:
        pass

    def list_tickets_on_reply_keyboard(self, tickets: list):
        buttons = [[InlineKeyboardButton(ticket.ticket_id, callback_data=ticket.ticket_id)] for ticket in tickets]
        buttons.append([InlineKeyboardButton("返主選單", callback_data='mainpanel')])
        return InlineKeyboardMarkup(buttons, one_time_keyboard=True)

    @staticmethod
    def extract_ticket_ids(tickets):
        return [ticket.get('id') for ticket in tickets]
