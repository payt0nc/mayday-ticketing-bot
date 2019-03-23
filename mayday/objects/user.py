class User:
    '''Convert Telegram User Dict to User Object'''

    def __init__(self, telegram_info: dict) -> None:
        self._user_id = telegram_info.get('id', 0)
        self._username = telegram_info.get('username', None)
        self._last_name = telegram_info.get('last_name', '')
        self._first_name = telegram_info.get('first_name', '')
        self._is_bot = telegram_info.get('is_bot', False)
        self._language_code = telegram_info.get('language_code', '')
        self._is_admin = False
        self._is_blacklist = False

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
        if isinstance(value, bool) is False:
            value = False
        self._is_admin = value

    @property
    def blacklist(self):
        return self._is_blacklist

    @blacklist.setter
    def blacklist(self, value: bool):
        if isinstance(value, bool) is False:
            raise TypeError
        self._is_blacklist = value

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
            is_blacklist=self._is_blacklist
        )
