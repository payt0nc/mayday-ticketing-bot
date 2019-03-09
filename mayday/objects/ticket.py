from mayday.item_validator import ItemValidator


class Ticket:

    def __init__(self, user_id: int, username: str):

        self._user_id = user_id
        self._username = username

        self._category = ''
        # Ticket Info
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
        self._remarks = ''

    @property
    def category(self) -> int:
        return self._category

    @category.setter
    def category(self, value: int):
        self._category = value

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
    def wish_dates(self) -> set:
        return self._wish_dates

    @wish_dates.setter
    def wish_dates(self, value: int):
        self._wish_dates.add(value)

    @property
    def wish_prices(self) -> int:
        return self._wish_prices

    @wish_prices.setter
    def wish_prices(self, value: int):
        self._wish_prices.add(value)

    @property
    def wish_quantities(self) -> int:
        return self._wish_quantities

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
    def remarks(self) -> str:
        return self._remarks

    @remarks.setter
    def remarks(self, value: str):
        self._remarks = value

    def to_dict(self):
        return dict(
            category=self.category,
            date=self.date,
            price=self.price,
            quantity=self.quantity,
            section=self.section,
            row=self.row,
            seat=self.seat,
            status=self.status,
            remarks=self.remarks,
            wish_dates=self.wish_dates,
            wish_prices=self.wish_prices,
            wish_quantities=self.wish_quantities,
            user_id=self._user_id,
            username=self._username
        )

    def to_obj(self, query_dict: dict):
        for key, value in query_dict.items():
            if isinstance(value, list):
                value = set(value)
            self.__setattr__('_{}'.format(key), value)
        return self

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
