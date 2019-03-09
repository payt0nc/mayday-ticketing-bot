class User:
    '''Convert Telegram User Dict to User Object'''

    def __init__(self, telegram_info: dict) -> None:
        self.user_id = telegram_info.get('id', 0)
        self.username = telegram_info.get('username', None)
        self.last_name = telegram_info.get('last_name', '')
        self.first_name = telegram_info.get('first_name', '')
        self.is_bot = telegram_info.get('is_bot', False)
        self.language_code = telegram_info.get('language_code', '')
        self._is_admin = False
        self._is_blacklist = False

    @property
    def admin_role(self):
        return self._is_admin

    @admin_role.setter
    def admin_role(self, value: bool):
        if isinstance(value, bool) is False:
            raise TypeError
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
        return bool(self.username)

    def to_dict(self) -> dict:
        return dict(
            user_id=self.user_id,
            username=self.username,
            last_name=self.last_name,
            first_name=self.first_name,
            is_bot=self.is_bot,
            language_code=self.language_code,
            is_admin=self._is_admin,
            is_blacklist=self._is_blacklist
        )
