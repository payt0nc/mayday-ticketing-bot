from telegram import InlineKeyboardButton, InlineKeyboardMarkup

from mayday import LogConfig
from mayday.constants import (CATEGORY_MAPPING, DATE_MAPPING, PRICE_MAPPING,
                              STATUS_MAPPING, conversations)
from mayday.helpers import Helper

logger = LogConfig.flogger


class UpdateHelper(Helper):

    def update_cache(self, user_id, username, content):
        ticket = self.get_cache(user_id=user_id, username=username)
        last_choice = self.get_last_choice(user_id)
        logger.debug(ticket)
        if (content and last_choice in ['category_id', 'status_id', 'quantity',
                                        'price_id', 'date']):
            ticket[last_choice] = int(content)
        else:
            ticket[last_choice] = content
        logger.debug(ticket)
        self.set_cache(user_id, ticket)
        return ticket

    def tickets_tostr(self, tickets):
        return '\n'.join([conversations.UPDATE_YOURS.format_map(self.flatten(ticket)) for ticket in tickets])

    @staticmethod
    def _create_keyboard_button(ticket_id):
        return InlineKeyboardButton(int(ticket_id), callback_data=int(ticket_id))

    def list_tickets_on_reply_keyboard(self, ticket_ids):
        keyboard = [[self._create_keyboard_button(ticket_id)] for ticket_id in ticket_ids]
        keyboard.append([InlineKeyboardButton("返主選單", callback_data='mainpanel')])
        return InlineKeyboardMarkup(keyboard, one_time_keyboard=True)

    @staticmethod
    def extract_ticket_ids(tickets):
        return [ticket.get('id') for ticket in tickets]
