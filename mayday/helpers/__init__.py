import logging

from mayday.constants import (CATEGORY_MAPPING, DATE_MAPPING, PRICE_MAPPING,
                              STATUS_MAPPING, conversations)
from mayday.helpers.redis import RedisHelper
from mayday.objects import Query, Ticket

logger = logging.getLogger()


class Helper:
    def __init__(self, task):
        # self._redis = redis
        self._task = task
        self._last_choice = '{}_last_choice'.format(task)

    def init_cache(self, user_id, username):
        self.reset_cache(user_id, username)
        return self.get_cache(user_id=user_id, username=username)

    def reset_cache(self, user_id, username):
        if self._task == 'search_ticket':
            content = Query(user_id=user_id, username=username).to_dict()
            self.set_cache(user_id, content)
            return content
        elif self._task == 'post_ticket':
            content = Ticket(user_id=user_id, username=username).to_dict()
            self.set_cache(user_id, content)
            return content
        elif self._task == 'update_ticket':
            ticket_id = self.get_cache(user_id=user_id, username=username).get('id')
            # ticket = request.send_search_ticket_by_ticket_id(ticket_id=ticket_id).get('info')
            self.set_cache(user_id=user_id, content=ticket)
            return ticket
        else:
            logger.warning('Reset cache not be implement. But should be work.')

    def update_cache(self, user_id, content):
        raise NotImplementedError

    def get_cache(self, user_id, username):
        result = redis.read(dict(user_id=user_id, action=self._task))
        return result.value if result else self.reset_cache(user_id=user_id, username=username)

    def set_cache(self, user_id, content):
        redis.save(dict(
            user_id=user_id,
            action=self._task,
            value=content
        ))

    def get_last_choice(self, user_id):
        return redis.read(dict(
            user_id=user_id,
            action=self._last_choice)).value

    def set_last_choice(self, user_id, content):
        redis.save(dict(
            user_id=user_id,
            action=self._last_choice,
            value=content))

    # def get_lastest_auth(self, telegram_info):
        # FIXME: removed
        # return authenticator.auth(telegram_info).is_banned

    def generate_tickets_traits(self, tickets):
        trait = []
        for ticket in tickets:
            if 'year' in ticket.keys():
                del ticket['year']
            if 'user_id' in ticket.keys():
                del ticket['user_id']
            trait.append(self.flatten(ticket))
        trait_len = 5
        output = []
        if len(trait) <= trait_len:
            output.append(trait)
        else:
            for i in range(0, len(trait), trait_len):
                output.append(trait[i: i+trait_len])
        return output

    @staticmethod
    def tickets_tostr(tickets):
        return '\n'.join([conversations.TICKET.format_map(ticket) for ticket in tickets])

    @staticmethod
    def flatten(content):
        result = {}
        for key, value in content.items():
            if value:
                if key == 'category':
                    value = CATEGORY_MAPPING.get(value)
                if key == '':
                    value = STATUS_MAPPING.get(value)
                if key == 'date':
                    if isinstance(value, list) or isinstance(value, set):
                        value = ', '.join(map(DATE_MAPPING.get, sorted(value)))
                    elif isinstance(value, int):
                        value = DATE_MAPPING.get(value)
                    else:
                        value = ''
                if key == 'price':
                    if isinstance(value, list) or isinstance(value, set):
                        value = ', '.join(map(PRICE_MAPPING.get, sorted(value)))
                    elif isinstance(value, int):
                        value = PRICE_MAPPING.get(value)
                    else:
                        value = ''
                if key == 'quantity':
                    if isinstance(value, list) or isinstance(value, set):
                        value = ', '.join(map(str, sorted(value)))
                    elif isinstance(value, int):
                        value = str(value)
                    else:
                        value = ''
                if key == 'wish_date':
                    if isinstance(value, str) and value:
                        value = ', '.join(map(DATE_MAPPING.get, sorted(map(int, value.split(',')))))
                    elif isinstance(value, list) or isinstance(value, set):
                        value = ', '.join(map(DATE_MAPPING.get, sorted(value)))
                    else:
                        value = ''

                if key == 'wish_price':
                    if isinstance(value, str) and value:
                        value = ', '.join(map(PRICE_MAPPING.get, sorted(map(int, value.split(',')))))
                    elif isinstance(value, list) or isinstance(value, set):
                        value = ', '.join(map(PRICE_MAPPING.get, sorted(value)))
                    else:
                        value = ''
                if key == 'wish_quantity':
                    if isinstance(value, str) and value:
                        value = ', '.join(map(str, sorted(map(int, value.split(',')))))
                    elif isinstance(value, list) or isinstance(value, set):
                        value = ', '.join(map(str, sorted(value)))
                    else:
                        value = ''
            else:
                if key == 'remarks':
                    value = ''
                elif key == 'username':
                    value = '(請去Setting/設定入面將你的Username/用戶名填上，否則不能提交門票)'
                else:
                    value = ''
            result[key] = value
        return result
