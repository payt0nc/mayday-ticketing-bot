from telegram import InlineKeyboardButton, InlineKeyboardMarkup

from mayday.helpers import Helper


class SPEventHelper(Helper):

    def generate_keyboard(self, events):
        def _gen_botton(event):
            idx = event.get('id')
            name = event.get('name')
            return InlineKeyboardButton(name, callback_data=int(idx))

        bottons = [[_gen_botton(event) for event in events]]
        bottons.append([InlineKeyboardButton("返主選單", callback_data='mainpanel')])
        return InlineKeyboardMarkup(bottons, one_time_keyboard=True)

    def generate_event_mapping(self, events: dict):
        msg = dict()
        for event in events:
            msg[event['id']] = dict(
                type=event['attachment_type'],
                description=event['description'].replace('\r', ''),
                attachment_id=event['attachment_hex']
            )
        return msg
