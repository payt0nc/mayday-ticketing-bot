
class TicketValidator:

    def __init__(self, ticket: dict):
        self._ticket = ticket
        self._validation = list()
        self._error_message = list()

    def _run(self):
        self.validate_category()
        self.validate_status_id()
        self.validate_date()
        self.validate_price()
        self.validate_quantity()

    def check_ticket(self):
        self._run()
        return dict(status=False, info='\n'.join(self._error_message)) if False in self._validation else dict(status=True, info=self._error_message)

    def check_query(self):
        result = {}
        self.validate_category()
        if False in self._validation:
            result['status'] = False
            result['info'] = '\n'.join(self._error_message)
        else:
            result['status'] = True
            result['info'] = self._error_message
        return result

    def validate_category(self):
        if self._ticket.get('category_id'):
            result = True
        else:
            result = False
            self._error_message.append('門票類別未填喔')
        self._validation.append(result)

    def validate_date(self):
        if self._ticket.get('date'):
            result = True
        else:
            result = False
            self._error_message.append('日期未填喔')
        self._validation.append(result)

    def validate_price(self):
        if self._ticket.get('price_id'):
            result = True
        else:
            result = False
            self._error_message.append('價錢未填喔')
        self._validation.append(result)

    def validate_quantity(self):
        if self._ticket.get('quantity'):
            result = True
        else:
            result = False
            self._error_message.append('數量未填喔')
        self._validation.append(result)

    def validate_status_id(self):
        if self._ticket.get('status_id'):
            result = True
        else:
            result = False
            self._error_message.append('門票狀態未填喔')
        self._validation.append(result)
