from mayday import Config
from mayday.helpers.request import RequestHelper

helper = RequestHelper()


class User:
    '''Convert Telegram User Dict to User Object'''

    def __init__(self, telegram_info: dict) -> None:
        self.id = telegram_info.get('id', 0)
        self.username = telegram_info.get('username', None)
        self.last_name = telegram_info.get('last_name', '')
        self.first_name = telegram_info.get('first_name', '')
        self.is_bot = telegram_info.get('is_bot', False)
        self.language_code = telegram_info.get('language_code', '')

    def is_username_blank(self) -> bool:
        return bool(self.username)

    def to_dict(self) -> dict:
        return dict(
            id=self.id,
            username=self.username,
            last_name=self.last_name,
            first_name=self.first_name,
            is_bot=self.is_bot,
            language_code=self.language_code
        )

    def validate(self) -> bool:
        return helper.auth(self.to_json())
