from mayday.item_validator import ItemValidator


class Query:

    def __init__(self, user_id: int, username: str, category_id: int):

        # Identity
        self._user_id = int(user_id)
        self._username = str(username)
        self._category = category_id

        # Query Context
        self._dates = set()
        self._prices = set()
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
        return self._dates

    @dates.setter
    def dates(self, value: int):
        self._dates.add(value)

    @property
    def prices(self) -> list:
        return self._prices

    @prices.setter
    def prices(self, value: int):
        self._prices.add(value)

    @property
    def quantities(self) -> list:
        return self._quantities

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
            dates=sorted(self.dates),
            prices=sorted(self.prices),
            quantities=sorted(self.quantities),
            status=self.status,
            username=self._username,
            user_id=self._user_id
        )

    def to_obj(self, query_dict: dict):
        for key, value in query_dict.items():
            if isinstance(value, list):
                value = set(value)
            self.__setattr__('_{}'.format(key), value)
        return self

    def update_field(self, field_name: str, field_value: (str, int), remove=False) -> bool:
        field_name = '_{}'.format(field_name)
        if isinstance(self.__getattribute__(field_name), int):
            self.__setattr__(field_name, field_value)
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
