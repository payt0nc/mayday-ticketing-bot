import time
from datetime import datetime

import pytz

from mayday.constants import (CATEGORY_MAPPING, DATE_MAPPING, PRICE_MAPPING,
                              STATUS_MAPPING, SOURCE_MAPPING)
from mayday.helpers.item_validator import ItemValidator

TIMEZONE = pytz.timezone('Asia/Taipei')


class Ticket:

    def __init__(self, user_id: int = 0, username: str = ''):

        self._user_id = user_id
        self._username = username

        self._category = int()
        # Ticket Info
        self._id = int()
        self._date = int()
        self._price_id = int()
        self._quantity = int()
        self._section = ''
        self._row = ''
        self._seat = ''
        # WishList
        self._wish_dates = set()
        self._wish_price_ids = set()
        self._wish_quantities = set()
        # Status
        self._status = 1
        self._source_id = int()
        self._remarks = ''
        # TS
        self._created_at = int(time.time())
        self._updated_at = int(time.time())

    @property
    def user_id(self):
        return self._user_id

    @property
    def username(self):
        return self._username

    @property
    def category(self) -> int:
        return self._category

    @category.setter
    def category(self, value: int):
        self._category = value

    @property
    def id(self):
        return self._id

    @property
    def date(self) -> int:
        return self._date

    @date.setter
    def date(self, value: int):
        self._date = int(value)

    @property
    def price_id(self) -> int:
        return self._price_id

    @price_id.setter
    def price_id(self, value: int):
        self._price_id = int(value)

    @property
    def quantity(self) -> int:
        return self._quantity

    @quantity.setter
    def quantity(self, value: int):
        self._quantity = int(value)

    @property
    def section(self) -> str:
        return self._section

    @section.setter
    def section(self, value: str):
        self._section = value

    @property
    def row(self) -> str:
        return self._row

    @row.setter
    def row(self, value: str):
        self._row = value

    @property
    def seat(self) -> str:
        return self._seat

    @seat.setter
    def seat(self, value: str):
        self._seat = value

    @property
    def wish_dates(self) -> list:
        return sorted(set(self._wish_dates))

    @property
    def wish_price_ids(self) -> list:
        return sorted(set(self._wish_price_ids))

    @property
    def wish_quantities(self) -> list:
        return sorted(set(self._wish_quantities))

    @property
    def status(self) -> int:
        return self._status

    @status.setter
    def status(self, value: int):
        self._status = int(value)

    @property
    def source_id(self) -> int:
        return self._source_id

    @source_id.setter
    def source_id(self, value: int):
        self._source_id = int(value)

    @property
    def remarks(self) -> str:
        return self._remarks

    @remarks.setter
    def remarks(self, value: str):
        self._remarks = value

    @property
    def created_at(self) -> int:
        return self._created_at

    @property
    def updated_at(self) -> int:
        self._updated_at = int(time.time())
        return self._updated_at

    def to_dict(self):
        return dict(
            id=self.id,
            category=self.category,
            date=self.date,
            price_id=self.price_id,
            quantity=self.quantity,
            section=self.section,
            row=self.row,
            seat=self.seat,
            status=self.status,
            source_id=self.source_id,
            remarks=self.remarks,
            wish_dates=self.wish_dates,
            wish_price_ids=self.wish_price_ids,
            wish_quantities=self.wish_quantities,
            user_id=self._user_id,
            username=self._username,
            created_at=self._created_at,
            updated_at=int(time.time()))

    def to_obj(self, ticket_dict: dict):
        for key, value in ticket_dict.items():
            if isinstance(value, list):
                self.__setattr__('_{}'.format(key), set(value))
            elif key in {'id', 'id'}:
                if value:
                    self._id = value
            elif key == '_id':
                self._id = str(value)[-6:]
            else:
                self.__setattr__('_{}'.format(key), value)
        return self

    def to_human_readable(self) -> dict:
        return dict(
            category=CATEGORY_MAPPING.get(self.category, ''),
            id=self.id if self.id else '',
            date=DATE_MAPPING.get(self.date, ''),
            price=PRICE_MAPPING.get(self.price_id, ''),
            quantity=self.quantity if self.quantity else '',
            section=self.section if self.section else '',
            row=self.row if self.row else '',
            seat=self.seat if self.seat else '',
            status=STATUS_MAPPING.get(self.status, ''),
            source=SOURCE_MAPPING.get(self.source_id, ''),
            remarks=self.remarks if self.remarks else '',
            wish_dates=', '.join(sorted(set(map(DATE_MAPPING.get, self.wish_dates)))),
            wish_prices=', '.join(sorted(set(map(PRICE_MAPPING.get, self.wish_price_ids)))),
            wish_quantities=', '.join(sorted(map(str, self.wish_quantities))),
            username=self.username,
            created_at=datetime.fromtimestamp(self._created_at).replace(tzinfo=TIMEZONE).strftime('%Y-%m-%d %H:%M:%S'),
            updated_at=datetime.fromtimestamp(self._updated_at).replace(tzinfo=TIMEZONE).strftime('%Y-%m-%d %H:%M:%S')
        )

    def update_field(self, field_name: str, field_value: (str, int), remove=False) -> bool:
        rename_field_name_map = dict(source='source_id', price='price_id', wish_prices='wish_price_ids')
        field_name = '_{}'.format(rename_field_name_map.get(field_name, field_name))
        if isinstance(self.__getattribute__(field_name), set):
            source = self.__getattribute__(field_name)
            if remove:
                source.remove(field_value)
            else:
                source.add(field_value)
            self.__setattr__(field_name, source)
        elif isinstance(self.__getattribute__(field_name), int):
            self.__setattr__(field_name, int(field_value))
        else:
            self.__setattr__(field_name, field_value)
        return self

    def validate(self) -> dict:
        return ItemValidator(self.to_dict()).check_ticket()

    def validate_wishlist(self) -> dict:
        return ItemValidator(self.to_dict()).check_wishlist()

    def fill_full_wishlist(self):
        if self.category == 2:
            if not self.wish_dates:
                self._wish_dates = list(DATE_MAPPING.keys())
            if not self.wish_price_ids:
                self._wish_price_ids = list(PRICE_MAPPING.keys())
            if not self.wish_quantities:
                self._wish_quantities = [x for x in range(1, 5)]
        return self
