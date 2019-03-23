from mayday.constants import STATUS_MAPPING, conversations
from mayday.controllers.request import RequestHelper
from mayday.helpers import Helper

request_helper = RequestHelper()


class StatHelper(Helper):

    def _flatten_distribution(self, distribution):
        return map(self.flatten, distribution)

    def get_stat(self):
        stats_result = request_helper.get_stats()
        if stats_result.get('status'):
            result = stats_result.get('info')
            stmt = conversations.STATS.format_map(
                {'status_distribution': '\n'.join(
                    map(conversations.STATUS_STAT.format_map,
                        self._flatten_distribution(result.get('status_distribution')))),
                 'ticket_distribution': '\n'.join(
                    map(conversations.TICKET_STAT.format_map,
                        self._flatten_distribution(result.get('ticket_distribution')))),
                 'update_at': result.get('update_at')}
            )
            return stmt
