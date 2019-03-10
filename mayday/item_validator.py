

class ItemValidator:

    def __init__(self, ticket: dict):
        self._ticket = ticket
        self._validation = list()
        self._error_message = list()

    def check_ticket(self) -> dict:
        self.validate_category()
        self.validate_status()
        self.validate_date()
        self.validate_price()
        self.validate_quantity()
        return self.get_report()

    def check_ticket_with_wishlist(self) -> dict:
        self.validate_category()
        self.validate_status()
        self.validate_date()
        self.validate_price()
        self.validate_quantity()
        self.validate_wish_date()
        self.validate_wish_price()
        self.validate_wish_quantity()
        return self.get_report()

    def check_query(self) -> dict:
        self.validate_category()
        return self.get_report()

    def check_wishlist(self) -> dict:
        self.validate_wish_date()
        self.validate_wish_price()
        self.validate_wish_quantity()
        return self.get_report()

    def get_report(self) -> dict:
        if False in self._validation:
            return dict(status=False, info='\n'.join(self._error_message))
        return dict(status=True, info='Pass')

    def validate_category(self):
        result = bool(self._ticket.get('category'))
        if result is False:
            self._error_message.append('門票類別未填喔')
        self._validation.append(result)

    def validate_date(self):
        result = bool(self._ticket.get('date'))
        if result is False:
            self._error_message.append('日期未填喔')
        self._validation.append(result)

    def validate_price(self):
        result = bool(self._ticket.get('price'))
        if result is False:
            self._error_message.append('價錢未填喔')
        self._validation.append(result)

    def validate_quantity(self):
        result = bool(self._ticket.get('quantity'))
        if result is False:
            self._error_message.append('數量未填喔')
        self._validation.append(result)

    def validate_status(self):
        result = bool(self._ticket.get('status'))
        if result is False:
            self._error_message.append('門票狀態未填喔')
        self._validation.append(result)

    def validate_wish_date(self):
        result = bool(self._ticket.get('wish_date'))
        if result is False:
            self._error_message.append('希望交換的日期未填喔')
        self._validation.append(result)

    def validate_wish_price(self):
        result = bool(self._ticket.get('wish_price'))
        if result is False:
            self._error_message.append('希望交換的價格種類未填喔')
        self._validation.append(result)

    def validate_wish_quantity(self):
        result = bool(self._ticket.get('wish_quantity'))
        if result is False:
            self._error_message.append('希望交換的數量未填喔')
        self._validation.append(result)
