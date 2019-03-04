from mayday import LogConfig
from mayday.constants import (CATEGORY_MAPPING, DATE_MAPPING, PRICE_MAPPING,
                              STATUS_MAPPING, Query)
from mayday.helpers import Helper

logger = LogConfig.flogger


class SearchHelper(Helper):

    def update_cache(self, user_id, username, content):
        ticket = self.get_cache(user_id=user_id, username=username)
        last_choice = self.get_last_choice(user_id)
        logger.debug(ticket)
        if last_choice in ['category_id', 'status_id']:
            if content != '':
                ticket[last_choice] = int(content)
        elif last_choice in ['quantity', 'price_id', 'date']:
            if content != '':
                ticket[last_choice].append(int(content))
        else:
            ticket[last_choice] = content
        logger.debug(ticket)
        self.set_cache(user_id, ticket)
        return ticket

    def get_quick_search(self, user_id):
        try:
            result = self._redis.read(dict(
                user_id=int(user_id),
                action='quick_search'
            ))
            return result.value
        except Exception:
            return None

    def set_quick_search(self, user_id, query):
        self._redis.save(dict(user_id=int(user_id), action='quick_search', value=query), expiration=None)
        return self.get_quick_search(user_id)
