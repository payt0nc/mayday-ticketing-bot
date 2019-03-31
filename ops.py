import mayday
from mayday.db.tables.tickets import TicketsModel
from mayday.db.tables.events import EventsModel
from mayday.db.tables.users import UsersModel

if __name__ == "__main__":
    ticket_table = TicketsModel(mayday.engine, mayday.metadata, role='writer')
    user_table = UsersModel(mayday.engine, mayday.metadata, role='writer')
    event_table = EventsModel(mayday.engine, mayday.metadata, role='writer')

    ticket_table.metadata.drop_all()
    user_table.metadata.drop_all()
    event_table.metadata.drop_all()

    ticket_table.metadata.create_all()
    user_table.metadata.create_all()
    event_table.metadata.create_all()
