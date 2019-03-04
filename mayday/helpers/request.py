import json

import requests
from mayday import Logger
from mayday import Config

logger = Logger().get_default_logger(__name__)

HEADER = {'Content-Type': 'application/json'}


class RequestHelper(object):

    def __init__(self):
        self.base_url = 'http://{host}:{port}/'.format_map(Config.api_config)

    def send_match_my_tickets(self, user_id):
        url = self.base_url + '/matchingMyTicket/{}'.format(user_id)
        r = requests.get(url)
        return r.json(encoding='UTF-8')

    def send_ticket_query(self, query_content):
        url = self.base_url + '/findTickets'
        logger.debug(json.dumps(query_content, ensure_ascii=False))
        r = requests.post(
            url, data=json.dumps(query_content, ensure_ascii=False).encode('utf-8'), headers=HEADER)
        logger.debug(r.__str__())
        return r.json(encoding='UTF-8')

    def send_ticket_insert(self, ticket):
        url = self.base_url + '/createTicket'
        ticket = self.flatten_wishlist(ticket)
        r = requests.post(
            url, data=json.dumps(ticket, ensure_ascii=False).encode('utf-8'), headers=HEADER)
        logger.info("[ /createTicket Response ] - {} ]".format(r.json(encoding='UTF-8')))
        return r.json(encoding='UTF-8')

    def send_ticket_update(self, ticket):
        url = self. + '/updateTicket/' + str(ticket['id'])
        logger.debug(json.dumps(ticket, ensure_ascii=False))
        r = requests.post(
            url, data=json.dumps(ticket, ensure_ascii=False).encode('utf-8'), headers=HEADER)
        return r.json(encoding='UTF-8')

    def send_search_my_ticket(self, userid):
        url = self.base_url + '/findTicketByUserId/' + str(userid)
        r = requests.get(url)
        return r.json(encoding='UTF-8')

    def send_search_ticket_by_ticket_id(self, ticket_id):
        url = self.base_url + '/findTicketByTicketId/' + str(ticket_id)
        r = requests.get(url)
        return r.json(encoding='UTF-8')

    # Auth and Admin
    def auth(self, profile):
        url = self.base_url + '/auth'
        response = requests.post(
            url, data=json.dumps(profile, ensure_ascii=False).encode('utf-8'), headers=HEADER)
        return response.json(encoding='UTF-8')

    # Stats
    def get_stats(self):
        url = self.base_url + '/getTicketStats'
        r = requests.get(url)
        return r.json(encoding='UTF-8')

    # SP Events
    def get_sp_events(self):
        url = self.base_url + '/getSupportEvents'
        return requests.get(url).json(encoding='UTF-8')

    @staticmethod
    def flatten_wishlist(ticket):
        ticket['wish_date'] = ','.join(map(str, ticket['wish_date']))
        ticket['wish_price_id'] = ','.join(map(str, ticket['wish_price_id']))
        ticket['wish_quantity'] = ','.join(map(str, ticket['wish_quantity']))
        return ticket
