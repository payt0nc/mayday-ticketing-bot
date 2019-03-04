import json

import requests
import mayday
from mayday import Config

logger = mayday.get_default_logger(__name__)


class RequestHelper:

    HEADER = {'Content-Type': 'application/json'}

    def __init__(self, base_url: str):
        self.base_url = base_url + '{endpoint}'

    # Auth and Admin

    def auth(self, profile: dict) -> dict:
        '''Auth

        Arguments:
            profile {dict} -- user's profile on telegram

        Returns:
            dict -- the results of is_banned and is_admin
        '''

        response = requests.post(
            url=self.base_url.format(endpoint='auth'),
            data=json.dumps(profile, ensure_ascii=False).encode('utf-8'),
            headers=self.HEADER
        ).json(encoding='UTF-8')
        return response

    # Tickets
    def get_my_matched_tickets(self, user_id: int) -> list:
        '''Get my matched tickets

        Arguments:
            user_id {int} -- user's telegram id

        Returns:
            tickets {list of dict}-- the ticket match user's wish sorted by created ts desc. 
        '''
        response = requests.get(
            url=self.base_url.format(endpoint='matching'),
            params=dict(user_id=user_id),
            headers=self.HEADER
        ).json(encoding='UTF-8')
        return response

    def get_tickets_by_conditions(self, conditions: dict) -> dict:
        '''Get ticket by condition

        Arguments:
            conditions {dict} -- The conditions that user wants to search the tickets

        Returns:
            tickets {list of dict} -- The tickets meet users' conditions
        '''

        logger.debug(json.dumps(conditions, ensure_ascii=False))
        response = requests.post(
            url=self.base_url.format(endpoint='tickets'),
            data=json.dumps(conditions, ensure_ascii=False).encode('utf-8'),
            headers=self.HEADER).json(encoding='UTF-8')
        logger.debug(response.__str__())
        return response

    def put_a_new_ticket(self, ticket: dict) -> dict:
        '''Create A new ticket in database

        Arguments:
            ticket {dict} -- the ticket stated by user

        Returns:
            ticket {dict} -- the ticket recorded in database.
        '''

        ticket = self.flatten_wishlist(ticket)
        logger.debug(json.dumps(ticket, ensure_ascii=False, sort_keys=True))
        response = requests.put(
            url=self.base_url.format(endpoint='myTicket'),
            data=json.dumps(ticket, ensure_ascii=False).encode('utf-8'),
            headers=self.HEADER).json(encoding='UTF-8')
        logger.info(json.dumps(response, ensure_ascii=False, sort_keys=True))
        return response

    def update_my_ticket(self, ticket: dict) -> dict:
        '''Update My Ticket

        Arguments:
            ticket {dict} -- the ticket after user updated.

        Returns:
            ticket {dict} -- the ticket recorded in database.
        '''

        logger.debug(json.dumps(ticket, ensure_ascii=False))
        response = requests.post(
            url=self.base_url.format(endpoint='myTicket'),
            data=json.dumps(ticket, ensure_ascii=False).encode('utf-8'),
            headers=self.HEADER
        ).json(encoding='UTF-8')
        logger.debug(json.dumps(response))
        return response

    def get_ticket_by_user_id(self, user_id: int) -> list:
        '''Search Ticket By User Id

        Arguments:
            user_id {int} -- user's telegram id

        Returns:
            tickets {list} -- tickets
        '''

        response = requests.get(
            url=self.base_url.format(endpoint='ticket'),
            params=dict(user_id=user_id)
        ).json(encoding='UTF-8')
        return response

    def get_ticket_by_ticket_id(self, ticket_id: int) -> dict:
        '''Search Ticket By Ticket Id 

        Arguments:
            ticket_id {int} -- ticket id

        Returns:
            ticket {dict} -- a ticket with stated ticket id
        '''

        response = requests.get(
            url=self.base_url.format(endpoint='ticket'),
            params=dict(ticket_id=ticket_id)
        ).json(encoding='UTF-8')
        return response

    # Stats
    def get_stats(self) -> dict:
        '''Get ticketing Stats

        Returns:
            results {dict}  -- the stats of ticketing in previous search
        '''

        response = requests.get(url=self.base_url.format(endpoint='stats')).json(encoding='UTF-8')
        return response

    # SP Events
    def get_sp_events(self):
        '''Get special events

        Returns:
            result {list of dict} -- list all supporting events recorded.
        '''
        return requests.get(url=self.base_url.format(endpoint='events')).json(encoding='UTF-8')

    @staticmethod
    def flatten_wishlist(ticket: dict) -> dict:
        ticket['wish_date'] = ','.join(map(str, ticket['wish_date']))
        ticket['wish_price_id'] = ','.join(map(str, ticket['wish_price_id']))
        ticket['wish_quantity'] = ','.join(map(str, ticket['wish_quantity']))
        return ticket
