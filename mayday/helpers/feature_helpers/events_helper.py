
from telegram import InlineKeyboardButton, InlineKeyboardMarkup

import mayday

from mayday.db.tables.events import EventsModel
from mayday.helpers.feature_helpers import FeatureHelper

event_table = EventsModel(mayday.engine, mayday.metadata)


class EventHelper(FeatureHelper):

    @staticmethod
    def generate_keyboard(events: list) -> list:
        return InlineKeyboardMarkup(
            [[InlineKeyboardButton(event['name'], url=event['url'])] for event in events], one_time_keyboard=True)

    def list_all_events(self) -> list:
        return event_table.list_all_events()

    def reset_cache(self, user_id: int, username: str):
        pass

    def update_cache(self, user_id: int, value: (str, int)):
        pass
