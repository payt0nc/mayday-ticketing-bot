import mayday
<<<<<<< HEAD
=======
from mayday.config import AUTH_LOGGER as auth_logger
>>>>>>> 589487b7c59176c1e1cd4bd9d287bafb4b3f94b3
from mayday.config import EVENT_LOGGER as event_logger
from mayday.config import ROOT_LOGGER as logger
from mayday.helpers.feature_helpers import FeatureHelper
from mayday.objects.ticket import Ticket


class PostTicketHelper(FeatureHelper):

    def update_cache(self, user_id: int, value) -> Ticket:
        ticket = self.load_drafting_ticket(user_id)
        ticket.update_field(self.load_last_choice(user_id), value)
        logger.info(ticket.to_dict())
        self.save_drafting_ticket(user_id, ticket)
        return ticket

    def reset_cache(self, user_id: int, username: str) -> Ticket:
        return self.reset_drafting_ticket(user_id, username)

    def get_category_id_from_cache(self, user_id: int) -> int:
        category = self.load_drafting_ticket(user_id).category
        return category if category else 1  # 1 is default keyboard and ticket setting
