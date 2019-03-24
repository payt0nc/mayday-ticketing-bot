import time

from mayday.constants import (CATEGORY_MAPPING, DATE_MAPPING, PRICE_MAPPING,
                              STATUS_MAPPING)
from mayday.helpers.item_validator import ItemValidator


class Query:

    def __init__(self, category_id: int, user_id: int = 0, username: str = ''):

        # Identity
        self._user_id = int(user_id)
        self._username = str(username)
        self._category = category_id

        # Query Context
        self._dates = set()
        self._prices = set()
        self._quantities = set()
        self._status = 1

        # TS
        self._created_at = int(time.time())
        self._updated_at = int(time.time())

    @property
    def category(self) -> int:
        return self._category

    @property
    def dates(self) -> list:
        return sorted(map(int, self._dates))

    @dates.setter
    def dates(self, value: int):
        self._dates = set(self._dates).add(value)

    @property
    def prices(self) -> list:
        return sorted(map(int, self._prices))

    @prices.setter
    def prices(self, value: int):
        self._prices = set(self._prices).add(value)

    @property
    def quantities(self) -> list:
        return sorted(map(int, self._quantities))

    @quantities.setter
    def quantities(self, value: int):
        self._quantities = set(self._quantities).add(value)

    @property
    def status(self) -> int:
        return self._status

    @status.setter
    def status(self, value: int):
        self._status = value

    @property
    def user_id(self) -> int:
        return self._user_id

    @property
    def username(self) -> str:
        return self._username

    @property
    def created_at(self) -> int:
        return self._created_at

    @property
    def updated_at(self) -> int:
        self._updated_at = int(time.time())
        return self._updated_at

    def to_dict(self) -> dict:
        return dict(
            category=self.category,
            dates=sorted(self.dates),
            prices=sorted(self.prices),
            quantities=sorted(self.quantities),
            status=self.status,
            username=self._username,
            user_id=self._user_id
        )

    def to_human_readable(self) -> dict:
        dates = list(map(DATE_MAPPING.get, self.dates)) if self.dates else list()
        prices = list(map(PRICE_MAPPING.get, self.prices)) if self.prices else list()
        quantities = sorted(map(str, self.quantities)) if self.quantities else list()

        return dict(
            category=CATEGORY_MAPPING.get(self.category),
            dates=', '.join(dates),
            prices=', '.join(prices),
            quantities=', '.join(quantities),
            status=STATUS_MAPPING.get(self.status),
            username=self._username,
            user_id=self._user_id
        )

    def to_mongo_syntax(self) -> dict:
        draft = dict(
            category=self.category,
            date=self.dates,
            price=self.prices,
            quantity=self.quantities,
            status=self.status,
            user_id=self.user_id,
            username=self.username
        )
        result = dict()
        for key, value in draft.items():
            if value:
                if isinstance(value, int) or isinstance(value, str):
                    result[key] = value
                if isinstance(value, list):
                    result[key] = {'$in': value}
        return result

    def to_obj(self, query_dict: dict):
        for key, value in query_dict.items():
            if isinstance(value, list):
                value = set(value)
            self.__setattr__('_{}'.format(key), value)
        return self

    def update_field(self, field_name: str, field_value: (str, int), remove=False) -> bool:
        field_name_mapping = dict(date='dates', price='prices', quantity='quantities')
        field_name = '_{}'.format(field_name_mapping.get(field_name, field_name))
        if isinstance(self.__getattribute__(field_name), int):
            self.__setattr__(field_name, int(field_value))
        elif isinstance(self.__getattribute__(field_name), set):
            source = self.__getattribute__(field_name)
            if remove:
                source.remove(field_value)
            else:
                source.add(field_value)
            self.__setattr__(field_name, source)
        elif isinstance(self.__getattribute__(field_name), list):
            source = self.__getattribute__(field_name)
            if remove:
                source.remove(field_value)
            else:
                source.append(field_value)
            self.__setattr__(field_name, source)
        return self

    def validate(self) -> dict:
        validator = ItemValidator(self.to_dict())
        return validator.check_query()
