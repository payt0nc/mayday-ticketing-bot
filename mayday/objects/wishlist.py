

class Wishlist:

    def __init__(self, user_id: int, username: str):
        self.user_id = user_id
        self.username = username

        # Wish List
        self.category_id = 2
        self.price_ids = set()
        self.dates = set()
        self.quantities = set()
        self.owned_ticket_ids = set()

    def to_dict(self) -> dict:
        return dict(
            user_id=self.user_id,
            username=self.username,
            dates=self.dates,
            price_ids=self.price_ids,
            quantities=self.quantities
        )

    def validate(self) -> bool:
        # TODO: Add validation
        pass
