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
        self._wish_date = set()
        self._wish_price = set()
        self._wish_quantity = set()
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
    def wish_date(self) -> int:
        return sorted(self._wish_date)

    @wish_date.setter
    def wish_date(self, value: int):
        self.wish_date.add(value)

    @property
    def wish_price(self) -> int:
        return sorted(self._wish_price)

    @wish_price.setter
    def wish_price(self, value: int):
        self.wish_price.add(value)

    @property
    def wish_quantity(self) -> int:
        return sorted(self._wish_quantity)

    @wish_quantity.setter
    def wish_quantity(self, value: int):
        self.wish_quantity.add(value)

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
            status_id=self.status,
            remarks=self.remarks,
            wish_date=self.wish_date,
            wish_price=self.wish_price,
            wish_quantity=self.wish_quantity,
            user_id=self._user_id,
            username=self._username
        )

    def validate(self) -> dict:
        validator = ItemValidator(self.to_dict())
        if self.category == 2:  # For Excahnge Ticket
            return validator.check_ticket_with_wishlist()
        return validator.check_ticket()
