from datetime import datetime
import time

import pytz

from mayday.constants import (CATEGORY_MAPPING, DATE_MAPPING, PRICE_MAPPING,
                              STATUS_MAPPING)
from mayday.helpers.item_validator import ItemValidator

TIMEZONE = pytz.timezone('Asia/Taipei')


class Ticket:

    def __init__(self, user_id: int = 0, username: str = ''):

        self._user_id = user_id
        self._username = username

        self._category = ''
        # Ticket Info
        self._ticket_id = ''
        self._date = ''
        self._price = int()
        self._quantity = int()
        self._section = ''
        self._row = ''
        self._seat = ''
        # WishList
        self._wish_dates = set()
        self._wish_prices = set()
        self._wish_quantities = set()
        # Status
        self._status = 1
        self._source = ''
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
    def ticket_id(self):
        return self._ticket_id

    @property
    def date(self) -> int:
        return self._date

    @date.setter
    def date(self, value: int):
        self._date = value

    @property
    def price(self) -> int:
        return self._price

    @price.setter
    def price(self, value: int):
        self._price = value

    @property
    def quantity(self) -> int:
        return self._quantity

    @quantity.setter
    def quantity(self, value: int):
        self._quantity = value

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

    @wish_dates.setter
    def wish_dates(self, value: int):
        self._wish_dates.add(value)

    @property
    def wish_prices(self) -> list:
        return sorted(set(self._wish_prices))

    @wish_prices.setter
    def wish_prices(self, value: int):
        self._wish_prices.add(value)

    @property
    def wish_quantities(self) -> list:
        return sorted(set(self._wish_quantities))

    @wish_quantities.setter
    def wish_quantities(self, value: int):
        self._wish_quantities.add(value)

    @property
    def status(self) -> int:
        return self._status

    @status.setter
    def status(self, value: int):
        self._status = value

    @property
    def source(self) -> int:
        return self._source

    @source.setter
    def source(self, value: int):
        self._source = value

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
            category=self.category,
            ticket_id=self.ticket_id,
            date=self.date,
            price=self.price,
            quantity=self.quantity,
            section=self.section,
            row=self.row,
            seat=self.seat,
            status=self.status,
            source=self.source,
            remarks=self.remarks,
            wish_dates=self.wish_dates,
            wish_prices=self.wish_prices,
            wish_quantities=self.wish_quantities,
            user_id=self._user_id,
            username=self._username,
            created_at=self._created_at,
            updated_at=int(time.time())
        )

    def to_obj(self, ticket_dict: dict):
        for key, value in ticket_dict.items():
            if isinstance(value, list):
                self.__setattr__('_{}'.format(key), set(value))
            elif key == '_id':
                self.__setattr__('_{}'.format('ticket_id'), str(value)[-6:])
            else:
                self.__setattr__('_{}'.format(key), value)
        return self

    def to_human_readable(self) -> dict:
        return dict(
            category=CATEGORY_MAPPING.get(self.category),
            ticket_id=self.ticket_id,
            date=DATE_MAPPING.get(self.date),
            price=PRICE_MAPPING.get(self.price),
            quantity=self.quantity,
            section=self.section,
            row=self.row,
            seat=self.seat,
            status=STATUS_MAPPING.get(self.status),
            source=self.source,
            remarks=self.remarks,
            wish_dates=', '.join(sorted(set(map(DATE_MAPPING.get, self.wish_dates)))),
            wish_prices=', '.join(sorted(set(map(PRICE_MAPPING.get, self.wish_prices)))),
            wish_quantities=', '.join(sorted(map(str, self.wish_quantities))),
            username=self._username,
            created_at=datetime.fromtimestamp(self._created_at).replace(tzinfo=TIMEZONE).strftime('%Y-%m-%d %H:%M:%S'),
            updated_at=datetime.fromtimestamp(self._updated_at).replace(tzinfo=TIMEZONE).strftime('%Y-%m-%d %H:%M:%S')
        )

    def update_field(self, field_name: str, field_value: (str, int), remove=False) -> bool:
        field_name = '_{}'.format(field_name)
        if isinstance(self.__getattribute__(field_name), set):
            source = self.__getattribute__(field_name)
            if remove:
                source.remove(field_value)
            else:
                source.add(field_value)
            self.__setattr__(field_name, source)
        else:
            self.__setattr__(field_name, field_value)
        return self

    def validate(self) -> dict:
        validator = ItemValidator(self.to_dict())
        if self.category == 2:  # For Excahnge Ticket
            return validator.check_ticket_with_wishlist()
        return validator.check_ticket()
