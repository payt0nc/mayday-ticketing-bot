
class WishlistValidator:
    '''
    'wish_date': self.wish_date,
    'wish_price_id': self.wish_price_id,
    'wish_quantity': self.wish_quantity,
    '''

    def __init__(self, ticket: dict):
        self._ticket = ticket
        self._validation = list()
        self._todo_keys = list()

    def check_wishlist(self):
        if self._ticket.category_id == 2:
            return self.validate_wishlist()
        return dict(status=True, info=[])

    def validate_wishlist(self):
        for key in ['wish_date', 'wish_price_id', 'wish_quantity']:
            if self._ticket.get(key):
                self._validation.append(True)
            else:
                self._validation.append(False)
                self._todo_keys.append(key)

        if False in self._validation:
            return dict(status=False, info=self._todo_keys)
        return dict(status=True, info=[])
