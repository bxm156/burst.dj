from sqlalchemy.sql.functions import now

from burstdj.models import *
from burstdj.models.room import Room
from burstdj.models.user import User

class RoomUser(Base):
    __tablename__ = 'room_user'
    id = Column(Integer, primary_key=True)
    time_created = Column(DateTime, default=now())
    room_id = Column(Integer, ForeignKey(Room.id))
    user_id = Column(Integer, ForeignKey(User.id))
    last_ping_time = Column(DateTime, default=now())
