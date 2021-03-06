from sqlalchemy.sql.functions import now

from burstdj.models import *
from burstdj.models.user import User

class Room(Base):
    __tablename__ = 'room'
    id = Column(Integer, primary_key=True)
    time_created = Column(DateTime, default=now())
    name = Column(String)
    current_user_id = Column(Integer, ForeignKey(User.id))
    #TODO: Make a ForeignKey when we get track models implemented
    current_track_id = Column(Integer)
    time_track_started = Column(DateTime)

    # the last time we did a scrub of the room to take out stale users
    time_scrubbed = Column(DateTime, default=now())

    #TODO: Include if we have extra time
    admin_user_id = Column(Integer)


Index('room_name', Room.name, unique=True, mysql_length=255)
