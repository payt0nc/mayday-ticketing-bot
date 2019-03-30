from telegram import User as TelegramUser


class User:
    '''Convert Telegram User Dict to User Object'''

    def __init__(self, user_profile: dict = None, telegram_user: TelegramUser = None) -> None:

        if telegram_user:
            self._user_id = telegram_user.id
            self._username = telegram_user.username
            self._last_name = telegram_user.last_name
            self._first_name = telegram_user.first_name
            self._is_bot = telegram_user.is_bot
            self._language_code = telegram_user.language_code
            self._is_admin = False
            self._is_blacklist = False

        elif user_profile:
            self._user_id = user_profile['user_id']
            self._username = user_profile['username']
            self._first_name = user_profile.get('first_name', '')
            self._last_name = user_profile.get('last_name', '')
            self._language_code = user_profile.get('language_code', '')
            self._is_admin = bool(user_profile.get('is_admin', False))
            self._is_bot = bool(user_profile.get('is_bot', False))
            self._is_blacklist = bool(user_profile.get('is_blacklist', False))

    @property
    def user_id(self) -> int:
        return self._user_id

    @property
    def username(self) -> str:
        return self._username

    @property
    def admin_role(self):
        return self._is_admin

    @admin_role.setter
    def admin_role(self, value: bool):
        self._is_admin = value if isinstance(value, bool) else False

    @property
    def blacklist(self):
        return self._is_blacklist

    @blacklist.setter
    def blacklist(self, value: bool):
        self._is_blacklist = value if isinstance(value, bool) else False

    def is_username_blank(self) -> bool:
        return not bool(self.username)

    def to_dict(self) -> dict:
        return dict(
            user_id=self.user_id,
            username=self.username,
            last_name=self._last_name,
            first_name=self._first_name,
            is_bot=self._is_bot,
            language_code=self._language_code,
            is_admin=self._is_admin,
            is_blacklist=self._is_blacklist)
