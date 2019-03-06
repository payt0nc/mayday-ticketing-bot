from mayday.item_validator import ItemValidator


class Query:

    def __init__(self, user_id: int, username: str, category_id: int):

        # Identity
        self._user_id = int(user_id)
        self._username = str(username)
        self._category = category_id

        # Query Context
        self._dates = set()
        self._price_ids = set()
        self._quantities = set()
        self._status = int()

    @property
    def category(self) -> int:
        return self._category

    @category.setter
    def category(self, value: int):
        self._category = value

    @property
    def dates(self) -> list:
        return sorted(self._dates)

    @dates.setter
    def dates(self, value: int):
        self._dates.add(value)

    @property
    def price_ids(self) -> list:
        return sorted(self._price_ids)

    @price_ids.setter
    def price_ids(self, value: int):
        self._price_ids.add(value)

    @property
    def quantities(self) -> list:
        return sorted(self._quantities)

    @quantities.setter
    def quantities(self, value: int):
        self._quantities.add(value)

    @property
    def status(self) -> int:
        return self._status

    @status.setter
    def status(self, value: int):
        self._status = value

    def to_dict(self) -> dict:
        return dict(
            category=self.category,
            dates=self.dates,
            price_ids=self.price_ids,
            quantities=self.quantities,
            status=self.status,
            username=self._username,
            user_id=self._user_id
        )

    def validate(self) -> dict:
        validator = ItemValidator(self.to_dict())
        return validator.check_query()
