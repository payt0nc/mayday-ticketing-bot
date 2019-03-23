from telegram import InlineKeyboardButton, InlineKeyboardMarkup


def generate_keyboard(events: list) -> list:
    bottons = [InlineKeyboardButton(event['name'], url=event['url']) for event in events]
    bottons.append([InlineKeyboardButton("返主選單", callback_data='mainpanel')])
    return InlineKeyboardMarkup(bottons, one_time_keyboard=True)
