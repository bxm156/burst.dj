from sqlalchemy.sql.functions import now

from burstdj.models import *
from burstdj.models.room import Room
from burstdj.models.user import User

class RoomQueue(Base):
    __tablename__ = 'room_queue'
    time_created = Column(DateTime, default=now())
    room_id = Column(Integer, ForeignKey(Room.id), primary_key=True)
    user_id = Column(Integer, ForeignKey(User.id), primary_key=True)
