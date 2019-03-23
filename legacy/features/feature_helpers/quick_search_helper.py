from mayday.constants import (CATEGORY_MAPPING, DATE_MAPPING, PRICE_MAPPING,
                              STATUS_MAPPING)
from mayday.controllers.request import RequestHelper
from mayday.helpers import Helper

request_helper = RequestHelper()


class QuickSearchHelper(Helper):

    def update_cache(self, user_id, content):
        pass

    def get_my_ticket_matching(self, user_id):
        return request_helper.send_match_my_tickets(user_id)
